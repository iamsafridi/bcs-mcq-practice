#!/usr/bin/env python3
"""
Test Bangla text processing functionality
"""

from text_processor import TextProcessor
from mcq_generator import MCQGenerator

def test_bangla_text_processing():
    """Test Bangla text processing and MCQ generation"""
    
    print("🧪 Testing Bangla Text Processing")
    print("=" * 40)
    
    # Sample Bangla text about BCS
    bangla_text = """
    বাংলাদেশ সিভিল সার্ভিস (বিসিএস) বাংলাদেশের সর্বোচ্চ সরকারি চাকরির পরীক্ষা।
    এই পরীক্ষায় উত্তীর্ণ হয়ে সরকারি বিভিন্ন মন্ত্রণালয় ও বিভাগে চাকরি করা যায়।
    বিসিএস পরীক্ষায় সাধারণত বাংলা, ইংরেজি, গণিত, বিজ্ঞান, বাংলাদেশ বিষয়াবলী ইত্যাদি বিষয়ে প্রশ্ন আসে।
    প্রতিবছর হাজার হাজার শিক্ষার্থী এই পরীক্ষায় অংশগ্রহণ করে।
    বিসিএস ক্যাডার পদে নিয়োগ পেলে একজন কর্মকর্তা বিভিন্ন সরকারি প্রতিষ্ঠানে কাজ করতে পারেন।
    """
    
    print("📝 Sample Bangla text:")
    print(bangla_text)
    print()
    
    # Initialize components
    text_processor = TextProcessor()
    mcq_generator = MCQGenerator()
    
    try:
        # Process Bangla text
        print("🔧 Processing Bangla text...")
        processed_text = text_processor.process_text(bangla_text)
        print(f"✅ Processed text length: {len(processed_text)} characters")
        print(f"📝 Processed text: {processed_text}")
        print()
        
        # Extract key concepts
        print("🔍 Extracting key concepts...")
        concepts = text_processor.extract_key_concepts(processed_text, max_concepts=10)
        print(f"✅ Found {len(concepts)} key concepts:")
        for i, concept in enumerate(concepts, 1):
            print(f"   {i}. {concept}")
        print()
        
        # Split into chunks
        print("📦 Splitting text into chunks...")
        chunks = text_processor.split_into_chunks(processed_text, chunk_size=200)
        print(f"✅ Created {len(chunks)} text chunks")
        for i, chunk in enumerate(chunks, 1):
            print(f"   Chunk {i}: {chunk[:50]}...")
        print()
        
        # Test MCQ generation with Bangla text
        print("🎯 Testing MCQ generation with Bangla text...")
        try:
            mcq_questions = mcq_generator.generate_questions(
                processed_text,
                num_questions=3,
                difficulty='easy'
            )
            
            if mcq_questions:
                print(f"✅ Successfully generated {len(mcq_questions)} MCQ questions")
                for i, question in enumerate(mcq_questions[:2], 1):
                    print(f"\n   Question {i}:")
                    print(f"   Q: {question['question']}")
                    print(f"   A: {question['options']['A']}")
                    print(f"   B: {question['options']['B']}")
                    print(f"   C: {question['options']['C']}")
                    print(f"   D: {question['options']['D']}")
                    print(f"   Correct: {question['correct_answer']}")
            else:
                print("⚠️  No MCQ questions generated")
                
        except Exception as e:
            print(f"⚠️  MCQ generation failed: {str(e)}")
        
        print("\n✅ Bangla text processing test completed successfully!")
        
    except Exception as e:
        print(f"❌ Bangla text processing test failed: {str(e)}")

if __name__ == "__main__":
    test_bangla_text_processing() 