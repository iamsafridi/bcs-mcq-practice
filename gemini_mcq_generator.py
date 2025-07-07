import os
import json
import random
import re
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiMCQGenerator:
    """Simple BCS MCQ Generator using Google Gemini AI"""
    
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found. Using fallback MCQ generation.")
            self.use_gemini = False
        else:
            genai.configure(api_key=api_key)
            self.use_gemini = True
            print("✅ Gemini MCQ Generator initialized!")
        
        # Fallback questions for when AI is not available
        self.fallback_questions = [
            {
                "question": "What is the main topic discussed in the provided text?",
                "options": ["A) General information", "B) Specific details", "C) Technical concepts", "D) Historical facts"],
                "correct_answer": "A",
                "explanation": "The text contains general information about the topic."
            },
            {
                "question": "Which of the following is most likely to be true based on the text?",
                "options": ["A) The topic is simple", "B) The topic is complex", "C) The topic is irrelevant", "D) The topic is outdated"],
                "correct_answer": "B",
                "explanation": "Most educational content contains complex concepts."
            }
        ]
    
    def generate_questions(self, text: str, num_questions: int = 10, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """
        Generate MCQ questions from text content
        """
        if not text:
            print("No text provided, using fallback questions")
            return self.fallback_questions[:num_questions]
        
        print(f"Generating {num_questions} questions from text of length {len(text)}")
        
        if self.use_gemini:
            try:
                questions = self._generate_with_gemini(text, num_questions, difficulty)
                if questions and len(questions) > 0:
                    print(f"Successfully generated {len(questions)} questions with Gemini")
                    return questions[:num_questions]
                else:
                    print("Gemini failed to generate questions, using fallback")
                    return self._generate_fallback_questions(text, num_questions)
            except Exception as e:
                print(f"Gemini error: {str(e)}")
                return self._generate_fallback_questions(text, num_questions)
        else:
            print("Gemini not available, using fallback generation")
            return self._generate_fallback_questions(text, num_questions)
    
    def _generate_with_gemini(self, text: str, num_questions: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate questions using Gemini AI"""
        # Improved language detection
        def is_bangla(text):
            bangla_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
            total_chars = len([c for c in text if c.isalpha() or '\u0980' <= c <= '\u09FF'])
            
            if total_chars == 0:
                return False
            
            bangla_ratio = bangla_chars / total_chars
            
            # More sensitive detection: if more than 15% of alphabetic characters are Bangla
            return bangla_ratio > 0.15 or bangla_chars > 5
        
        is_bangla_text = is_bangla(text)
        bangla_char_count = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
        print(f"Language detection: {'Bangla' if is_bangla_text else 'English'} (Bangla chars: {bangla_char_count})")
        
        if is_bangla_text:
            language_instruction = """
            IMPORTANT: Generate all questions, options, and explanations in Bangla (বাংলা ভাষা).
            Use proper Bangla grammar and vocabulary.
            Questions should be in Bangla format like: "বিসিএস পরীক্ষায় কোন বিষয় অন্তর্ভুক্ত?"
            Options should be in Bangla like: "ক) বাংলা ভাষা খ) ইংরেজি ভাষা গ) গণিত ঘ) বিজ্ঞান"
            """
        else:
            language_instruction = "Generate questions in English."
        
        # Improved prompt with better instructions
        prompt = f"""
        Generate exactly {num_questions} multiple choice questions based on the following text. 
        {language_instruction}
        
        Text: {text[:3000]}{"..." if len(text) > 3000 else ""}
        
        Instructions:
        1. Create questions that test understanding of the content
        2. Each question must have exactly 4 options (A, B, C, D)
        3. Only one option should be correct
        4. Make options realistic and plausible
        5. Provide clear explanations for correct answers
        6. Maintain the same language as the input text
        
        Format each question exactly as:
        {{
            "question": "Question text here?",
            "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
            "correct_answer": "A",
            "explanation": "Brief explanation of why this answer is correct."
        }}
        
        Return ONLY a valid JSON array of questions. Do not include any other text.
        """
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            print(f"Gemini response length: {len(response.text)}")
            print(f"Response preview: {response.text[:200]}...")
            
            # Parse response with multiple strategies
            questions = self._parse_gemini_response(response.text)
            
            if questions:
                print(f"Successfully parsed {len(questions)} questions from Gemini")
                return questions
            else:
                print("Failed to parse Gemini response, using fallback")
                return []
                
        except Exception as e:
            print(f"Error generating with Gemini: {str(e)}")
            return []
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse Gemini response with multiple fallback strategies"""
        # Strategy 1: Look for JSON array
        if '[' in response_text and ']' in response_text:
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            json_str = response_text[start:end]
            
            try:
                questions = json.loads(json_str)
                if isinstance(questions, list) and len(questions) > 0:
                    valid_questions = []
                    for q in questions:
                        if self._validate_question_format(q):
                            valid_questions.append(q)
                    if valid_questions:
                        return valid_questions
            except json.JSONDecodeError:
                print("JSON parsing failed, trying alternative parsing")
        
        # Strategy 2: Look for individual question blocks
        questions = []
        question_pattern = r'\{[^{}]*"question"[^{}]*\}'
        matches = re.findall(question_pattern, response_text, re.DOTALL)
        
        for match in matches:
            try:
                question = json.loads(match)
                if self._validate_question_format(question):
                    questions.append(question)
            except json.JSONDecodeError:
                continue
        
        if questions:
            return questions
        
        # Strategy 3: Manual parsing for simple cases
        return self._manual_parse_questions(response_text)
    
    def _manual_parse_questions(self, response_text: str) -> List[Dict[str, Any]]:
        """Manual parsing for simple question formats"""
        questions = []
        lines = response_text.split('\n')
        
        current_question = None
        current_options = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for question patterns
            if line.startswith('Q') or line.startswith('Question') or '?' in line:
                if current_question and current_options:
                    # Save previous question
                    question = self._create_question_from_parts(current_question, current_options)
                    if question:
                        questions.append(question)
                
                current_question = line
                current_options = []
            
            # Look for option patterns
            elif line.startswith('A)') or line.startswith('B)') or line.startswith('C)') or line.startswith('D)'):
                current_options.append(line)
        
        # Add last question
        if current_question and current_options:
            question = self._create_question_from_parts(current_question, current_options)
            if question:
                questions.append(question)
        
        return questions
    
    def _create_question_from_parts(self, question_text: str, options: List[str]) -> Dict[str, Any]:
        """Create a question from manually parsed parts"""
        if len(options) != 4:
            return None
        
        # Clean question text
        question_text = re.sub(r'^Q\d*\.?\s*', '', question_text)
        question_text = re.sub(r'^Question\s*\d*\.?\s*', '', question_text)
        
        # Clean options
        cleaned_options = []
        for option in options:
            option = option.strip()
            if option.startswith('A)') or option.startswith('B)') or option.startswith('C)') or option.startswith('D)'):
                cleaned_options.append(option)
        
        if len(cleaned_options) != 4:
            return None
        
        return {
            "question": question_text,
            "options": cleaned_options,
            "correct_answer": "A",  # Default to A
            "explanation": "This answer is correct based on the provided text."
        }
    
    def _validate_question_format(self, question: Dict[str, Any]) -> bool:
        """Validate question format with relaxed requirements"""
        # Check required fields
        if not isinstance(question, dict):
            return False
        
        if 'question' not in question or not question['question']:
            return False
        
        if 'options' not in question or not isinstance(question['options'], list):
            return False
        
        if 'correct_answer' not in question:
            return False
        
        # Validate options (relaxed)
        if len(question['options']) < 2:  # Allow at least 2 options
            return False
        
        # Validate correct answer (relaxed)
        correct = question['correct_answer']
        if not isinstance(correct, str) or len(correct) == 0:
            return False
        
        # If correct answer is A, B, C, D, validate it exists in options
        if correct in ['A', 'B', 'C', 'D']:
            option_index = ord(correct) - ord('A')
            if option_index >= len(question['options']):
                return False
        
        return True
    
    def _generate_fallback_questions(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Generate fallback questions from text content"""
        print(f"Generating {num_questions} fallback questions")
        questions = []
        
        # Extract information from text
        facts = self._extract_facts_from_text(text)
        concepts = self._extract_important_concepts(text)
        dates = self._extract_dates(text)
        numbers = self._extract_numbers(text)
        
        print(f"Extracted: {len(facts)} facts, {len(concepts)} concepts, {len(dates)} dates, {len(numbers)} numbers")
        
        # Generate different types of questions
        for i in range(num_questions):
            question = None
            
            if facts and i % 4 == 0:
                question = self._create_fact_based_question(facts, text)
            elif concepts and i % 4 == 1:
                concept = concepts[i % len(concepts)] if i < len(concepts) else random.choice(concepts)
                question = self._create_concept_question(concept, text)
            elif dates and i % 4 == 2:
                question = self._create_date_question(dates, text)
            elif numbers and i % 4 == 3:
                question = self._create_number_question(numbers, text)
            else:
                question = self._create_generic_question(text)
            
            if question and question not in questions:
                questions.append(question)
                print(f"Added question {len(questions)}: {question['question'][:50]}...")
        
        # If still not enough, add generic questions
        while len(questions) < num_questions:
            question = self._create_generic_question(text)
            if question and question not in questions:
                questions.append(question)
                print(f"Added generic question {len(questions)}")
        
        print(f"Generated {len(questions)} fallback questions")
        return questions[:num_questions]
    
    def _extract_important_concepts(self, text: str) -> List[str]:
        """Extract important concepts from text"""
        # Remove common words and get meaningful terms
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'as', 'from', 'not', 'no', 'yes', 'so', 'if', 'then', 'else', 'when', 'where', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose'}
        
        words = text.lower().split()
        word_freq = {}
        
        for word in words:
            # Clean word (remove punctuation)
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 4 and clean_word not in common_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Get most frequent words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:15]]
    
    def _extract_facts_from_text(self, text: str) -> List[str]:
        """Extract factual statements from text"""
        sentences = text.split('.')
        facts = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                # Look for factual statements
                if any(keyword in sentence.lower() for keyword in ['is', 'are', 'was', 'were', 'consists', 'includes', 'contains', 'established', 'created', 'formed']):
                    facts.append(sentence)
        
        return facts[:10]  # Limit to 10 facts
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_pattern = r'\b(19|20)\d{2}\b'
        dates = re.findall(date_pattern, text)
        return list(set(dates))
    
    def _extract_numbers(self, text: str) -> List[str]:
        """Extract important numbers from text"""
        number_pattern = r'\b\d+\b'
        numbers = re.findall(number_pattern, text)
        # Filter out common non-important numbers
        important_numbers = [num for num in numbers if int(num) > 10]
        return list(set(important_numbers))
    
    def _create_fact_based_question(self, facts: List[str], text: str) -> Dict[str, Any]:
        """Create question based on factual statements"""
        if not facts:
            return None
        
        fact = random.choice(facts)
        question_text = "Which of the following statements is correct according to the text?"
        
        options = [
            f"A) {fact[:80]}...",
            "B) The opposite of what is stated in the text",
            "C) Information not mentioned in the text",
            "D) A different interpretation of the text"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"This fact is directly stated in the text: {fact}"
        }
    
    def _create_concept_question(self, concept: str, text: str) -> Dict[str, Any]:
        """Create a question based on a concept"""
        question_text = f"Which statement best describes the role of {concept} according to the provided text?"
        
        options = [
            f"A) {concept} plays an important role as mentioned in the text",
            f"B) {concept} is not discussed in the text",
            f"C) {concept} is only briefly mentioned",
            f"D) {concept} has no significance in the context"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"The text discusses {concept} in detail, indicating its importance in the context."
        }
    
    def _create_date_question(self, dates: List[str], text: str) -> Dict[str, Any]:
        """Create question about dates"""
        if not dates:
            return None
        
        date = random.choice(dates)
        question_text = f"What significant event occurred in {date}?"
        
        options = [
            f"A) An important development in {date}",
            f"B) No significant event in {date}",
            f"C) A different year was more important",
            f"D) The text doesn't mention {date}"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"The text mentions {date} as an important year."
        }
    
    def _create_number_question(self, numbers: List[str], text: str) -> Dict[str, Any]:
        """Create question about numbers"""
        if not numbers:
            return None
        
        number = random.choice(numbers)
        question_text = f"What does the number {number} represent in the text?"
        
        options = [
            f"A) An important quantity mentioned in the text",
            f"B) A random number",
            f"C) A different number is more important",
            f"D) The text doesn't mention {number}"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"The number {number} is mentioned as an important figure in the text."
        }
    
    def _create_generic_question(self, text: str) -> Dict[str, Any]:
        """Create a generic but relevant question"""
        question_text = "What is the main topic discussed in the provided text?"
        
        options = [
            "A) The primary subject matter of the text",
            "B) A secondary topic mentioned briefly",
            "C) An unrelated topic not discussed",
            "D) A topic that contradicts the main content"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": "This information is directly stated in the text."
        } 