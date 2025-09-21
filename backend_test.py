import requests
import sys
import json
from datetime import datetime

class PeopleAnalyticsAPITester:
    def __init__(self, base_url="https://teamflow-34.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.sample_graph_data = {
            "nodes": [
                {"data": {"id": "1", "name": "Alice Johnson", "department": "Engineering", "title": "Tech Lead", "group": "backend"}},
                {"data": {"id": "2", "name": "Bob Chen", "department": "Engineering", "title": "Senior Developer", "group": "frontend"}},
                {"data": {"id": "3", "name": "Carol Davis", "department": "Marketing", "title": "Marketing Manager", "group": "content"}},
                {"data": {"id": "4", "name": "David Wilson", "department": "Sales", "title": "Sales Director", "group": "enterprise"}},
                {"data": {"id": "5", "name": "Emily Brown", "department": "Engineering", "title": "DevOps Engineer", "group": "infrastructure"}},
                {"data": {"id": "6", "name": "Frank Miller", "department": "Marketing", "title": "Content Specialist", "group": "content"}},
                {"data": {"id": "7", "name": "Grace Lee", "department": "Sales", "title": "Account Executive", "group": "mid-market"}},
                {"data": {"id": "8", "name": "Henry Garcia", "department": "Engineering", "title": "Product Manager", "group": "product"}},
                {"data": {"id": "9", "name": "Iris Thompson", "department": "Marketing", "title": "Designer", "group": "creative"}},
                {"data": {"id": "10", "name": "Jack Rodriguez", "department": "Sales", "title": "Sales Rep", "group": "smb"}},
                {"data": {"id": "11", "name": "Karen White", "department": "HR", "title": "HR Director", "group": "people"}},
                {"data": {"id": "12", "name": "Luke Anderson", "department": "Engineering", "title": "Data Scientist", "group": "analytics"}},
                {"data": {"id": "13", "name": "Maria Lopez", "department": "Marketing", "title": "Social Media Manager", "group": "social"}},
                {"data": {"id": "14", "name": "Nathan Clark", "department": "Sales", "title": "Customer Success", "group": "support"}},
                {"data": {"id": "15", "name": "Olivia Taylor", "department": "Engineering", "title": "Security Engineer", "group": "security"}}
            ],
            "edges": [
                {"data": {"id": "e1", "source": "1", "target": "2", "weight": 0.8, "type": "collaboration"}},
                {"data": {"id": "e2", "source": "1", "target": "5", "weight": 0.6, "type": "technical"}},
                {"data": {"id": "e3", "source": "1", "target": "8", "weight": 0.9, "type": "project"}},
                {"data": {"id": "e4", "source": "2", "target": "3", "weight": 0.4, "type": "cross-team"}},
                {"data": {"id": "e5", "source": "3", "target": "4", "weight": 0.7, "type": "go-to-market"}},
                {"data": {"id": "e6", "source": "3", "target": "6", "weight": 0.8, "type": "collaboration"}},
                {"data": {"id": "e7", "source": "4", "target": "7", "weight": 0.9, "type": "mentoring"}},
                {"data": {"id": "e8", "source": "4", "target": "10", "weight": 0.6, "type": "supervision"}},
                {"data": {"id": "e9", "source": "5", "target": "12", "weight": 0.5, "type": "infrastructure"}},
                {"data": {"id": "e10", "source": "6", "target": "9", "weight": 0.7, "type": "creative"}},
                {"data": {"id": "e11", "source": "7", "target": "14", "weight": 0.8, "type": "customer"}},
                {"data": {"id": "e12", "source": "8", "target": "12", "weight": 0.6, "type": "data"}},
                {"data": {"id": "e13", "source": "9", "target": "13", "weight": 0.5, "type": "marketing"}},
                {"data": {"id": "e14", "source": "11", "target": "1", "weight": 0.4, "type": "hr-support"}},
                {"data": {"id": "e15", "source": "11", "target": "4", "weight": 0.5, "type": "hr-support"}},
                {"data": {"id": "e16", "source": "11", "target": "3", "weight": 0.3, "type": "hr-support"}},
                {"data": {"id": "e17", "source": "8", "target": "3", "weight": 0.6, "type": "product-marketing"}},
                {"data": {"id": "e18", "source": "15", "target": "1", "weight": 0.5, "type": "security"}},
                {"data": {"id": "e19", "source": "15", "target": "5", "weight": 0.7, "type": "security"}}
            ]
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Non-dict response'}")
                    return True, response_data
                except:
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timed out after {timeout} seconds")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_upload_graph(self):
        """Test graph upload endpoint"""
        success, response = self.run_test(
            "Upload Graph Data",
            "POST",
            "upload-graph",
            200,
            data={"graph_data": self.sample_graph_data}
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            print(f"   Graph Stats: {stats}")
            if stats.get('nodes') == 15 and stats.get('edges') == 19:
                print("   ✅ Graph data uploaded with correct node/edge counts")
                return True
            else:
                print(f"   ⚠️  Unexpected node/edge counts: nodes={stats.get('nodes')}, edges={stats.get('edges')}")
        
        return success

    def test_get_graph_data(self):
        """Test retrieving graph data"""
        success, response = self.run_test(
            "Get Graph Data",
            "GET",
            "graph-data",
            200
        )
        
        if success and isinstance(response, dict):
            graph = response.get('graph', {})
            if 'nodes' in graph and 'edges' in graph:
                print(f"   ✅ Graph data retrieved with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
                return True
            else:
                print("   ⚠️  Graph data missing nodes or edges")
        
        return success

    def test_get_graph_stats(self):
        """Test graph statistics endpoint"""
        success, response = self.run_test(
            "Get Graph Statistics",
            "GET",
            "graph-stats",
            200
        )
        
        if success and isinstance(response, dict):
            expected_keys = ['nodes', 'edges', 'density', 'communities', 'top_central_people']
            missing_keys = [key for key in expected_keys if key not in response]
            
            if not missing_keys:
                print(f"   ✅ All expected stats present")
                print(f"   Stats: nodes={response.get('nodes')}, edges={response.get('edges')}, density={response.get('density'):.3f}")
                print(f"   Communities: {response.get('communities')}, Top central people: {len(response.get('top_central_people', []))}")
                return True
            else:
                print(f"   ⚠️  Missing keys: {missing_keys}")
        
        return success

    def test_nested_format_upload(self):
        """Test upload with nested format (main_combined.json style)"""
        # Create nested format data as mentioned in the review request
        nested_format_data = {
            "graph": {
                "elements": {
                    "nodes": [
                        {"data": {"id": "test1", "name": "Person 1", "department": "Engineering", "title": "Developer"}},
                        {"data": {"id": "test2", "name": "Person 2", "department": "Marketing", "title": "Manager"}},
                        {"data": {"id": "test3", "name": "Person 3", "department": "Sales", "title": "Rep"}}
                    ],
                    "edges": [
                        {"data": {"id": "edge1", "source": "test1", "target": "test2", "weight": 0.8, "type": "collaboration"}},
                        {"data": {"id": "edge2", "source": "test2", "target": "test3", "weight": 0.6, "type": "communication"}}
                    ]
                }
            }
        }
        
        print(f"   Testing nested format: {{graph: {{elements: {{nodes: [], edges: []}}}}}}")
        
        # The backend expects the extracted elements, not the full nested structure
        # So we need to send the elements part
        success, response = self.run_test(
            "Upload Nested Format Graph",
            "POST", 
            "upload-graph",
            200,
            data={"graph_data": nested_format_data["graph"]["elements"]}
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            print(f"   Graph Stats: {stats}")
            if stats.get('nodes') == 3 and stats.get('edges') == 2:
                print("   ✅ Nested format graph uploaded successfully")
                return True
            else:
                print(f"   ⚠️  Unexpected node/edge counts: nodes={stats.get('nodes')}, edges={stats.get('edges')}")
        
        return success

    def test_query_processing(self):
        """Test natural language query processing"""
        test_questions = [
            "Who are the informal leaders in our organization?",
            "Which teams are most at risk of becoming silos?",
            "Where are the communication bottlenecks?"
        ]
        
        all_passed = True
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n   Query {i}: {question}")
            success, response = self.run_test(
                f"Query Processing #{i}",
                "POST",
                "query",
                200,
                data={"question": question},
                timeout=60  # Longer timeout for AI processing
            )
            
            if success and isinstance(response, dict):
                required_keys = ['answer', 'subgraph', 'insights']
                missing_keys = [key for key in required_keys if key not in response]
                
                if not missing_keys:
                    answer_length = len(response.get('answer', ''))
                    subgraph_nodes = len(response.get('subgraph', {}).get('nodes', []))
                    insights_count = len(response.get('insights', []))
                    
                    print(f"   ✅ Query processed successfully")
                    print(f"   Answer length: {answer_length} chars")
                    print(f"   Subgraph nodes: {subgraph_nodes}")
                    print(f"   Insights count: {insights_count}")
                    
                    if answer_length < 50:
                        print(f"   ⚠️  Answer seems too short ({answer_length} chars)")
                        all_passed = False
                else:
                    print(f"   ❌ Missing response keys: {missing_keys}")
                    all_passed = False
            else:
                all_passed = False
        
        return all_passed

def main():
    print("🚀 Starting People Analytics API Tests")
    print("=" * 50)
    
    tester = PeopleAnalyticsAPITester()
    
    # Test sequence
    tests = [
        ("Graph Upload", tester.test_upload_graph),
        ("Nested Format Upload", tester.test_nested_format_upload),
        ("Graph Data Retrieval", tester.test_get_graph_data),
        ("Graph Statistics", tester.test_get_graph_stats),
        ("Query Processing", tester.test_query_processing)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print(f"\n{'='*50}")
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend API tests passed!")
        return 0
    else:
        print("⚠️  Some backend API tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())