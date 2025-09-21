import requests
import sys
import json
import tempfile
import os

class GraphUploadTester:
    def __init__(self, base_url="https://teamflow-34.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
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

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_valid_graph_upload(self):
        """Test uploading a valid graph structure"""
        valid_graph = {
            "nodes": [
                {"data": {"id": "test1", "name": "Test Person 1", "department": "Engineering"}},
                {"data": {"id": "test2", "name": "Test Person 2", "department": "Marketing"}}
            ],
            "edges": [
                {"data": {"id": "e1", "source": "test1", "target": "test2", "weight": 0.5}}
            ]
        }
        
        success, response = self.run_test(
            "Valid Graph Upload",
            "POST",
            "upload-graph",
            200,
            data={"graph_data": valid_graph}
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            if stats.get('nodes') == 2 and stats.get('edges') == 1:
                print("   ✅ Valid graph uploaded successfully with correct stats")
                return True
            else:
                print(f"   ⚠️  Unexpected stats: {stats}")
        
        return success

    def test_invalid_json_structure(self):
        """Test uploading invalid JSON structure"""
        invalid_structures = [
            # Missing nodes array
            {"edges": [{"data": {"id": "e1", "source": "1", "target": "2"}}]},
            # Missing edges array  
            {"nodes": [{"data": {"id": "1", "name": "Test"}}]},
            # Empty structure
            {},
            # Wrong structure
            {"data": "invalid"},
            # Nodes not in correct format
            {"nodes": "invalid", "edges": []},
            # Edges not in correct format
            {"nodes": [], "edges": "invalid"}
        ]
        
        all_passed = True
        for i, invalid_graph in enumerate(invalid_structures, 1):
            print(f"\n   Testing invalid structure #{i}: {invalid_graph}")
            success, response = self.run_test(
                f"Invalid Structure #{i}",
                "POST", 
                "upload-graph",
                400,  # Expecting 400 Bad Request
                data={"graph_data": invalid_graph}
            )
            if not success:
                all_passed = False
        
        return all_passed

    def test_empty_graph(self):
        """Test uploading empty graph"""
        empty_graph = {
            "nodes": [],
            "edges": []
        }
        
        success, response = self.run_test(
            "Empty Graph Upload",
            "POST",
            "upload-graph", 
            200,  # Should accept empty graph
            data={"graph_data": empty_graph}
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            if stats.get('nodes') == 0 and stats.get('edges') == 0:
                print("   ✅ Empty graph handled correctly")
                return True
            else:
                print(f"   ⚠️  Unexpected stats for empty graph: {stats}")
        
        return success

    def test_large_graph(self):
        """Test uploading a larger graph"""
        # Create a graph with 50 nodes and 100 edges
        nodes = []
        edges = []
        
        # Generate nodes
        for i in range(50):
            nodes.append({
                "data": {
                    "id": f"node_{i}",
                    "name": f"Person {i}",
                    "department": ["Engineering", "Marketing", "Sales", "HR"][i % 4],
                    "title": f"Title {i}"
                }
            })
        
        # Generate edges (connecting each node to next 2 nodes)
        edge_id = 0
        for i in range(50):
            for j in range(2):
                target = (i + j + 1) % 50
                edges.append({
                    "data": {
                        "id": f"edge_{edge_id}",
                        "source": f"node_{i}",
                        "target": f"node_{target}",
                        "weight": 0.5 + (i * 0.01) % 0.5
                    }
                })
                edge_id += 1
        
        large_graph = {
            "nodes": nodes,
            "edges": edges
        }
        
        success, response = self.run_test(
            "Large Graph Upload (50 nodes, 100 edges)",
            "POST",
            "upload-graph",
            200,
            data={"graph_data": large_graph},
            timeout=60  # Longer timeout for large graph
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            if stats.get('nodes') == 50 and stats.get('edges') == 100:
                print("   ✅ Large graph uploaded successfully")
                return True
            else:
                print(f"   ⚠️  Unexpected stats for large graph: {stats}")
        
        return success

    def test_special_characters(self):
        """Test graph with special characters in names"""
        special_graph = {
            "nodes": [
                {"data": {"id": "1", "name": "José María García-López", "department": "Engineering"}},
                {"data": {"id": "2", "name": "李小明", "department": "Marketing"}},
                {"data": {"id": "3", "name": "Müller & Schmidt", "department": "Sales"}},
                {"data": {"id": "4", "name": "O'Connor-Smith", "department": "HR"}}
            ],
            "edges": [
                {"data": {"id": "e1", "source": "1", "target": "2", "weight": 0.8}},
                {"data": {"id": "e2", "source": "2", "target": "3", "weight": 0.6}},
                {"data": {"id": "e3", "source": "3", "target": "4", "weight": 0.7}}
            ]
        }
        
        success, response = self.run_test(
            "Special Characters in Names",
            "POST",
            "upload-graph",
            200,
            data={"graph_data": special_graph}
        )
        
        if success and isinstance(response, dict):
            stats = response.get('stats', {})
            if stats.get('nodes') == 4 and stats.get('edges') == 3:
                print("   ✅ Graph with special characters uploaded successfully")
                return True
            else:
                print(f"   ⚠️  Unexpected stats: {stats}")
        
        return success

    def test_missing_required_fields(self):
        """Test graphs with missing required fields"""
        test_cases = [
            # Node missing id
            {
                "nodes": [{"data": {"name": "Test Person"}}],
                "edges": []
            },
            # Edge missing source
            {
                "nodes": [{"data": {"id": "1", "name": "Test"}}],
                "edges": [{"data": {"id": "e1", "target": "1"}}]
            },
            # Edge missing target
            {
                "nodes": [{"data": {"id": "1", "name": "Test"}}],
                "edges": [{"data": {"id": "e1", "source": "1"}}]
            }
        ]
        
        all_passed = True
        for i, test_graph in enumerate(test_cases, 1):
            print(f"\n   Testing missing fields case #{i}")
            success, response = self.run_test(
                f"Missing Required Fields #{i}",
                "POST",
                "upload-graph",
                400,  # Should fail with 400
                data={"graph_data": test_graph}
            )
            # For this test, we expect it to fail (400), so success means the test passed
            if not success:
                print(f"   ⚠️  Expected failure but got different result")
                all_passed = False
        
        return all_passed

def main():
    print("🚀 Starting Graph Upload Specific Tests")
    print("=" * 60)
    
    tester = GraphUploadTester()
    
    # Test sequence focusing on upload functionality
    tests = [
        ("Valid Graph Upload", tester.test_valid_graph_upload),
        ("Empty Graph Handling", tester.test_empty_graph),
        ("Large Graph Upload", tester.test_large_graph),
        ("Special Characters", tester.test_special_characters),
        ("Invalid JSON Structures", tester.test_invalid_json_structure),
        ("Missing Required Fields", tester.test_missing_required_fields)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print(f"\n{'='*60}")
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All graph upload tests passed!")
        return 0
    else:
        print("⚠️  Some graph upload tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())