import requests
import json
import sys
from datetime import datetime

class EnhancedAnalysisAPITester:
    def __init__(self, base_url="https://teamflow-34.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        
        # Enhanced sample data with more realistic organizational structure
        self.enhanced_graph_data = {
            "nodes": [
                {"data": {"id": "1", "full_name": "Alice Johnson", "name": "Alice", "department": "Engineering", "designation": "Tech Lead", "hierarchy_level": 3}},
                {"data": {"id": "2", "full_name": "Bob Chen", "name": "Bob", "department": "Engineering", "designation": "Senior Developer", "hierarchy_level": 4}},
                {"data": {"id": "3", "full_name": "Carol Davis", "name": "Carol", "department": "Marketing", "designation": "Marketing Manager", "hierarchy_level": 3}},
                {"data": {"id": "4", "full_name": "David Wilson", "name": "David", "department": "Sales", "designation": "Sales Director", "hierarchy_level": 2}},
                {"data": {"id": "5", "full_name": "Emily Brown", "name": "Emily", "department": "Engineering", "designation": "DevOps Engineer", "hierarchy_level": 4}},
                {"data": {"id": "6", "full_name": "Frank Miller", "name": "Frank", "department": "Marketing", "designation": "Content Specialist", "hierarchy_level": 5}},
                {"data": {"id": "7", "full_name": "Grace Lee", "name": "Grace", "department": "Sales", "designation": "Account Executive", "hierarchy_level": 4}},
                {"data": {"id": "8", "full_name": "Henry Garcia", "name": "Henry", "department": "Engineering", "designation": "Product Manager", "hierarchy_level": 3}},
                {"data": {"id": "9", "full_name": "Iris Thompson", "name": "Iris", "department": "Marketing", "designation": "Designer", "hierarchy_level": 5}},
                {"data": {"id": "10", "full_name": "Jack Rodriguez", "name": "Jack", "department": "Sales", "designation": "Sales Rep", "hierarchy_level": 5}},
                {"data": {"id": "11", "full_name": "Karen White", "name": "Karen", "department": "HR", "designation": "HR Director", "hierarchy_level": 2}},
                {"data": {"id": "12", "full_name": "Luke Anderson", "name": "Luke", "department": "Engineering", "designation": "Data Scientist", "hierarchy_level": 4}},
                {"data": {"id": "13", "full_name": "Maria Lopez", "name": "Maria", "department": "Marketing", "designation": "Social Media Manager", "hierarchy_level": 4}},
                {"data": {"id": "14", "full_name": "Nathan Clark", "name": "Nathan", "department": "Sales", "designation": "Customer Success", "hierarchy_level": 4}},
                {"data": {"id": "15", "full_name": "Olivia Taylor", "name": "Olivia", "department": "Engineering", "designation": "Security Engineer", "hierarchy_level": 4}},
                {"data": {"id": "16", "full_name": "Paul Kim", "name": "Paul", "department": "Finance", "designation": "Finance Manager", "hierarchy_level": 3}},
                {"data": {"id": "17", "full_name": "Quinn Roberts", "name": "Quinn", "department": "Operations", "designation": "Operations Lead", "hierarchy_level": 3}},
                {"data": {"id": "18", "full_name": "Rachel Green", "name": "Rachel", "department": "HR", "designation": "Recruiter", "hierarchy_level": 5}},
                {"data": {"id": "19", "full_name": "Sam Wilson", "name": "Sam", "department": "Finance", "designation": "Financial Analyst", "hierarchy_level": 5}},
                {"data": {"id": "20", "full_name": "Tina Brown", "name": "Tina", "department": "Operations", "designation": "Process Specialist", "hierarchy_level": 5}}
            ],
            "edges": [
                # High centrality connections for Alice (should be top influencer)
                {"data": {"id": "e1", "source": "1", "target": "2", "weight": 0.9, "type": "collaboration"}},
                {"data": {"id": "e2", "source": "1", "target": "5", "weight": 0.8, "type": "technical"}},
                {"data": {"id": "e3", "source": "1", "target": "8", "weight": 0.9, "type": "project"}},
                {"data": {"id": "e4", "source": "1", "target": "12", "weight": 0.7, "type": "data"}},
                {"data": {"id": "e5", "source": "1", "target": "15", "weight": 0.6, "type": "security"}},
                {"data": {"id": "e6", "source": "1", "target": "11", "weight": 0.5, "type": "hr-support"}},
                
                # David as Sales Director with high connections (formal leader)
                {"data": {"id": "e7", "source": "4", "target": "7", "weight": 0.9, "type": "mentoring"}},
                {"data": {"id": "e8", "source": "4", "target": "10", "weight": 0.8, "type": "supervision"}},
                {"data": {"id": "e9", "source": "4", "target": "14", "weight": 0.8, "type": "customer"}},
                {"data": {"id": "e10", "source": "4", "target": "3", "weight": 0.7, "type": "go-to-market"}},
                {"data": {"id": "e11", "source": "4", "target": "16", "weight": 0.6, "type": "finance"}},
                
                # Karen as HR Director (high betweenness - connector)
                {"data": {"id": "e12", "source": "11", "target": "1", "weight": 0.6, "type": "hr-support"}},
                {"data": {"id": "e13", "source": "11", "target": "4", "weight": 0.7, "type": "hr-support"}},
                {"data": {"id": "e14", "source": "11", "target": "3", "weight": 0.5, "type": "hr-support"}},
                {"data": {"id": "e15", "source": "11", "target": "8", "weight": 0.5, "type": "hr-support"}},
                {"data": {"id": "e16", "source": "11", "target": "17", "weight": 0.6, "type": "operations"}},
                {"data": {"id": "e17", "source": "11", "target": "18", "weight": 0.8, "type": "team"}},
                
                # Cross-departmental connections
                {"data": {"id": "e18", "source": "2", "target": "3", "weight": 0.4, "type": "cross-team"}},
                {"data": {"id": "e19", "source": "3", "target": "6", "weight": 0.8, "type": "collaboration"}},
                {"data": {"id": "e20", "source": "6", "target": "9", "weight": 0.7, "type": "creative"}},
                {"data": {"id": "e21", "source": "9", "target": "13", "weight": 0.6, "type": "marketing"}},
                {"data": {"id": "e22", "source": "8", "target": "3", "weight": 0.7, "type": "product-marketing"}},
                {"data": {"id": "e23", "source": "5", "target": "12", "weight": 0.6, "type": "infrastructure"}},
                {"data": {"id": "e24", "source": "7", "target": "14", "weight": 0.8, "type": "customer"}},
                {"data": {"id": "e25", "source": "16", "target": "17", "weight": 0.5, "type": "finance-ops"}},
                {"data": {"id": "e26", "source": "17", "target": "20", "weight": 0.7, "type": "operations"}},
                {"data": {"id": "e27", "source": "16", "target": "19", "weight": 0.8, "type": "finance-team"}},
                {"data": {"id": "e28", "source": "12", "target": "16", "weight": 0.4, "type": "data-finance"}},
                {"data": {"id": "e29", "source": "15", "target": "17", "weight": 0.5, "type": "security-ops"}},
                {"data": {"id": "e30", "source": "8", "target": "17", "weight": 0.4, "type": "product-ops"}}
            ]
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=60):
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

    def test_enhanced_pagerank_analysis(self):
        """Test PageRank algorithm for identifying influencers with numerical scores"""
        print("\n🎯 TESTING ENHANCED PAGERANK ANALYSIS")
        
        # First upload the enhanced graph data
        success, response = self.run_test(
            "Upload Enhanced Graph for PageRank",
            "POST",
            "upload-graph",
            200,
            data={"graph_data": self.enhanced_graph_data}
        )
        
        if not success:
            return False
        
        # Test influencer identification question
        question = "Who are the hidden influencers we should recognize or engage in change initiatives?"
        
        success, response = self.run_test(
            "PageRank Influencer Analysis",
            "POST",
            "query",
            200,
            data={"question": question},
            timeout=90
        )
        
        if success and isinstance(response, dict):
            answer = response.get('answer', '')
            
            # Check for PageRank-specific indicators
            pagerank_indicators = [
                'pagerank', 'PageRank', 'influence', 'influencer', 'score', 'ranking',
                'Alice', 'David', 'Karen'  # Expected top influencers based on our data
            ]
            
            found_indicators = [indicator for indicator in pagerank_indicators 
                              if indicator.lower() in answer.lower()]
            
            print(f"   📊 PageRank indicators found: {len(found_indicators)}/{len(pagerank_indicators)}")
            print(f"   Found: {found_indicators}")
            
            # Check for numerical scores in the response
            import re
            score_patterns = [
                r'\d+\.\d+',  # Decimal scores like 0.1234
                r'score[:\s]+\d+',  # "score: 123" or "score 123"
                r'rank[:\s]+\d+',   # "rank: 1" or "rank 1"
                r'\d+\.',           # Numbered lists like "1."
            ]
            
            numerical_scores = []
            for pattern in score_patterns:
                matches = re.findall(pattern, answer, re.IGNORECASE)
                numerical_scores.extend(matches)
            
            print(f"   🔢 Numerical scores/rankings found: {len(numerical_scores)}")
            if numerical_scores:
                print(f"   Examples: {numerical_scores[:5]}")
            
            # Check for specific names with rankings
            name_ranking_patterns = [
                r'\d+\.\s*[A-Z][a-z]+\s+[A-Z][a-z]+',  # "1. Alice Johnson"
                r'[A-Z][a-z]+\s+[A-Z][a-z]+.*score',   # "Alice Johnson ... score"
                r'[A-Z][a-z]+\s+[A-Z][a-z]+.*rank',    # "Alice Johnson ... rank"
            ]
            
            name_rankings = []
            for pattern in name_ranking_patterns:
                matches = re.findall(pattern, answer)
                name_rankings.extend(matches)
            
            print(f"   👥 Named rankings found: {len(name_rankings)}")
            if name_rankings:
                print(f"   Examples: {name_rankings[:3]}")
            
            # Success criteria
            success_criteria = [
                len(found_indicators) >= 4,  # At least 4 PageRank-related terms
                len(numerical_scores) >= 3,   # At least 3 numerical scores/rankings
                len(answer) >= 1000,          # Substantial analysis
                'Alice' in answer or 'David' in answer or 'Karen' in answer  # Expected influencers
            ]
            
            passed_criteria = sum(success_criteria)
            print(f"   ✅ Success criteria met: {passed_criteria}/4")
            
            if passed_criteria >= 3:
                print("   🎉 PageRank analysis PASSED - Specific names with numerical scores detected!")
                return True
            else:
                print("   ⚠️  PageRank analysis needs improvement - Missing specific rankings/scores")
                return False
        
        return False

    def test_betweenness_centrality_connectors(self):
        """Test Betweenness Centrality for identifying connectors with scores"""
        print("\n🌉 TESTING BETWEENNESS CENTRALITY CONNECTOR ANALYSIS")
        
        question = "Which people serve as the most important connectors between departments?"
        
        success, response = self.run_test(
            "Betweenness Centrality Connector Analysis",
            "POST",
            "query",
            200,
            data={"question": question},
            timeout=90
        )
        
        if success and isinstance(response, dict):
            answer = response.get('answer', '')
            
            # Check for betweenness-specific indicators
            betweenness_indicators = [
                'betweenness', 'connector', 'bridge', 'centrality', 'between',
                'departments', 'cross-functional', 'Karen', 'Alice'  # Expected connectors
            ]
            
            found_indicators = [indicator for indicator in betweenness_indicators 
                              if indicator.lower() in answer.lower()]
            
            print(f"   📊 Betweenness indicators found: {len(found_indicators)}/{len(betweenness_indicators)}")
            print(f"   Found: {found_indicators}")
            
            # Check for connector-specific language
            connector_phrases = [
                'bridge between', 'connects', 'linking', 'intermediary',
                'facilitates communication', 'spans departments'
            ]
            
            connector_language = [phrase for phrase in connector_phrases 
                                if phrase.lower() in answer.lower()]
            
            print(f"   🔗 Connector language found: {len(connector_language)}")
            if connector_language:
                print(f"   Examples: {connector_language}")
            
            # Check for numerical betweenness scores
            import re
            betweenness_scores = re.findall(r'betweenness[:\s]+\d+\.\d+', answer, re.IGNORECASE)
            centrality_scores = re.findall(r'centrality[:\s]+\d+\.\d+', answer, re.IGNORECASE)
            
            print(f"   🔢 Betweenness scores found: {len(betweenness_scores + centrality_scores)}")
            
            # Success criteria
            success_criteria = [
                len(found_indicators) >= 4,
                len(connector_language) >= 1,
                len(answer) >= 1000,
                'Karen' in answer or 'Alice' in answer  # Expected high betweenness
            ]
            
            passed_criteria = sum(success_criteria)
            print(f"   ✅ Success criteria met: {passed_criteria}/4")
            
            if passed_criteria >= 3:
                print("   🎉 Betweenness Centrality analysis PASSED!")
                return True
            else:
                print("   ⚠️  Betweenness analysis needs improvement")
                return False
        
        return False

    def test_statistical_outlier_detection(self):
        """Test upper outlier detection with statistical methods"""
        print("\n📈 TESTING STATISTICAL OUTLIER DETECTION")
        
        question = "Who are the top 5 most influential people in our organization and what are their scores?"
        
        success, response = self.run_test(
            "Statistical Outlier Detection",
            "POST",
            "query",
            200,
            data={"question": question},
            timeout=90
        )
        
        if success and isinstance(response, dict):
            answer = response.get('answer', '')
            
            # Check for statistical method indicators
            statistical_indicators = [
                'IQR', 'percentile', 'threshold', 'outlier', 'statistical',
                'z-score', 'standard deviation', 'quartile', 'method'
            ]
            
            found_indicators = [indicator for indicator in statistical_indicators 
                              if indicator.lower() in answer.lower()]
            
            print(f"   📊 Statistical indicators found: {len(found_indicators)}/{len(statistical_indicators)}")
            print(f"   Found: {found_indicators}")
            
            # Check for threshold mentions
            import re
            threshold_mentions = re.findall(r'threshold[:\s]+\d+\.\d+', answer, re.IGNORECASE)
            method_mentions = re.findall(r'(IQR|percentile|z-score)', answer, re.IGNORECASE)
            
            print(f"   🎯 Threshold scores found: {len(threshold_mentions)}")
            print(f"   📐 Statistical methods mentioned: {method_mentions}")
            
            # Check for top 5 ranking
            top_rankings = re.findall(r'[1-5]\.\s*[A-Z][a-z]+\s+[A-Z][a-z]+', answer)
            numbered_lists = re.findall(r'\d+\.\s*\w+', answer)
            
            print(f"   🏆 Top rankings found: {len(top_rankings)}")
            print(f"   📝 Numbered items: {len(numbered_lists)}")
            
            # Success criteria
            success_criteria = [
                len(found_indicators) >= 2,  # Statistical method indicators
                len(method_mentions) >= 1,    # At least one statistical method mentioned
                len(top_rankings) >= 3,       # At least 3 people ranked
                'top' in answer.lower() and '5' in answer  # Top 5 mentioned
            ]
            
            passed_criteria = sum(success_criteria)
            print(f"   ✅ Success criteria met: {passed_criteria}/4")
            
            if passed_criteria >= 3:
                print("   🎉 Statistical Outlier Detection PASSED!")
                return True
            else:
                print("   ⚠️  Statistical analysis needs improvement")
                return False
        
        return False

    def test_formal_vs_informal_leaders(self):
        """Test differentiation between formal and informal leaders"""
        print("\n👔 TESTING FORMAL VS INFORMAL LEADER DIFFERENTIATION")
        
        question = "Who are the informal leaders in our organization, and how do they influence decision-making?"
        
        success, response = self.run_test(
            "Formal vs Informal Leader Analysis",
            "POST",
            "query",
            200,
            data={"question": question},
            timeout=90
        )
        
        if success and isinstance(response, dict):
            answer = response.get('answer', '')
            
            # Check for formal vs informal indicators
            leadership_indicators = [
                'formal', 'informal', 'title', 'hierarchy', 'manager', 'director',
                'influence without', 'natural leader', 'unofficial'
            ]
            
            found_indicators = [indicator for indicator in leadership_indicators 
                              if indicator.lower() in answer.lower()]
            
            print(f"   📊 Leadership indicators found: {len(found_indicators)}/{len(leadership_indicators)}")
            print(f"   Found: {found_indicators}")
            
            # Check for specific differentiation language
            differentiation_phrases = [
                'formal leader', 'informal leader', 'by title', 'without title',
                'hierarchy', 'natural influence', 'unofficial leader'
            ]
            
            diff_language = [phrase for phrase in differentiation_phrases 
                           if phrase.lower() in answer.lower()]
            
            print(f"   🔍 Differentiation language: {len(diff_language)}")
            if diff_language:
                print(f"   Examples: {diff_language}")
            
            # Success criteria
            success_criteria = [
                len(found_indicators) >= 4,
                len(diff_language) >= 2,
                'formal' in answer.lower() and 'informal' in answer.lower(),
                len(answer) >= 1000
            ]
            
            passed_criteria = sum(success_criteria)
            print(f"   ✅ Success criteria met: {passed_criteria}/4")
            
            if passed_criteria >= 3:
                print("   🎉 Formal vs Informal Leader Analysis PASSED!")
                return True
            else:
                print("   ⚠️  Leadership differentiation needs improvement")
                return False
        
        return False

def main():
    print("🚀 Starting Enhanced PageRank & Outlier Analysis Tests")
    print("=" * 60)
    
    tester = EnhancedAnalysisAPITester()
    
    # Test sequence focusing on enhanced features
    tests = [
        ("Enhanced PageRank Analysis", tester.test_enhanced_pagerank_analysis),
        ("Betweenness Centrality Connectors", tester.test_betweenness_centrality_connectors),
        ("Statistical Outlier Detection", tester.test_statistical_outlier_detection),
        ("Formal vs Informal Leaders", tester.test_formal_vs_informal_leaders)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print(f"\n{'='*60}")
    print(f"📊 Enhanced Analysis Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All enhanced analysis tests passed!")
        return 0
    else:
        print("⚠️  Some enhanced analysis tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())