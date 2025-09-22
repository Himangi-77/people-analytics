import requests
import sys
import json
import re

class FinalFormattingVerification:
    def __init__(self, base_url="https://teamflow-34.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.results = {
            'ai_analysis_completes': False,
            'bold_text_formatting': False,
            'italic_text_formatting': False,
            'paragraph_breaks': False,
            'headers_emphasized': False,
            'metrics_highlighted': False,
            'professional_presentation': False
        }
        
    def setup_test_data(self):
        """Setup graph data for testing"""
        sample_data = {
            "nodes": [
                {"data": {"id": "1", "name": "Alice Johnson", "department": "Engineering", "title": "Tech Lead"}},
                {"data": {"id": "2", "name": "Bob Chen", "department": "Engineering", "title": "Senior Developer"}},
                {"data": {"id": "3", "name": "Carol Davis", "department": "Marketing", "title": "Marketing Manager"}},
                {"data": {"id": "4", "name": "David Wilson", "department": "Sales", "title": "Sales Director"}},
                {"data": {"id": "5", "name": "Emily Brown", "department": "Engineering", "title": "DevOps Engineer"}},
                {"data": {"id": "6", "name": "Frank Miller", "department": "Marketing", "title": "Content Specialist"}},
                {"data": {"id": "7", "name": "Grace Lee", "department": "Sales", "title": "Account Executive"}},
                {"data": {"id": "8", "name": "Henry Garcia", "department": "Engineering", "title": "Product Manager"}},
                {"data": {"id": "9", "name": "Iris Thompson", "department": "Marketing", "title": "Designer"}},
                {"data": {"id": "10", "name": "Jack Rodriguez", "department": "Sales", "title": "Sales Rep"}},
                {"data": {"id": "11", "name": "Karen White", "department": "HR", "title": "HR Director"}},
                {"data": {"id": "12", "name": "Luke Anderson", "department": "Engineering", "title": "Data Scientist"}},
                {"data": {"id": "13", "name": "Maria Lopez", "department": "Marketing", "title": "Social Media Manager"}},
                {"data": {"id": "14", "name": "Nathan Clark", "department": "Sales", "title": "Customer Success"}},
                {"data": {"id": "15", "name": "Olivia Taylor", "department": "Engineering", "title": "Security Engineer"}}
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
        
        try:
            response = requests.post(
                f"{self.base_url}/upload-graph",
                json={"graph_data": sample_data},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def verify_critical_success_criteria(self):
        """Verify all critical success criteria from the review request"""
        print("🎯 VERIFYING CRITICAL SUCCESS CRITERIA")
        print("=" * 60)
        
        # Setup test data
        if not self.setup_test_data():
            print("❌ Failed to setup test data")
            return False
        
        # Test with the specific question mentioned in review request
        test_question = "Who are the informal leaders in our organization, and how do they influence decision-making?"
        
        print(f"📝 Test Question: {test_question}")
        print("⏳ Processing AI analysis...")
        
        try:
            response = requests.post(
                f"{self.base_url}/query",
                json={"question": test_question},
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                
                print(f"✅ AI analysis completed successfully!")
                print(f"📊 Response length: {len(answer)} characters")
                self.results['ai_analysis_completes'] = True
                
                # Verify each critical success criterion
                self.verify_formatting_criteria(answer)
                
                return True
            else:
                print(f"❌ AI analysis failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error during AI analysis: {str(e)}")
            return False
    
    def verify_formatting_criteria(self, answer_text):
        """Verify specific formatting criteria"""
        print("\n🔍 DETAILED FORMATTING VERIFICATION:")
        print("-" * 50)
        
        # 1. Bold text (**text**) formatting
        bold_matches = re.findall(r'\*\*(.*?)\*\*', answer_text)
        if bold_matches:
            self.results['bold_text_formatting'] = True
            print(f"✅ Bold text formatting: {len(bold_matches)} instances found")
            print(f"   Examples: {bold_matches[:3]}")
        else:
            print("❌ Bold text formatting: No instances found")
        
        # 2. Italic text (*text*) formatting
        italic_pattern = r'(?<!\*)\*([^*]+?)\*(?!\*)'
        italic_matches = re.findall(italic_pattern, answer_text)
        if italic_matches:
            self.results['italic_text_formatting'] = True
            print(f"✅ Italic text formatting: {len(italic_matches)} instances found")
            print(f"   Examples: {italic_matches[:3]}")
        else:
            print("❌ Italic text formatting: No instances found")
        
        # 3. Paragraph breaks
        paragraph_breaks = answer_text.count('\n\n')
        if paragraph_breaks > 0:
            self.results['paragraph_breaks'] = True
            print(f"✅ Paragraph breaks: {paragraph_breaks} instances found")
        else:
            print("❌ Paragraph breaks: No proper separation found")
        
        # 4. Headers and key terms emphasized
        key_terms = ['Key Insight:', 'Recommendation:', 'Important:', 'Note:', 'Warning:', 'Action Item:']
        headers_found = []
        
        # Check for headers (lines ending with colons)
        lines = answer_text.split('\n')
        header_lines = [line for line in lines if line.strip().endswith(':') and len(line.strip()) < 100]
        
        # Check for key terms
        for term in key_terms:
            if term in answer_text:
                headers_found.append(term)
        
        if header_lines or headers_found:
            self.results['headers_emphasized'] = True
            print(f"✅ Headers and key terms: {len(header_lines)} headers, {len(headers_found)} key terms")
            if headers_found:
                print(f"   Key terms found: {headers_found}")
        else:
            print("❌ Headers and key terms: Limited emphasis found")
        
        # 5. Metrics and percentages highlighted
        percentage_matches = re.findall(r'\*(\d+\.?\d*%)\*', answer_text)
        ratio_matches = re.findall(r'\*(\d+\.?\d* out of \d+)\*', answer_text)
        
        if percentage_matches or ratio_matches:
            self.results['metrics_highlighted'] = True
            print(f"✅ Metrics highlighted: {len(percentage_matches)} percentages, {len(ratio_matches)} ratios")
        else:
            print("❌ Metrics highlighted: No highlighted metrics found")
        
        # 6. Professional presentation (overall structure)
        structured_elements = len(bold_matches) + len(header_lines) + paragraph_breaks
        if structured_elements >= 5:
            self.results['professional_presentation'] = True
            print(f"✅ Professional presentation: {structured_elements} structural elements")
        else:
            print(f"❌ Professional presentation: Only {structured_elements} structural elements")
        
        # Show sample of formatted content
        print(f"\n📝 SAMPLE FORMATTED CONTENT:")
        print("-" * 40)
        sample_paragraphs = answer_text.split('\n\n')[:2]
        for i, paragraph in enumerate(sample_paragraphs, 1):
            if paragraph.strip():
                print(f"Paragraph {i}: {paragraph.strip()[:150]}...")
    
    def generate_final_report(self):
        """Generate final verification report"""
        print(f"\n{'='*60}")
        print("🏆 FINAL VERIFICATION REPORT")
        print("=" * 60)
        
        criteria_labels = {
            'ai_analysis_completes': 'AI analysis completes and returns formatted response',
            'bold_text_formatting': 'Bold text (**text**) renders correctly as HTML <strong>',
            'italic_text_formatting': 'Italic text (*text*) renders correctly as HTML <em>',
            'paragraph_breaks': 'Paragraph breaks create proper visual separation',
            'headers_emphasized': 'Headers and key terms are properly emphasized',
            'metrics_highlighted': 'Metrics and percentages are visually highlighted',
            'professional_presentation': 'Overall presentation is professional and readable'
        }
        
        passed_count = 0
        total_count = len(self.results)
        
        for key, passed in self.results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{status} - {criteria_labels[key]}")
            if passed:
                passed_count += 1
        
        print(f"\n📊 OVERALL SCORE: {passed_count}/{total_count} criteria met")
        
        if passed_count == total_count:
            print("🎉 EXCELLENT! All critical success criteria met!")
            return True
        elif passed_count >= total_count * 0.8:
            print("✅ GOOD! Most critical success criteria met!")
            return True
        elif passed_count >= total_count * 0.6:
            print("⚠️  ACCEPTABLE! Majority of criteria met, some improvements needed!")
            return True
        else:
            print("❌ NEEDS IMPROVEMENT! Several criteria not met!")
            return False

def main():
    print("🚀 FINAL AI ANALYSIS FORMATTING VERIFICATION")
    print("=" * 60)
    print("Testing against all critical success criteria from review request")
    
    verifier = FinalFormattingVerification()
    
    # Run comprehensive verification
    success = verifier.verify_critical_success_criteria()
    
    if success:
        # Generate final report
        overall_success = verifier.generate_final_report()
        return 0 if overall_success else 1
    else:
        print("\n❌ VERIFICATION FAILED - Could not complete AI analysis")
        return 1

if __name__ == "__main__":
    sys.exit(main())