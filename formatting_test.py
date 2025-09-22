import requests
import sys
import json
import re

class AIFormattingTester:
    def __init__(self, base_url="https://teamflow-34.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        
        # Sample graph data for testing
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

    def setup_graph_data(self):
        """Upload sample graph data for testing"""
        print("🔧 Setting up graph data for formatting tests...")
        
        url = f"{self.base_url}/upload-graph"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json={"graph_data": self.sample_graph_data}, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                stats = result.get('stats', {})
                print(f"✅ Graph data uploaded: {stats.get('nodes')} nodes, {stats.get('edges')} edges")
                return True
            else:
                print(f"❌ Failed to upload graph data: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading graph data: {str(e)}")
            return False

    def test_ai_formatting_features(self):
        """Test AI analysis formatting with specific question about informal leaders"""
        print("\n🎯 Testing AI Analysis Formatting Features")
        print("=" * 60)
        
        # Use the specific question mentioned in the review request
        test_question = "Who are the informal leaders in our organization, and how do they influence decision-making?"
        
        print(f"Question: {test_question}")
        print("⏳ Processing AI analysis (may take 15-30 seconds)...")
        
        url = f"{self.base_url}/query"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(
                url, 
                json={"question": test_question}, 
                headers=headers, 
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                
                print(f"\n✅ AI Analysis completed successfully!")
                print(f"📊 Response length: {len(answer)} characters")
                
                # Test formatting features
                formatting_results = self.analyze_formatting(answer)
                
                return formatting_results
            else:
                print(f"❌ AI Analysis failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Error text: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error during AI analysis: {str(e)}")
            return False

    def analyze_formatting(self, answer_text):
        """Analyze the formatting features in the AI response"""
        print("\n🔍 Analyzing Formatting Features:")
        print("-" * 40)
        
        formatting_checks = {
            'bold_text': False,
            'italic_text': False,
            'paragraph_breaks': False,
            'key_terms': False,
            'metrics_highlighted': False,
            'proper_structure': False
        }
        
        # Check for bold text formatting (**text**)
        bold_matches = re.findall(r'\*\*(.*?)\*\*', answer_text)
        if bold_matches:
            formatting_checks['bold_text'] = True
            print(f"✅ Bold text found: {len(bold_matches)} instances")
            print(f"   Examples: {bold_matches[:3]}")
        else:
            print("❌ No bold text formatting found")
        
        # Check for italic text formatting (*text*)
        # Need to be careful not to match bold text
        italic_pattern = r'(?<!\*)\*([^*]+?)\*(?!\*)'
        italic_matches = re.findall(italic_pattern, answer_text)
        if italic_matches:
            formatting_checks['italic_text'] = True
            print(f"✅ Italic text found: {len(italic_matches)} instances")
            print(f"   Examples: {italic_matches[:3]}")
        else:
            print("❌ No italic text formatting found")
        
        # Check for paragraph breaks (double newlines)
        paragraph_breaks = answer_text.count('\n\n')
        if paragraph_breaks > 0:
            formatting_checks['paragraph_breaks'] = True
            print(f"✅ Paragraph breaks found: {paragraph_breaks} instances")
        else:
            print("❌ No paragraph breaks found")
        
        # Check for key terms formatting
        key_terms = ['Key Insight:', 'Recommendation:', 'Important:', 'Note:', 'Warning:', 'Action Item:']
        found_key_terms = []
        for term in key_terms:
            if term in answer_text:
                found_key_terms.append(term)
        
        if found_key_terms:
            formatting_checks['key_terms'] = True
            print(f"✅ Key terms found: {found_key_terms}")
        else:
            print("❌ No key terms formatting found")
        
        # Check for metrics highlighting (percentages, ratios)
        percentage_matches = re.findall(r'\*(\d+\.?\d*%)\*', answer_text)
        ratio_matches = re.findall(r'\*(\d+\.?\d* out of \d+)\*', answer_text)
        
        if percentage_matches or ratio_matches:
            formatting_checks['metrics_highlighted'] = True
            print(f"✅ Metrics highlighted:")
            if percentage_matches:
                print(f"   Percentages: {percentage_matches}")
            if ratio_matches:
                print(f"   Ratios: {ratio_matches}")
        else:
            print("❌ No metrics highlighting found")
        
        # Check for proper structure (headers, sections)
        lines = answer_text.split('\n')
        structured_lines = [line for line in lines if line.strip().endswith(':') or '**' in line]
        
        if len(structured_lines) >= 2:
            formatting_checks['proper_structure'] = True
            print(f"✅ Proper structure found: {len(structured_lines)} structured lines")
        else:
            print("❌ Limited structural formatting found")
        
        # Print sample of the formatted text
        print(f"\n📝 Sample of formatted response:")
        print("-" * 40)
        sample_lines = answer_text.split('\n\n')[:2]  # First 2 paragraphs
        for i, paragraph in enumerate(sample_lines, 1):
            if paragraph.strip():
                print(f"Paragraph {i}: {paragraph.strip()[:200]}...")
        
        # Calculate overall formatting score
        passed_checks = sum(formatting_checks.values())
        total_checks = len(formatting_checks)
        
        print(f"\n📊 Formatting Score: {passed_checks}/{total_checks} features implemented")
        
        if passed_checks >= 4:
            print("🎉 Excellent formatting implementation!")
            return True
        elif passed_checks >= 2:
            print("⚠️  Good formatting, but some features missing")
            return True
        else:
            print("❌ Limited formatting implementation")
            return False

def main():
    print("🚀 Starting AI Analysis Formatting Tests")
    print("=" * 60)
    
    tester = AIFormattingTester()
    
    # Setup graph data first
    if not tester.setup_graph_data():
        print("❌ Failed to setup graph data. Cannot proceed with formatting tests.")
        return 1
    
    # Test AI formatting features
    formatting_success = tester.test_ai_formatting_features()
    
    print(f"\n{'='*60}")
    if formatting_success:
        print("🎉 AI Analysis Formatting Tests PASSED!")
        print("✅ Enhanced formatting features are working correctly")
        return 0
    else:
        print("⚠️  AI Analysis Formatting Tests had issues")
        print("❌ Some formatting features may need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())