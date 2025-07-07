#!/usr/bin/env python3
"""
Test script for Bangla PDF parsing functionality
"""

import os
import sys
from file_handler import FileHandler
from text_processor import TextProcessor

def test_bangla_pdf_parsing():
    """Test Bangla PDF parsing with sample files"""
    
    print("🧪 Testing Bangla PDF Parsing Functionality")
    print("=" * 50)
    
    # Initialize components
    file_handler = FileHandler()
    text_processor = TextProcessor()
    
    # Check if uploads directory exists and has PDF files
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        print("❌ Uploads directory not found. Please upload a PDF file first.")
        return
    
    # Find PDF files in uploads directory
    pdf_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in uploads directory.")
        print("Please upload a PDF file with Bangla text to test.")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF file(s) in uploads directory")
    
    # Test each PDF file
    for pdf_file in pdf_files:
        filepath = os.path.join(uploads_dir, pdf_file)
        print(f"\n📄 Testing file: {pdf_file}")
        print("-" * 30)
        
        try:
            # Extract text from PDF
            print("🔍 Extracting text from PDF...")
            extracted_text = file_handler.extract_text(filepath)
            
            if not extracted_text:
                print("❌ No text extracted from PDF")
                continue
            
            print(f"✅ Successfully extracted {len(extracted_text)} characters")
            
            # Check for Bangla characters
            bangla_chars = [char for char in extracted_text if '\u0980' <= char <= '\u09FF']
            if bangla_chars:
                print(f"✅ Found {len(bangla_chars)} Bangla characters")
                print(f"📝 Sample Bangla text: {extracted_text[:200]}...")
            else:
                print("⚠️  No Bangla characters detected in extracted text")
                print(f"📝 Sample text: {extracted_text[:200]}...")
            
            # Process text
            print("🔧 Processing extracted text...")
            processed_text = text_processor.process_text(extracted_text)
            
            print(f"✅ Processed text length: {len(processed_text)} characters")
            
            # Extract key concepts
            print("🔍 Extracting key concepts...")
            concepts = text_processor.extract_key_concepts(processed_text, max_concepts=10)
            
            if concepts:
                print(f"✅ Found {len(concepts)} key concepts:")
                for i, concept in enumerate(concepts[:5], 1):
                    print(f"   {i}. {concept}")
            else:
                print("⚠️  No key concepts extracted")
            
            # Split into chunks
            print("📦 Splitting text into chunks...")
            chunks = text_processor.split_into_chunks(processed_text, chunk_size=500)
            
            print(f"✅ Created {len(chunks)} text chunks")
            if chunks:
                print(f"📝 First chunk preview: {chunks[0][:100]}...")
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Bangla PDF parsing test completed!")

def test_unicode_support():
    """Test Unicode support for Bangla characters"""
    
    print("\n🔤 Testing Unicode Support for Bangla")
    print("=" * 40)
    
    # Sample Bangla text
    bangla_text = """
    বাংলাদেশ একটি দক্ষিণ এশীয় দেশ। এটি বিশ্বের সবচেয়ে জনবহুল দেশগুলির মধ্যে একটি।
    বাংলাদেশের রাজধানী ঢাকা। বাংলা ভাষা এখানকার প্রধান ভাষা।
    """
    
    print("📝 Sample Bangla text:")
    print(bangla_text)
    
    # Test text processor
    text_processor = TextProcessor()
    
    try:
        processed_text = text_processor.process_text(bangla_text)
        print(f"✅ Text processing successful: {len(processed_text)} characters")
        
        concepts = text_processor.extract_key_concepts(processed_text)
        print(f"✅ Key concepts extracted: {len(concepts)}")
        
        chunks = text_processor.split_into_chunks(processed_text)
        print(f"✅ Text chunks created: {len(chunks)}")
        
        print("✅ Unicode support test passed!")
        
    except Exception as e:
        print(f"❌ Unicode support test failed: {str(e)}")

if __name__ == "__main__":
    test_unicode_support()
    test_bangla_pdf_parsing() 