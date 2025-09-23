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
#from emergentintegrations.llm.chat import LlmChat, UserMessage
import openai
import logging

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME')

if not mongo_url or not db_name:
    raise ValueError("Missing MONGO_URL or DB_NAME environment variables")

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Create the main app without a prefix
app = FastAPI(title="People Analytics API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global variables for graph data
graph_data = None
nx_graph = None

# Placeholder graph data for demo purposes
PLACEHOLDER_GRAPH_DATA = {
    "nodes": [
        {"data": {"id": "alice", "name": "Alice Johnson", "full_name": "Alice Johnson", "department": "Engineering", "designation": "Senior Manager", "hierarchy_level": 2, "gender": "Female"}},
        {"data": {"id": "bob", "name": "Bob Smith", "full_name": "Bob Smith", "department": "Engineering", "designation": "Developer", "hierarchy_level": 4, "gender": "Male"}},
        {"data": {"id": "charlie", "name": "Charlie Brown", "full_name": "Charlie Brown", "department": "Product", "designation": "Product Manager", "hierarchy_level": 3, "gender": "Male"}},
        {"data": {"id": "diana", "name": "Diana Wilson", "full_name": "Diana Wilson", "department": "Marketing", "designation": "Marketing Director", "hierarchy_level": 2, "gender": "Female"}},
        {"data": {"id": "eve", "name": "Eve Davis", "full_name": "Eve Davis", "department": "Sales", "designation": "Sales Manager", "hierarchy_level": 3, "gender": "Female"}},
        {"data": {"id": "frank", "name": "Frank Miller", "full_name": "Frank Miller", "department": "Engineering", "designation": "Tech Lead", "hierarchy_level": 3, "gender": "Male"}},
        {"data": {"id": "grace", "name": "Grace Lee", "full_name": "Grace Lee", "department": "HR", "designation": "HR Business Partner", "hierarchy_level": 3, "gender": "Female"}},
        {"data": {"id": "henry", "name": "Henry Taylor", "full_name": "Henry Taylor", "department": "Finance", "designation": "Financial Analyst", "hierarchy_level": 4, "gender": "Male"}},
        {"data": {"id": "iris", "name": "Iris Garcia", "full_name": "Iris Garcia", "department": "Product", "designation": "UX Designer", "hierarchy_level": 4, "gender": "Female"}},
        {"data": {"id": "jack", "name": "Jack Thompson", "full_name": "Jack Thompson", "department": "Operations", "designation": "Operations Manager", "hierarchy_level": 3, "gender": "Male"}},
        {"data": {"id": "kate", "name": "Kate Anderson", "full_name": "Kate Anderson", "department": "Marketing", "designation": "Content Strategist", "hierarchy_level": 4, "gender": "Female"}},
        {"data": {"id": "leo", "name": "Leo Rodriguez", "full_name": "Leo Rodriguez", "department": "Sales", "designation": "Sales Representative", "hierarchy_level": 5, "gender": "Male"}},
        {"data": {"id": "mary", "name": "Mary Chen", "full_name": "Mary Chen", "department": "Engineering", "designation": "QA Engineer", "hierarchy_level": 4, "gender": "Female"}},
        {"data": {"id": "nick", "name": "Nick White", "full_name": "Nick White", "department": "Finance", "designation": "Finance Director", "hierarchy_level": 2, "gender": "Male"}},
        {"data": {"id": "olivia", "name": "Olivia Kumar", "full_name": "Olivia Kumar", "department": "Product", "designation": "Product Owner", "hierarchy_level": 4, "gender": "Female"}}
    ],
    "edges": [
        {"data": {"id": "alice-bob", "source": "alice", "target": "bob", "weight": 2}},
        {"data": {"id": "alice-frank", "source": "alice", "target": "frank", "weight": 3}},
        {"data": {"id": "alice-charlie", "source": "alice", "target": "charlie", "weight": 2}},
        {"data": {"id": "alice-diana", "source": "alice", "target": "diana", "weight": 1}},
        {"data": {"id": "bob-frank", "source": "bob", "target": "frank", "weight": 3}},
        {"data": {"id": "bob-mary", "source": "bob", "target": "mary", "weight": 2}},
        {"data": {"id": "charlie-iris", "source": "charlie", "target": "iris", "weight": 2}},
        {"data": {"id": "charlie-olivia", "source": "charlie", "target": "olivia", "weight": 2}},
        {"data": {"id": "charlie-alice", "source": "charlie", "target": "alice", "weight": 1}},
        {"data": {"id": "diana-kate", "source": "diana", "target": "kate", "weight": 2}},
        {"data": {"id": "diana-grace", "source": "diana", "target": "grace", "weight": 1}},
        {"data": {"id": "eve-leo", "source": "eve", "target": "leo", "weight": 3}},
        {"data": {"id": "eve-jack", "source": "eve", "target": "jack", "weight": 1}},
        {"data": {"id": "frank-mary", "source": "frank", "target": "mary", "weight": 2}},
        {"data": {"id": "grace-henry", "source": "grace", "target": "henry", "weight": 1}},
        {"data": {"id": "grace-nick", "source": "grace", "target": "nick", "weight": 1}},
        {"data": {"id": "henry-nick", "source": "henry", "target": "nick", "weight": 3}},
        {"data": {"id": "iris-olivia", "source": "iris", "target": "olivia", "weight": 2}},
        {"data": {"id": "jack-nick", "source": "jack", "target": "nick", "weight": 1}},
        {"data": {"id": "kate-eve", "source": "kate", "target": "eve", "weight": 1}},
        {"data": {"id": "charlie-diana", "source": "charlie", "target": "diana", "weight": 1}},
        {"data": {"id": "alice-grace", "source": "alice", "target": "grace", "weight": 1}},
        {"data": {"id": "frank-charlie", "source": "frank", "target": "charlie", "weight": 1}},
        {"data": {"id": "mary-iris", "source": "mary", "target": "iris", "weight": 1}},
        {"data": {"id": "leo-jack", "source": "leo", "target": "jack", "weight": 1}}
    ]
}

def initialize_placeholder_graph():
    """Initialize the placeholder graph on startup"""
    global graph_data, nx_graph
    try:
        graph_data = PLACEHOLDER_GRAPH_DATA
        nx_graph = load_cytoscape_to_networkx(graph_data)
        logging.info(f"Placeholder graph initialized with {nx_graph.number_of_nodes()} nodes and {nx_graph.number_of_edges()} edges")
    except Exception as e:
        logging.error(f"Failed to initialize placeholder graph: {e}")

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
    G = nx.Graph()
    elements = cytoscape_data.get('elements', cytoscape_data)
    
    # Handle both 'elements' format and direct nodes/edges format
    if 'nodes' in elements and 'edges' in elements:
        nodes_data = elements['nodes']
        edges_data = elements['edges']
    else:
        nodes_data = cytoscape_data.get('nodes', [])
        edges_data = cytoscape_data.get('edges', [])
    
    for node in nodes_data:
        node_id = node['data']['id']
        G.add_node(node_id, **node['data'])
    for edge in edges_data:
        data = edge['data'].copy()
        source = data.pop('source')
        target = data.pop('target')
        G.add_edge(source, target, **data)
    return G

def get_centrality_measures(G):
    """Calculate various centrality measures including PageRank"""
    try:
        centrality_measures = {
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'degree': nx.degree_centrality(G),
            'eigenvector': nx.eigenvector_centrality(G, max_iter=1000),
            'pagerank': nx.pagerank(G, max_iter=1000)
        }
        return centrality_measures
    except:
        # Fallback for disconnected graphs
        centrality_measures = {
            'betweenness': nx.betweenness_centrality(G),
            'closeness': nx.closeness_centrality(G),
            'degree': nx.degree_centrality(G),
            'eigenvector': {node: 0.0 for node in G.nodes()},
            'pagerank': nx.pagerank(G, max_iter=1000)
        }
        return centrality_measures

def detect_upper_outliers(values, method='adaptive'):
    """Detect upper outliers using statistical methods, adaptive for network size"""
    import numpy as np
    
    if not values or len(values) < 2:
        return {}
    
    values_array = np.array(list(values.values()) if isinstance(values, dict) else values)
    n = len(values_array)
    
    # For small networks, use more inclusive methods
    if n <= 10:
        method = 'percentile_75'  # Top 25%
    elif n <= 50:
        method = 'percentile_80'  # Top 20%
    else:
        method = 'iqr'  # Standard IQR for larger networks
    
    if method == 'iqr':
        # Interquartile Range method
        Q1 = np.percentile(values_array, 25)
        Q3 = np.percentile(values_array, 75)
        IQR = Q3 - Q1
        upper_threshold = Q3 + 1.5 * IQR
        
    elif method == 'zscore':
        # Z-score method (1.5 standard deviations for smaller networks)
        mean_val = np.mean(values_array)
        std_val = np.std(values_array)
        upper_threshold = mean_val + 1.5 * std_val
        
    elif method == 'percentile_75':
        # Top 25% method for small networks
        upper_threshold = np.percentile(values_array, 75)
        
    elif method == 'percentile_80':
        # Top 20% method for medium networks
        upper_threshold = np.percentile(values_array, 80)
        
    elif method == 'percentile_90':
        # Top 10% method for large networks
        upper_threshold = np.percentile(values_array, 90)
        
    else:
        # Default: adaptive percentile based on network size
        percentile = 90 - (20 * min(n, 50) / 50)  # 90% for n=1, 70% for n=50
        upper_threshold = np.percentile(values_array, percentile)
    
    if isinstance(values, dict):
        outliers = {k: v for k, v in values.items() if v > upper_threshold}
    else:
        outliers = [v for v in values_array if v > upper_threshold]
    
    # Ensure we get at least top 3 for small networks, even if not statistical outliers
    if isinstance(values, dict) and len(outliers) < 3 and n >= 3:
        sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
        outliers = dict(sorted_values[:min(3, n)])
    
    return outliers

def get_ranked_influencers_and_connectors(G, centrality_measures):
    """Get ranked lists of influencers (PageRank) and connectors (Betweenness) with outlier analysis"""
    
    # Get PageRank scores for influencers
    pagerank_scores = centrality_measures['pagerank']
    betweenness_scores = centrality_measures['betweenness']
    
    # Detect upper outliers
    pagerank_outliers = detect_upper_outliers(pagerank_scores, method='iqr')
    betweenness_outliers = detect_upper_outliers(betweenness_scores, method='iqr')
    
    # Create ranked lists with names and scores
    influencers_list = []
    for node, score in sorted(pagerank_outliers.items(), key=lambda x: x[1], reverse=True):
        node_data = G.nodes.get(node, {})
        name = node_data.get('full_name') or node_data.get('name') or str(node)
        department = node_data.get('department', 'Unknown')
        title = node_data.get('designation') or node_data.get('title', 'Unknown')
        
        influencers_list.append({
            'rank': len(influencers_list) + 1,
            'name': name,
            'pagerank_score': round(score, 4),
            'department': department,
            'title': title,
            'node_id': str(node)
        })
    
    connectors_list = []
    for node, score in sorted(betweenness_outliers.items(), key=lambda x: x[1], reverse=True):
        node_data = G.nodes.get(node, {})
        name = node_data.get('full_name') or node_data.get('name') or str(node)
        department = node_data.get('department', 'Unknown')
        title = node_data.get('designation') or node_data.get('title', 'Unknown')
        
        connectors_list.append({
            'rank': len(connectors_list) + 1,
            'name': name,
            'betweenness_score': round(score, 4),
            'department': department,
            'title': title,
            'node_id': str(node)
        })
    
    return {
        'influencers': influencers_list,
        'connectors': connectors_list,
        'analysis_summary': {
            'total_influencers_identified': len(influencers_list),
            'total_connectors_identified': len(connectors_list),
            'pagerank_threshold': round(min(pagerank_outliers.values()) if pagerank_outliers else 0, 4),
            'betweenness_threshold': round(min(betweenness_outliers.values()) if betweenness_outliers else 0, 4)
        }
    }

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

def analyze_leadership_influence(G, centrality_measures):
    """Analyze leadership and influence patterns using PageRank and statistical outliers"""
    
    # Get ranked influencers and connectors with outlier analysis
    ranked_analysis = get_ranked_influencers_and_connectors(G, centrality_measures)
    
    # Separate formal vs informal leaders based on titles and hierarchy
    formal_leaders = []
    informal_leaders = []
    
    for influencer in ranked_analysis['influencers']:
        node_id = influencer['node_id']
        node_data = G.nodes.get(node_id, {})
        title = node_data.get('designation', '').lower()
        hierarchy = node_data.get('hierarchy_level', 5)
        
        # Formal leaders (by title/hierarchy)
        if any(term in title for term in ['manager', 'director', 'head', 'lead', 'vp', 'ceo']) or hierarchy <= 3:
            formal_leaders.append(influencer)
        else:
            informal_leaders.append(influencer)
    
    leadership_analysis = {
        'all_influencers': ranked_analysis['influencers'],
        'all_connectors': ranked_analysis['connectors'],
        'formal_leaders': formal_leaders,
        'informal_leaders': informal_leaders,
        'analysis_summary': ranked_analysis['analysis_summary']
    }
    
    return leadership_analysis

def analyze_diversity_equity(G, centrality_measures):
    """Analyze diversity and equity in network positions"""
    diversity_analysis = {}
    
    # Analyze by gender
    gender_centrality = {'Male': [], 'Female': [], 'Other': []}
    
    # Analyze by hierarchy level
    hierarchy_centrality = {}
    
    for node, data in G.nodes(data=True):
        gender = data.get('gender', 'Other')
        hierarchy = data.get('hierarchy_level', 5)
        betweenness = centrality_measures['betweenness'].get(node, 0)
        
        if gender in gender_centrality:
            gender_centrality[gender].append(betweenness)
        
        if hierarchy not in hierarchy_centrality:
            hierarchy_centrality[hierarchy] = []
        hierarchy_centrality[hierarchy].append(betweenness)
    
    # Calculate average centrality by group
    diversity_analysis['gender_avg_centrality'] = {
        gender: sum(centralities) / len(centralities) if centralities else 0
        for gender, centralities in gender_centrality.items()
    }
    
    diversity_analysis['hierarchy_avg_centrality'] = {
        level: sum(centralities) / len(centralities) if centralities else 0
        for level, centralities in hierarchy_centrality.items()
    }
    
    return diversity_analysis

def analyze_risk_vulnerability(G, centrality_measures):
    """Analyze network risks and vulnerabilities"""
    risk_analysis = {}
    
    # Identify critical connectors (high betweenness)
    critical_nodes = []
    for node, centrality in centrality_measures['betweenness'].items():
        if centrality > 0.05:  # High threshold for critical nodes
            data = G.nodes[node]
            critical_nodes.append({
                'node': node,
                'name': data.get('full_name', data.get('name', node)),
                'betweenness': centrality,
                'degree': G.degree(node),
                'department': data.get('department', 'Unknown')
            })
    
    risk_analysis['critical_connectors'] = sorted(critical_nodes, key=lambda x: x['betweenness'], reverse=True)[:10]
    
    # Analyze department dependencies
    dept_dependencies = {}
    for node in G.nodes():
        dept = G.nodes[node].get('department', 'Unknown')
        if dept not in dept_dependencies:
            dept_dependencies[dept] = {'nodes': 0, 'total_centrality': 0}
        
        dept_dependencies[dept]['nodes'] += 1
        dept_dependencies[dept]['total_centrality'] += centrality_measures['betweenness'].get(node, 0)
    
    # Calculate vulnerability score (high centrality concentrated in few people)
    for dept, data in dept_dependencies.items():
        if data['nodes'] > 0:
            data['avg_centrality'] = data['total_centrality'] / data['nodes']
            data['vulnerability_score'] = data['total_centrality'] / max(data['nodes'], 1)  # Higher = more vulnerable
    
    risk_analysis['department_vulnerability'] = dept_dependencies
    
    return risk_analysis

def format_analysis_response(response: str) -> str:
    """Format the AI analysis response with better styling"""
    if not response or len(response.strip()) == 0:
        return response
    
    # Split into paragraphs and format
    paragraphs = response.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Format headers (lines that end with colons or are short and ALL CAPS)
        if paragraph.endswith(':') or (len(paragraph) < 50 and paragraph.isupper()):
            paragraph = f"**{paragraph}**"
        
        # Format bullet points
        elif paragraph.startswith('-') or paragraph.startswith('•'):
            # Bold the first part before colon if exists
            if ':' in paragraph:
                parts = paragraph.split(':', 1)
                paragraph = f"**{parts[0]}:** {parts[1].strip()}"
        
        # Format numbered points
        elif any(paragraph.startswith(f"{i}.") for i in range(1, 11)):
            # Bold the first part before colon if exists
            if ':' in paragraph:
                parts = paragraph.split(':', 1)
                paragraph = f"**{parts[0]}:** {parts[1].strip()}"
        
        # Emphasize key terms
        paragraph = paragraph.replace('Key Insight:', '**Key Insight:**')
        paragraph = paragraph.replace('Recommendation:', '**Recommendation:**')
        paragraph = paragraph.replace('Important:', '**Important:**')
        paragraph = paragraph.replace('Note:', '**Note:**')
        paragraph = paragraph.replace('Warning:', '**Warning:**')
        paragraph = paragraph.replace('Action Item:', '**Action Item:**')
        
        # Italicize percentages and metrics
        import re
        paragraph = re.sub(r'(\d+\.?\d*%)', r'*\1*', paragraph)
        paragraph = re.sub(r'(\d+\.?\d* out of \d+)', r'*\1*', paragraph)
        
        formatted_paragraphs.append(paragraph)
    
    # Join with double line breaks for proper spacing
    return '\n\n'.join(formatted_paragraphs)

async def analyze_with_ai(question: str, graph_analysis: Dict) -> str:
    """Use OpenAI to analyze graph data and provide insights with enhanced formatting"""
    try:
        # For placeholder/demo purposes, return a formatted analysis without actual AI call
        # Uncomment the actual AI implementation when you have the LLM setup
        
        placeholder_response = f"""
        **Network Analysis Summary**
        
        Based on your question: "{question}"
        
        **Key Findings:**
        
        The organizational network shows *{graph_analysis.get('total_nodes', 0)} people* connected through *{graph_analysis.get('total_edges', 0)} relationships*.
        
        **Top Influencers (PageRank Analysis):**
        {chr(10).join([f"• **{inf['name']}** ({inf['department']}) - *PageRank: {inf['score']}*" for inf in graph_analysis.get('influencers_analysis', {}).get('top_influencers', [])[:3]])}
        
        **Key Connectors (Betweenness Analysis):**
        {chr(10).join([f"• **{conn['name']}** ({conn['department']}) - *Betweenness: {conn['score']}*" for conn in graph_analysis.get('connectors_analysis', {}).get('top_connectors', [])[:3]])}
        
        **Network Density:** *{graph_analysis.get('density', 0):.3f}* - This indicates {"a highly connected" if graph_analysis.get('density', 0) > 0.3 else "a moderately connected" if graph_analysis.get('density', 0) > 0.1 else "a sparse"} network structure.
        
        **Recommendations:**
        - Monitor key connectors as they bridge different parts of the organization
        - Consider developing backup pathways for critical communication flows
        - Leverage informal leaders for change management initiatives
        
        **Note:** This is a demonstration analysis. Enable AI integration for detailed insights.
        """
        
        return placeholder_response.strip()
        
        # Actual AI implementation (commented out for placeholder functionality)
        """
        # Initialize LLM chat
        chat = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id=f"graph_analysis_{uuid.uuid4()}",
            system_message="You are an expert organizational network analyst..."
        ).with_model("openai", "gpt-4o")
        
        user_message = UserMessage(text=analysis_text)
        response = await chat.send_message(user_message)
        
        return format_analysis_response(response)
        """
        
    except Exception as e:
        logging.error(f"AI analysis failed: {e}")
        return f"**Analysis Summary**\n\nBased on the network analysis, here are the key findings for your question about organizational dynamics and collaboration patterns. Network shows *{graph_analysis.get('total_nodes', 0)} people* with *{graph_analysis.get('total_edges', 0)} connections*."

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
    global graph_data
    if graph_data is None:
        # Try to load from database first
        try:
            db_graph = await db.graph_data.find_one({})
            if db_graph:
                graph_data = db_graph["data"]
                return {"graph": graph_data}
        except Exception as e:
            logging.warning(f"Failed to load from database: {e}")
        
        # If no database data, initialize with placeholder
        initialize_placeholder_graph()
        if graph_data:
            return {"graph": graph_data}
        else:
            raise HTTPException(status_code=404, detail="No graph data found")
    
    return {"graph": graph_data}

@api_router.post("/query", response_model=QueryResponse)
async def query_graph(query: QueryRequest):
    """Process natural language query and return analysis with visualization"""
    global nx_graph
    
    if nx_graph is None:
        # Try to load from database first
        try:
            db_graph = await db.graph_data.find_one({})
            if db_graph:
                global graph_data
                graph_data = db_graph["data"]
                nx_graph = load_cytoscape_to_networkx(graph_data)
        except Exception as e:
            logging.warning(f"Failed to load from database: {e}")
        
        # If still no graph, initialize with placeholder
        if nx_graph is None:
            initialize_placeholder_graph()
            
        if nx_graph is None:
            raise HTTPException(status_code=404, detail="No graph data available. Please upload graph data first.")
    
    try:
        # Perform graph analysis
        centrality_measures = get_centrality_measures(nx_graph)
        communities = find_communities(nx_graph)
        dept_connections, dept_internal = get_department_connections(nx_graph)
        
        # Perform specialized analyses
        leadership_analysis = analyze_leadership_influence(nx_graph, centrality_measures)
        diversity_analysis = analyze_diversity_equity(nx_graph, centrality_measures)
        risk_analysis = analyze_risk_vulnerability(nx_graph, centrality_measures)
        
        # Prepare comprehensive analysis data for AI
        graph_analysis = {
            'total_nodes': nx_graph.number_of_nodes(),
            'total_edges': nx_graph.number_of_edges(),
            'density': nx.density(nx_graph),
            'communities_count': len(set(communities.values())),
            'dept_analysis': {
                'connections': {dept: len(conns) for dept, conns in dept_connections.items()},
                'internal': dept_internal
            },
            'influencers_analysis': {
                'method': 'PageRank with IQR outlier detection',
                'total_identified': len(leadership_analysis['all_influencers']),
                'threshold_score': leadership_analysis['analysis_summary']['pagerank_threshold'],
                'top_influencers': [
                    {
                        'rank': inf['rank'],
                        'name': inf['name'],
                        'score': inf['pagerank_score'],
                        'department': inf['department'],
                        'title': inf['title']
                    } for inf in leadership_analysis['all_influencers'][:10]
                ]
            },
            'connectors_analysis': {
                'method': 'Betweenness Centrality with IQR outlier detection',
                'total_identified': len(leadership_analysis['all_connectors']),
                'threshold_score': leadership_analysis['analysis_summary']['betweenness_threshold'],
                'top_connectors': [
                    {
                        'rank': conn['rank'],
                        'name': conn['name'],
                        'score': conn['betweenness_score'],
                        'department': conn['department'],
                        'title': conn['title']
                    } for conn in leadership_analysis['all_connectors'][:10]
                ]
            },
            'leadership_breakdown': {
                'formal_leaders_count': len(leadership_analysis['formal_leaders']),
                'informal_leaders_count': len(leadership_analysis['informal_leaders']),
                'formal_leaders': leadership_analysis['formal_leaders'][:5],
                'informal_leaders': leadership_analysis['informal_leaders'][:5]
            },
            'diversity_analysis': diversity_analysis,
            'risk_analysis': {
                'critical_connectors_count': len(risk_analysis['critical_connectors']),
                'top_critical': [(conn['name'], conn['betweenness']) for conn in risk_analysis['critical_connectors'][:3]],
                'vulnerable_departments': [dept for dept, data in risk_analysis['department_vulnerability'].items() 
                                         if data.get('vulnerability_score', 0) > 0.02]
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
    global nx_graph
    
    if nx_graph is None:
        # Try to load from database first
        try:
            db_graph = await db.graph_data.find_one({})
            if db_graph:
                global graph_data
                graph_data = db_graph["data"]
                nx_graph = load_cytoscape_to_networkx(graph_data)
        except Exception as e:
            logging.warning(f"Failed to load from database: {e}")
        
        # If still no graph, initialize with placeholder
        if nx_graph is None:
            initialize_placeholder_graph()
            
        if nx_graph is None:
            raise HTTPException(status_code=404, detail="No graph data available")
    
    centrality_measures = get_centrality_measures(nx_graph)
    communities = find_communities(nx_graph)
    
    stats = {
        "nodes": nx_graph.number_of_nodes(),
        "edges": nx_graph.number_of_edges(),
        "density": nx.density(nx_graph),
        "communities": len(set(communities.values())),
        "is_placeholder": graph_data == PLACEHOLDER_GRAPH_DATA,
        "top_central_people": [
            {
                "id": node,
                "name": nx_graph.nodes.get(node, {}).get('name', node),
                "department": nx_graph.nodes.get(node, {}).get('department', 'Unknown'),
                "betweenness": round(score, 4)
            }
            for node, score in sorted(centrality_measures['betweenness'].items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    }
    
    return stats

@api_router.get("/health")
async def health_check():
    return {"status": "ok", "placeholder_available": graph_data is not None}

@api_router.post("/reset-to-placeholder")
async def reset_to_placeholder():
    """Reset graph to placeholder data for demo purposes"""
    initialize_placeholder_graph()
    return {"message": "Graph reset to placeholder data", "nodes": len(PLACEHOLDER_GRAPH_DATA["nodes"]), "edges": len(PLACEHOLDER_GRAPH_DATA["edges"])}

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["https://people-analytics-frontend.onrender.com/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize placeholder graph on startup"""
    logger.info("Starting People Analytics API...")
    
    # Try to load existing data from database first
    try:
        db_graph = await db.graph_data.find_one({})
        if db_graph:
            global graph_data, nx_graph
            graph_data = db_graph["data"]
            nx_graph = load_cytoscape_to_networkx(graph_data)
            logger.info(f"Loaded existing graph from database with {nx_graph.number_of_nodes()} nodes")
        else:
            # No existing data, initialize with placeholder
            initialize_placeholder_graph()
            logger.info("Initialized with placeholder graph data")
    except Exception as e:
        logger.error(f"Failed to load from database: {e}")
        # Fallback to placeholder
        initialize_placeholder_graph()
        logger.info("Using placeholder graph as fallback")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
