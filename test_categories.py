import requests
import json

def test_categorized_questions():
    """Test the new categorized question system with specialized analysis"""
    base_url = "https://teamflow-34.preview.emergentagent.com/api"
    
    # Upload sample data first
    sample_graph_data = {
        "nodes": [
            {"data": {"id": "1", "name": "Alice Johnson", "department": "Engineering", "title": "Tech Lead", "group": "backend"}},
            {"data": {"id": "2", "name": "Bob Chen", "department": "Engineering", "title": "Senior Developer", "group": "frontend"}},
            {"data": {"id": "3", "name": "Carol Davis", "department": "Marketing", "title": "Marketing Manager", "group": "content"}},
            {"data": {"id": "4", "name": "David Wilson", "department": "Sales", "title": "Sales Director", "group": "enterprise"}},
            {"data": {"id": "5", "name": "Emily Brown", "department": "Engineering", "title": "DevOps Engineer", "group": "infrastructure"}}
        ],
        "edges": [
            {"data": {"id": "e1", "source": "1", "target": "2", "weight": 0.8, "type": "collaboration"}},
            {"data": {"id": "e2", "source": "1", "target": "5", "weight": 0.6, "type": "technical"}},
            {"data": {"id": "e3", "source": "2", "target": "3", "weight": 0.4, "type": "cross-team"}},
            {"data": {"id": "e4", "source": "3", "target": "4", "weight": 0.7, "type": "go-to-market"}}
        ]
    }
    
    # Upload graph data
    print("🔄 Uploading sample graph data...")
    upload_response = requests.post(f"{base_url}/upload-graph", 
                                  json={"graph_data": sample_graph_data}, 
                                  headers={'Content-Type': 'application/json'})
    
    if upload_response.status_code != 200:
        print(f"❌ Failed to upload graph data: {upload_response.status_code}")
        return False
    
    print("✅ Graph data uploaded successfully")
    
    # Questions from each category as implemented in the frontend
    categorized_questions = {
        'leadership': "Who are the hidden influencers we should recognize or engage in change initiatives?",
        'collaboration': "Which departments are working in silos and need stronger connections?",
        'innovation': "Who are the bridges connecting R&D with Sales and Marketing?",
        'diversity': "Are women and minority groups equally central in the network?",
        'risk': "If this critical person left tomorrow, what part of the network would be disrupted?"
    }
    
    all_passed = True
    
    # Test one question from each category to verify specialized analysis
    for category, question in categorized_questions.items():
        print(f"\n🔍 Testing {category.upper()} category:")
        print(f"   Question: {question}")
        
        try:
            response = requests.post(f"{base_url}/query", 
                                   json={"question": question}, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                
                # Check if the response contains category-specific analysis
                category_indicators = {
                    'leadership': ['leader', 'influence', 'formal', 'informal', 'centrality'],
                    'collaboration': ['silo', 'department', 'collaboration', 'cross-team', 'connection'],
                    'innovation': ['knowledge', 'innovation', 'R&D', 'bridge', 'idea'],
                    'diversity': ['diversity', 'equity', 'gender', 'representation', 'minority'],
                    'risk': ['risk', 'critical', 'vulnerable', 'succession', 'disrupted']
                }
                
                indicators_found = sum(1 for indicator in category_indicators[category] 
                                     if indicator.lower() in answer.lower())
                
                print(f"   ✅ Category-specific analysis detected: {indicators_found}/{len(category_indicators[category])} indicators found")
                
                if indicators_found >= 2:  # At least 2 category-specific terms
                    print(f"   ✅ Specialized {category} analysis confirmed")
                else:
                    print(f"   ⚠️  Limited {category}-specific analysis detected")
                    all_passed = False
                    
                print(f"   Answer length: {len(answer)} chars")
                print(f"   Subgraph nodes: {len(result.get('subgraph', {}).get('nodes', []))}")
                
                # Show a snippet of the answer to verify content
                snippet = answer[:200] + "..." if len(answer) > 200 else answer
                print(f"   Answer snippet: {snippet}")
                
            else:
                print(f"   ❌ Failed to process {category} question: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Error processing {category} question: {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Testing Categorized Question System")
    print("=" * 50)
    
    success = test_categorized_questions()
    
    if success:
        print("\n🎉 All categorized question tests passed!")
    else:
        print("\n⚠️  Some categorized question tests failed")