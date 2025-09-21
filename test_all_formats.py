#!/usr/bin/env python3
"""
Comprehensive test for all three supported graph formats
"""
import json
import tempfile
import os
from pathlib import Path

def create_test_files():
    """Create test files for all three supported formats"""
    
    # Base data
    nodes = [
        {"data": {"id": "test1", "name": "Person 1", "department": "Engineering", "title": "Developer"}},
        {"data": {"id": "test2", "name": "Person 2", "department": "Marketing", "title": "Manager"}},
        {"data": {"id": "test3", "name": "Person 3", "department": "Sales", "title": "Rep"}}
    ]
    
    edges = [
        {"data": {"id": "edge1", "source": "test1", "target": "test2", "weight": 0.8, "type": "collaboration"}},
        {"data": {"id": "edge2", "source": "test2", "target": "test3", "weight": 0.6, "type": "communication"}}
    ]
    
    # Format 1: Nested format (main_combined.json style)
    nested_format = {
        "graph": {
            "elements": {
                "nodes": nodes,
                "edges": edges
            }
        }
    }
    
    # Format 2: Simple format
    simple_format = {
        "nodes": nodes,
        "edges": edges
    }
    
    # Format 3: Elements format
    elements_format = {
        "elements": {
            "nodes": nodes,
            "edges": edges
        }
    }
    
    # Write test files
    test_files = {}
    
    with open("/app/test_nested_format.json", "w") as f:
        json.dump(nested_format, f, indent=2)
        test_files["nested"] = "/app/test_nested_format.json"
    
    with open("/app/test_simple_format.json", "w") as f:
        json.dump(simple_format, f, indent=2)
        test_files["simple"] = "/app/test_simple_format.json"
    
    with open("/app/test_elements_format.json", "w") as f:
        json.dump(elements_format, f, indent=2)
        test_files["elements"] = "/app/test_elements_format.json"
    
    return test_files

def main():
    print("🚀 Creating test files for all supported formats...")
    test_files = create_test_files()
    
    for format_name, file_path in test_files.items():
        print(f"✅ Created {format_name} format test file: {file_path}")
        
        # Show file structure
        with open(file_path, 'r') as f:
            data = json.load(f)
            print(f"   Structure: {list(data.keys())}")
    
    print("\n🎉 All test files created successfully!")
    return test_files

if __name__ == "__main__":
    main()