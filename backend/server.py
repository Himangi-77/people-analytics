from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import json
import asyncio
import networkx as nx
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global variables for graph data
graph_data = None
nx_graph = None

# Pydantic Models
class GraphUpload(BaseModel):
    graph_data: Dict[str, Any]

class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    subgraph: Dict[str, Any]
    insights: List[str]
    
class GraphNode(BaseModel):
    id: str
    label: str
    department: Optional[str] = None
    title: Optional[str] = None
    group: Optional[str] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    weight: Optional[float] = 1.0
    type: Optional[str] = None

# Graph Analysis Functions
def load_cytoscape_to_networkx(cytoscape_data):
    """Convert Cytoscape JSON to NetworkX graph"""
    G = nx.Graph()
    
    # Add nodes
    if 'elements' in cytoscape_data:
        elements = cytoscape_data['elements']
    else:
        elements = cytoscape_data
    
    nodes = elements.get('nodes', [])
    edges = elements.get('edges', [])
    
    for node in nodes:
        node_id = node['data']['id']
        node_data = node['data']
        G.add_node(node_id, **node_data)
    
    # Add edges
    for edge in edges:
        edge_data = edge['data']
        source = edge_data['source']
        target = edge_data['target']
        weight = edge_data.get('weight', 1.0)
        G.add_edge(source, target, weight=weight, **edge_data)
    
    return G

def get_centrality_measures(G):
    """Calculate various centrality measures"""
    try:
        centrality_measures = {
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'degree': nx.degree_centrality(G),
            'eigenvector': nx.eigenvector_centrality(G, max_iter=1000)
        }
        return centrality_measures
    except:
        # Fallback for disconnected graphs
        centrality_measures = {
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'degree': nx.degree_centrality(G),
            'eigenvector': {node: 0.0 for node in G.nodes()}
        }
        return centrality_measures

def find_communities(G):
    """Detect communities in the graph"""
    try:
        communities = nx.community.greedy_modularity_communities(G)
        community_dict = {}
        for i, community in enumerate(communities):
            for node in community:
                community_dict[node] = i
        return community_dict
    except:
        return {node: 0 for node in G.nodes()}

def get_department_connections(G):
    """Analyze connections between departments"""
    dept_connections = {}
    dept_internal = {}
    
    for node in G.nodes(data=True):
        dept = node[1].get('department', 'Unknown')
        if dept not in dept_connections:
            dept_connections[dept] = set()
            dept_internal[dept] = 0
    
    for edge in G.edges(data=True):
        source_dept = G.nodes[edge[0]].get('department', 'Unknown')
        target_dept = G.nodes[edge[1]].get('department', 'Unknown')
        
        if source_dept == target_dept:
            dept_internal[source_dept] += 1
        else:
            dept_connections[source_dept].add(target_dept)
            dept_connections[target_dept].add(source_dept)
    
    return dept_connections, dept_internal

async def analyze_with_ai(question: str, graph_analysis: Dict) -> str:
    """Use OpenAI to analyze graph data and provide insights"""
    try:
        # Initialize LLM chat
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"graph_analysis_{uuid.uuid4()}",
            system_message="""You are an expert organizational network analyst. 
            You analyze social networks, collaboration patterns, and organizational structures.
            Provide clear, actionable insights based on graph analysis data.
            Focus on practical recommendations for improving organizational effectiveness."""
        ).with_model("openai", "gpt-4o")
        
        # Prepare analysis context
        analysis_text = f"""
        Graph Analysis Data:
        - Total nodes: {graph_analysis.get('total_nodes', 0)}
        - Total edges: {graph_analysis.get('total_edges', 0)}
        - Graph density: {graph_analysis.get('density', 0):.3f}
        - Top central people: {graph_analysis.get('top_central', [])}
        - Communities detected: {graph_analysis.get('communities_count', 0)}
        - Department connections: {graph_analysis.get('dept_analysis', {})}
        
        User Question: {question}
        
        Provide a comprehensive analysis addressing the user's question with specific insights and recommendations.
        """
        
        user_message = UserMessage(text=analysis_text)
        response = await chat.send_message(user_message)
        
        return response
        
    except Exception as e:
        logging.error(f"AI analysis failed: {e}")
        return f"Analysis complete. Based on the graph structure with {graph_analysis.get('total_nodes', 0)} nodes and {graph_analysis.get('total_edges', 0)} edges, here are the key findings related to your question."

def create_subgraph_for_question(G, question: str, centrality_measures: Dict) -> Dict:
    """Create a relevant subgraph based on the question type"""
    question_lower = question.lower()
    
    if 'leader' in question_lower or 'influencer' in question_lower or 'central' in question_lower:
        # Show top central nodes
        top_central = sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:15]
        nodes_to_include = [node[0] for node in top_central]
        
    elif 'bottleneck' in question_lower or 'communication' in question_lower:
        # Show high betweenness centrality nodes
        top_betweenness = sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:10]
        nodes_to_include = [node[0] for node in top_betweenness]
        
    elif 'department' in question_lower or 'team' in question_lower:
        # Show inter-departmental connections
        nodes_to_include = list(G.nodes())[:20]  # Sample for demo
        
    elif 'silo' in question_lower:
        # Show weakly connected components
        components = list(nx.connected_components(G))
        nodes_to_include = list(components[0]) if components else list(G.nodes())[:20]
        
    else:
        # Default: show most connected nodes
        degree_cent = centrality_measures['degree']
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:20]
        nodes_to_include = [node[0] for node in top_degree]
    
    # Create subgraph
    subgraph = G.subgraph(nodes_to_include)
    
    # Convert to Cytoscape format
    cytoscape_subgraph = {
        'nodes': [],
        'edges': []
    }
    
    for node in subgraph.nodes(data=True):
        node_data = node[1].copy()
        node_data['id'] = node[0]
        
        # Add centrality data for visualization
        node_data['betweenness'] = centrality_measures['betweenness'].get(node[0], 0)
        node_data['degree'] = centrality_measures['degree'].get(node[0], 0)
        
        cytoscape_subgraph['nodes'].append({'data': node_data})
    
    for edge in subgraph.edges(data=True):
        edge_data = edge[2].copy()
        edge_data['source'] = edge[0]
        edge_data['target'] = edge[1]
        edge_data['id'] = f"{edge[0]}-{edge[1]}"
        
        cytoscape_subgraph['edges'].append({'data': edge_data})
    
    return cytoscape_subgraph

# API Routes
@api_router.post("/upload-graph")
async def upload_graph(graph_upload: GraphUpload):
    """Upload and process the organizational graph data"""
    global graph_data, nx_graph
    
    try:
        graph_data = graph_upload.graph_data
        nx_graph = load_cytoscape_to_networkx(graph_data)
        
        # Store in database
        await db.graph_data.delete_many({})  # Clear existing data
        await db.graph_data.insert_one({"data": graph_data, "uploaded_at": datetime.utcnow()})
        
        stats = {
            "nodes": nx_graph.number_of_nodes(),
            "edges": nx_graph.number_of_edges(),
            "density": nx.density(nx_graph)
        }
        
        return {"message": "Graph uploaded successfully", "stats": stats}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process graph: {str(e)}")

@api_router.get("/graph-data")
async def get_graph_data():
    """Get the current graph data"""
    if graph_data is None:
        # Try to load from database
        db_graph = await db.graph_data.find_one({})
        if db_graph:
            return {"graph": db_graph["data"]}
        else:
            raise HTTPException(status_code=404, detail="No graph data found")
    
    return {"graph": graph_data}

@api_router.post("/query", response_model=QueryResponse)
async def query_graph(query: QueryRequest):
    """Process natural language query and return analysis with visualization"""
    global nx_graph
    
    if nx_graph is None:
        # Try to load from database
        db_graph = await db.graph_data.find_one({})
        if db_graph:
            global graph_data
            graph_data = db_graph["data"]
            nx_graph = load_cytoscape_to_networkx(graph_data)
        else:
            raise HTTPException(status_code=404, detail="No graph data available. Please upload graph data first.")
    
    try:
        # Perform graph analysis
        centrality_measures = get_centrality_measures(nx_graph)
        communities = find_communities(nx_graph)
        dept_connections, dept_internal = get_department_connections(nx_graph)
        
        # Prepare analysis data for AI
        graph_analysis = {
            'total_nodes': nx_graph.number_of_nodes(),
            'total_edges': nx_graph.number_of_edges(),
            'density': nx.density(nx_graph),
            'top_central': [(node, score) for node, score in sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:5]],
            'communities_count': len(set(communities.values())),
            'dept_analysis': {
                'connections': {dept: len(conns) for dept, conns in dept_connections.items()},
                'internal': dept_internal
            }
        }
        
        # Get AI analysis
        ai_response = await analyze_with_ai(query.question, graph_analysis)
        
        # Create relevant subgraph
        subgraph = create_subgraph_for_question(nx_graph, query.question, centrality_measures)
        
        # Generate insights
        insights = [
            f"Network has {nx_graph.number_of_nodes()} people with {nx_graph.number_of_edges()} connections",
            f"Network density: {nx.density(nx_graph):.3f}",
            f"Communities detected: {len(set(communities.values()))}",
        ]
        
        # Add top central people to insights
        top_central = sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:3]
        for node, score in top_central:
            node_data = nx_graph.nodes.get(node, {})
            name = node_data.get('name', node)
            dept = node_data.get('department', 'Unknown')
            insights.append(f"Key connector: {name} ({dept}) - Centrality: {score:.3f}")
        
        return QueryResponse(
            answer=ai_response,
            subgraph=subgraph,
            insights=insights
        )
        
    except Exception as e:
        logging.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")

@api_router.get("/graph-stats")
async def get_graph_stats():
    """Get basic statistics about the current graph"""
    if nx_graph is None:
        raise HTTPException(status_code=404, detail="No graph data available")
    
    centrality_measures = get_centrality_measures(nx_graph)
    communities = find_communities(nx_graph)
    
    stats = {
        "nodes": nx_graph.number_of_nodes(),
        "edges": nx_graph.number_of_edges(),
        "density": nx.density(nx_graph),
        "communities": len(set(communities.values())),
        "top_central_people": [
            {
                "id": node,
                "name": nx_graph.nodes.get(node, {}).get('name', node),
                "betweenness": score
            }
            for node, score in sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    }
    
    return stats

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()