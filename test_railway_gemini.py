#!/usr/bin/env python3
"""
Test script to verify Gemini API is working on Railway
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test if Gemini API is working"""
    print("🔍 Testing Gemini API configuration...")
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("💡 Make sure to add GEMINI_API_KEY in Railway Variables tab")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Generate 1 BCS-style MCQ question about Bangladesh Civil Service. Format as JSON with question, options (A-D), correct_answer, and explanation.")
        
        print("✅ Gemini API test successful!")
        print(f"📝 Response preview: {response.text[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api() 