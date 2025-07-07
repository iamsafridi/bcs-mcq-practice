#!/usr/bin/env python3
"""
Test language detection for Bangla text
"""

def test_language_detection():
    """Test the improved language detection logic"""
    
    # Improved language detection function from gemini_mcq_generator.py
    def is_bangla(text):
        bangla_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
        total_chars = len([c for c in text if c.isalpha() or '\u0980' <= c <= '\u09FF'])
        
        if total_chars == 0:
            return False
        
        bangla_ratio = bangla_chars / total_chars
        
        # More sensitive detection: if more than 15% of alphabetic characters are Bangla
        return bangla_ratio > 0.15 or bangla_chars > 5
    
    # Test cases
    test_cases = [
        {
            "name": "Pure Bangla text",
            "text": "বাংলাদেশ সিভিল সার্ভিস (বিসিএস) বাংলাদেশের সর্বোচ্চ সরকারি চাকরির পরীক্ষা।",
            "expected": True
        },
        {
            "name": "Mixed Bangla-English text",
            "text": "বাংলাদেশ সিভিল সার্ভিস (BCS) is the highest government job examination in Bangladesh.",
            "expected": True
        },
        {
            "name": "English text",
            "text": "BCS is the highest government job examination in Bangladesh.",
            "expected": False
        },
        {
            "name": "Short Bangla text",
            "text": "বিসিএস পরীক্ষা",
            "expected": True
        },
        {
            "name": "Bangla with numbers and symbols",
            "text": "বিসিএস পরীক্ষায় 200টি প্রশ্ন থাকে। (BCS exam has 200 questions.)",
            "expected": True
        }
    ]
    
    print("🧪 Testing Improved Language Detection Logic")
    print("=" * 50)
    
    for test_case in test_cases:
        result = is_bangla(test_case["text"])
        status = "✅" if result == test_case["expected"] else "❌"
        print(f"{status} {test_case['name']}: {result} (expected: {test_case['expected']})")
        print(f"   Text: {test_case['text'][:50]}...")
        print(f"   Total length: {len(test_case['text'])} chars")
        bangla_chars = sum(1 for c in test_case['text'] if '\u0980' <= c <= '\u09FF')
        total_alpha = len([c for c in test_case['text'] if c.isalpha() or '\u0980' <= c <= '\u09FF'])
        print(f"   Bangla chars: {bangla_chars}")
        print(f"   Total alphabetic chars: {total_alpha}")
        if total_alpha > 0:
            print(f"   Bangla ratio: {bangla_chars/total_alpha:.2f}")
        print()

if __name__ == "__main__":
    test_language_detection() 