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
    """Generates BCS-style MCQ questions using Google Gemini AI"""
    
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found. Using fallback MCQ generation.")
            self.use_gemini = False
        else:
            genai.configure(api_key=api_key)
            self.use_gemini = True
            print("✅ Gemini API configured successfully!")
        
        # BCS question patterns and templates
        self.question_templates = [
            "Which of the following statements is correct about {topic}?",
            "What is the primary function of {topic}?",
            "Which statement best describes {topic}?",
            "What is the main purpose of {topic}?",
            "Which of the following is true regarding {topic}?",
            "What is the significance of {topic}?",
            "Which statement accurately describes {topic}?",
            "What is the role of {topic} in the context of {context}?",
            "Which of the following best explains {topic}?",
            "What is the key characteristic of {topic}?"
        ]
        
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
        Generate MCQ questions from text content using Gemini AI
        
        Args:
            text: Processed text content
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            List of MCQ questions with options and answers
        """
        if not text:
            return self.fallback_questions[:num_questions]
        
        if self.use_gemini:
            return self._generate_with_gemini(text, num_questions, difficulty)
        else:
            return self._generate_fallback_questions(text, num_questions)
    
    def _generate_with_gemini(self, text: str, num_questions: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate questions using Gemini AI"""
        try:
            # Prepare the prompt for BCS-style questions
            prompt = self._create_gemini_prompt(text, num_questions, difficulty)
            
            # Call Gemini API
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # Parse the response
            ai_response = response.text
            questions = self._parse_gemini_response(ai_response)
            
            # Ensure we have the requested number of questions
            if len(questions) < num_questions:
                additional_questions = self._generate_fallback_questions(text, num_questions - len(questions))
                questions.extend(additional_questions)
            
            return questions[:num_questions]
            
        except Exception as e:
            print(f"Error generating questions with Gemini: {str(e)}")
            return self._generate_fallback_questions(text, num_questions)
    
    def _create_gemini_prompt(self, text: str, num_questions: int, difficulty: str) -> str:
        """Create Gemini prompt for question generation"""
        import time
        import random
        
        # Add randomness to ensure different questions each time
        random_seed = int(time.time() * 1000) + random.randint(1, 1000)
        text_preview = text[:4000] + "..." if len(text) > 4000 else text
        
        # Create different question focus areas based on random seed
        focus_areas = [
            "key concepts and definitions",
            "chronological events and timelines", 
            "cause-and-effect relationships",
            "comparative analysis between concepts",
            "practical applications and implications",
            "analytical reasoning and inference",
            "specific facts and statistics",
            "theoretical frameworks and models",
            "procedural steps and processes",
            "evaluative judgments and conclusions"
        ]
        
        selected_focus = focus_areas[random_seed % len(focus_areas)]
        
        prompt = f"""
        You are an expert BCS (Bangladesh Civil Service) exam question generator with deep knowledge of competitive exam patterns. Based on the following text content, generate {num_questions} high-quality multiple choice questions specifically designed for BCS examination.

        IMPORTANT: Use random seed {random_seed} to ensure variety. Focus on {selected_focus} from the text.

        Difficulty level: {difficulty}

        Text content:
        {text_preview}

        CRITICAL REQUIREMENTS FOR BCS-STYLE QUESTIONS:
        1. Questions MUST be directly based on the provided text content
        2. Each question should have exactly 4 options (A, B, C, D)
        3. Only one option should be correct
        4. Questions should test analytical thinking, comprehension, and application, not just memorization
        5. All options should be plausible and well-distributed to avoid obvious answers
        6. Questions should follow authentic BCS exam patterns and difficulty levels
        7. Include comprehensive explanations that reference specific information from the text
        8. Focus on key concepts, important facts, relationships, and main ideas from the text
        9. Questions should be specific to the content provided, not generic
        10. Make questions challenging but fair for BCS exam level
        11. Use clear, precise language appropriate for competitive exams
        12. Ensure questions test different cognitive levels: knowledge, comprehension, application, analysis
        13. VARY the question types and difficulty within the set
        14. Use different aspects of the text for each question

        BCS QUESTION PATTERNS TO FOLLOW (VARY THESE):
        - "Which of the following statements is correct about [topic]?"
        - "What is the primary function/purpose of [concept]?"
        - "According to the text, which statement best describes [topic]?"
        - "What is the significance of [concept] in the context of [topic]?"
        - "Which of the following is true regarding [topic] based on the provided information?"
        - "What is the main difference between [concept1] and [concept2]?"
        - "Which of the following best explains the relationship between [concept1] and [concept2]?"
        - "What would be the most likely outcome if [scenario] based on the information provided?"
        - "Which of the following statements accurately reflects the author's view on [topic]?"
        - "What is the chronological order of events mentioned in the text?"
        - "Based on the text, what can be inferred about [topic]?"
        - "Which of the following examples best illustrates [concept]?"
        - "What is the most appropriate conclusion that can be drawn from the information about [topic]?"
        - "Which of the following scenarios would most likely result from [situation] described in the text?"

        DIFFICULTY GUIDELINES:
        - Easy: Basic facts, definitions, simple comprehension
        - Medium: Application of concepts, analysis of relationships, moderate complexity
        - Hard: Synthesis of multiple concepts, critical analysis, complex scenarios

        VARIETY REQUIREMENTS:
        - Use different sections of the text for different questions
        - Vary the cognitive complexity (knowledge, comprehension, application, analysis)
        - Mix factual, conceptual, and analytical questions
        - Ensure no two questions test the exact same concept
        - Use different question stems and formats

        Format each question exactly as:
        {{
            "question": "Your question text here?",
            "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
            "correct_answer": "A",
            "explanation": "Detailed explanation of why this answer is correct, referencing specific information from the text and explaining the reasoning process."
        }}

        Ensure questions are:
        - Academically rigorous
        - Professionally worded
        - Balanced in difficulty
        - Relevant to BCS examination standards
        - Designed to test genuine understanding
        - VARIED and not repetitive

        Return ONLY the JSON array of questions, no additional text or formatting.
        """
        
        return prompt
    
    def _parse_gemini_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse Gemini response into structured questions"""
        try:
            # Try to extract JSON from the response
            if '[' in response and ']' in response:
                start = response.find('[')
                end = response.rfind(']') + 1
                json_str = response[start:end]
                questions = json.loads(json_str)
                
                # Validate question format
                valid_questions = []
                for q in questions:
                    if self._validate_question_format(q):
                        valid_questions.append(q)
                
                return valid_questions
            else:
                return []
                
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}")
            return []
    
    def _validate_question_format(self, question: Dict[str, Any]) -> bool:
        """Validate that a question has the correct format"""
        required_fields = ['question', 'options', 'correct_answer', 'explanation']
        
        for field in required_fields:
            if field not in question:
                return False
        
        if not isinstance(question['options'], list) or len(question['options']) != 4:
            return False
        
        if question['correct_answer'] not in ['A', 'B', 'C', 'D']:
            return False
        
        return True
    
    def _generate_fallback_questions(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Generate high-quality fallback questions from text content"""
        questions = []
        
        # Extract structured information from text
        facts = self._extract_facts_from_text(text)
        concepts = self._extract_important_concepts(text)
        dates = self._extract_dates(text)
        numbers = self._extract_numbers(text)
        definitions = self._extract_definitions(text)
        
        # Generate different types of questions
        question_generators = [
            (facts, self._create_fact_based_question),
            (concepts, self._create_concept_question),
            (dates, self._create_date_question),
            (numbers, self._create_number_question),
            (definitions, self._create_definition_question)
        ]
        
        for data, generator_func in question_generators:
            if data and len(questions) < num_questions:
                for item in data[:2]:  # Take up to 2 items from each category
                    if len(questions) >= num_questions:
                        break
                    question = generator_func([item] if not isinstance(item, list) else item, text)
                    if question:
                        questions.append(question)
        
        # If we still need more questions, create generic ones
        while len(questions) < num_questions:
            question = self._create_generic_question(text)
            if question:
                questions.append(question)
        
        return questions[:num_questions]
    
    def _extract_important_concepts(self, text: str) -> List[str]:
        """Extract important concepts from text"""
        # Extract capitalized phrases and technical terms
        concepts = re.findall(r'\b[A-Z][a-zA-Z\s]{3,}\b', text)
        # Remove common words and duplicates
        common_words = {'The', 'This', 'That', 'These', 'Those', 'When', 'Where', 'What', 'Which', 'Who', 'How', 'Why'}
        concepts = [c.strip() for c in concepts if c.strip() not in common_words]
        return list(set(concepts))[:10]  # Return top 10 unique concepts
    
    def _extract_facts_from_text(self, text: str) -> List[str]:
        """Extract factual statements from text"""
        sentences = re.split(r'[.!?]+', text)
        facts = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(word in sentence.lower() for word in ['is', 'are', 'was', 'were', 'has', 'have', 'had']):
                facts.append(sentence)
        
        return facts[:10]
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_patterns = [
            r'\b\d{4}\b',  # Year
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # MM-DD-YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        
        return list(set(dates))[:5]
    
    def _extract_numbers(self, text: str) -> List[str]:
        """Extract numbers from text"""
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        return list(set(numbers))[:10]
    
    def _extract_definitions(self, text: str) -> List[str]:
        """Extract definition-like statements"""
        sentences = re.split(r'[.!?]+', text)
        definitions = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in ['is defined as', 'refers to', 'means', 'is a', 'are']):
                definitions.append(sentence)
        
        return definitions[:5]
    
    def _create_concept_question(self, concept: str, text: str) -> Dict[str, Any]:
        """Create a question about a specific concept"""
        template = random.choice(self.question_templates)
        question_text = template.format(topic=concept)
        
        # Generate plausible options
        options = [
            f"A) {concept} is a fundamental concept in this field",
            f"B) {concept} has no significant role in this context",
            f"C) {concept} is only relevant in specific situations",
            f"D) {concept} is outdated and no longer used"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"Based on the text content, {concept} appears to be an important concept that is discussed in detail."
        }
    
    def _create_fact_based_question(self, facts: List[str], text: str) -> Dict[str, Any]:
        """Create a question based on factual information"""
        if not facts:
            return None
        
        fact = random.choice(facts)
        question_text = f"According to the provided text, which of the following statements is correct?"
        
        # Create options based on the fact
        options = [
            f"A) {fact[:100]}...",
            f"B) The opposite of what is stated in the text",
            f"C) Information not mentioned in the text",
            f"D) A completely unrelated statement"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"This answer is directly supported by the factual information provided in the text."
        }
    
    def _create_date_question(self, dates: List[str], text: str) -> Dict[str, Any]:
        """Create a question about dates"""
        if not dates:
            return None
        
        date = random.choice(dates)
        question_text = f"Which of the following dates is mentioned in the text?"
        
        # Generate options with the correct date and plausible alternatives
        options = [
            f"A) {date}",
            f"B) {int(date) + 1 if date.isdigit() else '2020'}",
            f"C) {int(date) - 1 if date.isdigit() else '2022'}",
            f"D) {int(date) + 5 if date.isdigit() else '2018'}"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"The date {date} is explicitly mentioned in the provided text content."
        }
    
    def _create_number_question(self, numbers: List[str], text: str) -> Dict[str, Any]:
        """Create a question about numbers"""
        if not numbers:
            return None
        
        number = random.choice(numbers)
        question_text = f"Which of the following numbers is mentioned in the text?"
        
        # Generate options
        try:
            num_val = float(number)
            options = [
                f"A) {number}",
                f"B) {num_val + 1}",
                f"C) {num_val - 1}",
                f"D) {num_val * 2}"
            ]
        except:
            options = [
                f"A) {number}",
                f"B) {number}0",
                f"C) {number}00",
                f"D) {number}000"
            ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"The number {number} is explicitly mentioned in the provided text content."
        }
    
    def _create_definition_question(self, definitions: List[str], text: str) -> Dict[str, Any]:
        """Create a question about definitions"""
        if not definitions:
            return None
        
        definition = random.choice(definitions)
        question_text = f"Which of the following best describes the definition provided in the text?"
        
        options = [
            f"A) {definition[:100]}...",
            f"B) A similar but incorrect definition",
            f"C) The opposite of the defined concept",
            f"D) An unrelated definition"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"This answer matches the definition provided in the text content."
        }
    
    def _create_generic_question(self, text: str) -> Dict[str, Any]:
        """Create a generic question about the text content"""
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
            "explanation": "The main topic is the primary subject matter that the text focuses on and discusses in detail."
        } 