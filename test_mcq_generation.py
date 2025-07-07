#!/usr/bin/env python3
"""
Test script for MCQ generation
"""

import os
from dotenv import load_dotenv
from gemini_mcq_generator import GeminiMCQGenerator

# Load environment variables
load_dotenv()

def test_mcq_generation():
    """Test MCQ generation with sample text"""
    
    # Sample text for testing
    sample_text = """
    The Bangladesh Civil Service (BCS) is the civil service of Bangladesh. It originated from the Indian Civil Service (ICS) 
    and was established after the independence of Bangladesh in 1971. The BCS examination is conducted by the Bangladesh 
    Public Service Commission (BPSC) to recruit civil servants for various government departments and ministries.
    
    The BCS examination consists of three stages: Preliminary Examination, Written Examination, and Viva Voce. 
    The preliminary examination consists of 200 multiple choice questions covering various subjects including 
    languages, general knowledge, and technical subjects. Candidates who pass the preliminary examination 
    are eligible to sit for the written examination, which consists of subjective questions.
    
    The BCS is divided into several cadres, each responsible for different aspects of government administration. 
    These include the Administrative Cadre, Police Cadre, Foreign Service Cadre, and various technical cadres. 
    Each cadre has specific responsibilities and career progression paths.
    
    The BCS examination is highly competitive, with thousands of candidates appearing each year for a limited 
    number of positions. The examination process is designed to select the most qualified candidates based on 
    their knowledge, skills, and aptitude for public service.
    """
    
    print("🧪 Testing MCQ Generation...")
    print("=" * 50)
    
    # Initialize generator
    generator = GeminiMCQGenerator()
    
    # Test with different numbers of questions
    test_cases = [5, 10, 15]
    
    for num_questions in test_cases:
        print(f"\n📝 Testing with {num_questions} questions:")
        print("-" * 30)
        
        try:
            questions = generator.generate_questions(sample_text, num_questions, "medium")
            
            if questions:
                print(f"✅ Successfully generated {len(questions)} questions")
                
                # Display first question as example
                if len(questions) > 0:
                    first_q = questions[0]
                    print(f"\n📋 Sample Question:")
                    print(f"Q: {first_q['question']}")
                    for i, option in enumerate(first_q['options']):
                        print(f"   {option}")
                    print(f"Correct Answer: {first_q['correct_answer']}")
                    print(f"Explanation: {first_q['explanation']}")
            else:
                print("❌ No questions generated")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_mcq_generation() 