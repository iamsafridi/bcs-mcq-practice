import os
import json
import random
import re
import hashlib
import time
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiMCQGenerator:
    """Enhanced BCS MCQ Generator with advanced features"""
    
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️ Warning: GEMINI_API_KEY not found. Using fallback MCQ generation.")
            self.use_gemini = False
        else:
            genai.configure(api_key=api_key)
            self.use_gemini = True
            print("✅ Enhanced Gemini MCQ Generator initialized!")
        
        # Question cache for performance
        self.question_cache = {}
        
        # Advanced question templates
        self.advanced_templates = {
            'factual': [
                "Which of the following statements accurately describes {topic}?",
                "What is the primary characteristic of {topic}?",
                "According to the text, which statement is correct about {topic}?"
            ],
            'conceptual': [
                "How does {concept1} relate to {concept2}?",
                "What is the significance of {topic} in the context of {context}?",
                "Which principle best explains the relationship between {concept1} and {concept2}?"
            ],
            'analytical': [
                "Based on the information provided, what can be inferred about {topic}?",
                "What would be the most likely outcome if {scenario}?",
                "Which conclusion is best supported by the evidence in the text?"
            ],
            'application': [
                "How would you apply the concept of {topic} in a real-world situation?",
                "Which scenario best demonstrates the practical application of {concept}?",
                "What would be the most effective approach to {situation} based on the text?"
            ],
            'case_study': [
                "In a scenario where {situation}, what would be the most appropriate response?",
                "Given the case of {case}, which factor would be most critical?",
                "If {scenario} occurs, what would be the immediate consequence?"
            ],
            'critical_thinking': [
                "Which argument is most logically sound based on the provided information?",
                "What is the underlying assumption in the statement about {topic}?",
                "Which perspective provides the most balanced view of {issue}?"
            ]
        }
        
        # Fallback questions for when AI is not available
        self.fallback_questions = [
            {
                "question": "What is the main topic discussed in the provided text?",
                "options": ["A) General information", "B) Specific details", "C) Technical concepts", "D) Historical facts"],
                "correct_answer": "A",
                "explanation": "The text contains general information about the topic.",
                "difficulty": "easy",
                "type": "factual"
            },
            {
                "question": "Which of the following is most likely to be true based on the text?",
                "options": ["A) The topic is simple", "B) The topic is complex", "C) The topic is irrelevant", "D) The topic is outdated"],
                "correct_answer": "B",
                "explanation": "Most educational content contains complex concepts.",
                "difficulty": "medium",
                "type": "analytical"
            }
        ]
    
    def generate_questions(self, text: str, num_questions: int = 10, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """
        Generate enhanced MCQ questions from text content
        """
        if not text:
            return self.fallback_questions[:num_questions]
        
        # Check cache first
        cache_key = self._generate_cache_key(text, num_questions, difficulty)
        if cache_key in self.question_cache:
            print("✅ Using cached questions for better performance")
            return self.question_cache[cache_key]
        
        if self.use_gemini:
            questions = self._generate_with_enhanced_gemini(text, num_questions, difficulty)
            if questions and len(questions) > 0:
                # Cache the results
                self.question_cache[cache_key] = questions
                return questions
            else:
                raise Exception("Enhanced Gemini failed to generate questions. Check API key, quota, or response format.")
        else:
            raise Exception("Gemini API key not found or not configured. Cannot generate questions.")
    
    def _generate_cache_key(self, text: str, num_questions: int, difficulty: str) -> str:
        """Generate cache key for questions"""
        content_hash = hashlib.md5(text[:1000].encode()).hexdigest()
        return f"{content_hash}_{num_questions}_{difficulty}"
    
    def _generate_with_enhanced_gemini(self, text: str, num_questions: int, difficulty: str) -> List[Dict[str, Any]]:
        """Generate questions using enhanced Gemini AI with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Analyze text structure and extract key information
                text_analysis = self._analyze_text_structure(text)
                
                # Create enhanced prompt
                prompt = self._create_enhanced_prompt(text, text_analysis, num_questions, difficulty)
                
                # Call Gemini API with enhanced model
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                # Parse and validate response
                questions = self._parse_enhanced_response(response.text)
                
                # Quality assurance
                questions = self._apply_quality_checks(questions, text_analysis)
                
                # Ensure proper distribution
                questions = self._ensure_question_distribution(questions, num_questions, difficulty)
                
                return questions[:num_questions]
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise Exception(f"Enhanced Gemini failed after {max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def _analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """Analyze text structure for better question generation"""
        analysis = {
            'topics': self._extract_topics(text),
            'concepts': self._extract_concepts(text),
            'facts': self._extract_facts(text),
            'relationships': self._extract_relationships(text),
            'complexity': self._assess_complexity(text),
            'structure': self._analyze_structure(text)
        }
        return analysis
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text"""
        # Enhanced topic extraction using NLP-like patterns
        sentences = re.split(r'[.!?।]', text)
        topics = []
        
        for sentence in sentences:
            # Look for topic indicators
            if any(indicator in sentence.lower() for indicator in ['topic', 'subject', 'theme', 'area', 'field']):
                # Extract potential topics
                words = re.findall(r'\b[A-Z][a-zA-Z\s]{3,}\b', sentence)
                topics.extend(words)
        
        return list(set(topics))[:15]
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts with enhanced logic"""
        # Look for concept patterns
        concept_patterns = [
            r'\b[A-Z][a-zA-Z\s]{3,}\b',  # Capitalized phrases
            r'\b\w+ism\b',  # -ism words
            r'\b\w+tion\b',  # -tion words
            r'\b\w+ment\b',  # -ment words
        ]
        
        concepts = []
        for pattern in concept_patterns:
            concepts.extend(re.findall(pattern, text))
        
        # Filter and rank concepts
        concept_freq = {}
        for concept in concepts:
            clean_concept = concept.strip()
            if len(clean_concept) > 3:
                concept_freq[clean_concept] = concept_freq.get(clean_concept, 0) + 1
        
        # Return top concepts
        sorted_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, freq in sorted_concepts[:20]]
    
    def _extract_facts(self, text: str) -> List[str]:
        """Extract factual statements with enhanced logic"""
        sentences = re.split(r'[.!?।]', text)
        facts = []
        
        fact_indicators = [
            'is', 'are', 'was', 'were', 'has', 'have', 'had',
            'consists', 'includes', 'contains', 'established', 'created',
            'defined', 'refers', 'means', 'represents', 'indicates'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                # Check for factual patterns
                if any(indicator in sentence.lower() for indicator in fact_indicators):
                    facts.append(sentence)
        
        return facts[:20]
    
    def _extract_relationships(self, text: str) -> List[Dict[str, str]]:
        """Extract relationships between concepts"""
        relationships = []
        
        # Look for relationship indicators
        relationship_patterns = [
            (r'(\w+)\s+(causes|leads to|results in)\s+(\w+)', 'cause-effect'),
            (r'(\w+)\s+(is similar to|resembles|like)\s+(\w+)', 'similarity'),
            (r'(\w+)\s+(differs from|unlike|different from)\s+(\w+)', 'difference'),
            (r'(\w+)\s+(depends on|requires|needs)\s+(\w+)', 'dependency'),
        ]
        
        for pattern, rel_type in relationship_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                relationships.append({
                    'concept1': match[0],
                    'concept2': match[2],
                    'type': rel_type,
                    'indicator': match[1]
                })
        
        return relationships[:10]
    
    def _assess_complexity(self, text: str) -> str:
        """Assess text complexity"""
        # Simple complexity assessment
        avg_sentence_length = len(text.split()) / len(re.split(r'[.!?।]', text))
        unique_words = len(set(text.lower().split()))
        
        if avg_sentence_length > 25 or unique_words > 500:
            return 'high'
        elif avg_sentence_length > 15 or unique_words > 200:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze text structure"""
        paragraphs = text.split('\n\n')
        sentences = re.split(r'[.!?।]', text)
        
        return {
            'paragraphs': len(paragraphs),
            'sentences': len(sentences),
            'avg_paragraph_length': len(sentences) / len(paragraphs) if paragraphs else 0,
            'has_lists': bool(re.search(r'\d+\.|\*|\-', text)),
            'has_definitions': bool(re.search(r'is defined as|refers to|means', text, re.IGNORECASE))
        }
    
    def _create_enhanced_prompt(self, text: str, analysis: Dict[str, Any], num_questions: int, difficulty: str) -> str:
        """Create enhanced prompt with better structure and variety"""
        import time
        import random
        
        # Language detection
        def is_bangla(text):
            bangla_chars = sum(1 for c in text if '\u0980' <= c <= '\u09FF')
            return bangla_chars > 0.3 * len(text)
        
        is_bangla_text = is_bangla(text)
        random_seed = int(time.time() * 1000) + random.randint(1, 1000)
        text_preview = text[:5000] + "..." if len(text) > 5000 else text
        
        # Enhanced focus areas
        focus_areas = [
            "comprehensive topic coverage with balanced distribution",
            "conceptual relationships and theoretical frameworks",
            "practical applications and real-world scenarios",
            "critical analysis and evaluative thinking",
            "synthesis of multiple concepts and interdisciplinary connections",
            "problem-solving and decision-making scenarios",
            "comparative analysis and contrasting perspectives",
            "chronological and causal relationships",
            "quantitative and qualitative data interpretation",
            "ethical considerations and value-based judgments"
        ]
        
        selected_focus = focus_areas[random_seed % len(focus_areas)]
        language_instruction = "All questions, options, and explanations must be in Bangla (বাংলা ভাষা) if the input text is in Bangla. Otherwise, use English." if is_bangla_text else "Use English."
        
        # Enhanced prompt with better structure
        prompt = f"""
        You are an expert BCS (Bangladesh Civil Service) exam question generator with advanced knowledge of competitive exam patterns and educational psychology. Generate {num_questions} high-quality multiple choice questions based on the provided text content.

        TEXT ANALYSIS:
        - Main Topics: {', '.join(analysis['topics'][:5])}
        - Key Concepts: {', '.join(analysis['concepts'][:5])}
        - Text Complexity: {analysis['complexity']}
        - Structure: {analysis['structure']['paragraphs']} paragraphs, {analysis['structure']['sentences']} sentences

        FOCUS AREA: {selected_focus}
        DIFFICULTY LEVEL: {difficulty}
        RANDOM SEED: {random_seed}

        {language_instruction}

        ENHANCED REQUIREMENTS:

        1. QUESTION TYPES (Distribute evenly):
           - Factual (20%): Basic facts, definitions, simple comprehension
           - Conceptual (25%): Understanding relationships, principles, theories
           - Analytical (25%): Analysis, inference, interpretation
           - Application (20%): Real-world application, problem-solving
           - Critical Thinking (10%): Evaluation, synthesis, judgment

        2. COGNITIVE LEVELS:
           - Knowledge: Recall facts, definitions, concepts
           - Comprehension: Understand meaning, interpret information
           - Application: Apply concepts to new situations
           - Analysis: Break down complex information
           - Synthesis: Combine elements to create new understanding
           - Evaluation: Make judgments based on criteria

        3. QUALITY STANDARDS:
           - Each question must be directly based on the text
           - All options must be plausible and well-distributed
           - Correct answer should not be obvious
           - Explanations must reference specific text content
           - Questions should test genuine understanding, not memorization

        4. ADVANCED QUESTION PATTERNS:
           - Case Study: "In a scenario where [situation], what would be the most appropriate response?"
           - Comparative: "What is the key difference between [concept1] and [concept2]?"
           - Analytical: "Based on the information provided, what can be inferred about [topic]?"
           - Application: "How would you apply the principle of [concept] in [scenario]?"
           - Critical: "Which argument is most logically sound regarding [topic]?"
           - Synthesis: "What conclusion can be drawn by combining the information about [concept1] and [concept2]?"

        5. DIFFICULTY GUIDELINES:
           - Easy: Basic facts, simple comprehension, straightforward application
           - Medium: Analysis of relationships, moderate complexity, application to familiar contexts
           - Hard: Synthesis of multiple concepts, complex scenarios, critical evaluation

        TEXT CONTENT:
        {text_preview}

        FORMAT EACH QUESTION AS:
        {{
            "question": "Question text here?",
            "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
            "correct_answer": "A",
            "explanation": "Detailed explanation referencing specific text content and reasoning process.",
            "difficulty": "easy|medium|hard",
            "type": "factual|conceptual|analytical|application|critical_thinking",
            "cognitive_level": "knowledge|comprehension|application|analysis|synthesis|evaluation"
        }}

        QUALITY CHECKS:
        - Ensure no two questions test the exact same concept
        - Vary question stems and formats
        - Include questions from different sections of the text
        - Balance difficulty levels appropriately
        - Make explanations educational and comprehensive

        Return ONLY the JSON array of questions, no additional text.
        """
        
        return prompt
    
    def _parse_enhanced_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse enhanced Gemini response with better error handling"""
        try:
            # Try to extract JSON from the response
            if '[' in response and ']' in response:
                start = response.find('[')
                end = response.rfind(']') + 1
                json_str = response[start:end]
                questions = json.loads(json_str)
                
                # Enhanced validation
                valid_questions = []
                for q in questions:
                    if self._validate_enhanced_question_format(q):
                        valid_questions.append(q)
                
                return valid_questions
            else:
                print("Warning: No valid JSON found in response")
                return []
                
        except Exception as e:
            print(f"Error parsing enhanced Gemini response: {str(e)}")
            return []
    
    def _validate_enhanced_question_format(self, question: Dict[str, Any]) -> bool:
        """Enhanced question format validation"""
        required_fields = ['question', 'options', 'correct_answer', 'explanation']
        optional_fields = ['difficulty', 'type', 'cognitive_level']
        
        # Check required fields
        for field in required_fields:
            if field not in question:
                return False
        
        # Validate options
        if not isinstance(question['options'], list) or len(question['options']) != 4:
            return False
        
        # Validate correct answer
        if question['correct_answer'] not in ['A', 'B', 'C', 'D']:
            return False
        
        # Validate optional fields if present
        if 'difficulty' in question and question['difficulty'] not in ['easy', 'medium', 'hard']:
            question['difficulty'] = 'medium'  # Default
        
        if 'type' in question and question['type'] not in ['factual', 'conceptual', 'analytical', 'application', 'critical_thinking']:
            question['type'] = 'factual'  # Default
        
        return True
    
    def _apply_quality_checks(self, questions: List[Dict[str, Any]], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply quality assurance checks to questions"""
        checked_questions = []
        
        for question in questions:
            # Check for ambiguity
            if self._is_question_ambiguous(question):
                continue
            
            # Check for bias
            if self._is_question_biased(question):
                continue
            
            # Check for clarity
            if self._is_question_unclear(question):
                continue
            
            # Check for relevance
            if self._is_question_relevant(question, analysis):
                checked_questions.append(question)
        
        return checked_questions
    
    def _is_question_ambiguous(self, question: Dict[str, Any]) -> bool:
        """Check if question is ambiguous"""
        # Simple ambiguity checks
        ambiguous_indicators = ['all of the above', 'none of the above', 'both a and b', 'either a or b']
        question_text = question['question'].lower()
        
        return any(indicator in question_text for indicator in ambiguous_indicators)
    
    def _is_question_biased(self, question: Dict[str, Any]) -> bool:
        """Check if question has bias"""
        # Simple bias checks
        biased_indicators = ['obviously', 'clearly', 'definitely', 'certainly']
        question_text = question['question'].lower()
        
        return any(indicator in question_text for indicator in biased_indicators)
    
    def _is_question_unclear(self, question: Dict[str, Any]) -> bool:
        """Check if question is unclear"""
        # Simple clarity checks
        question_text = question['question']
        
        # Check for very long questions
        if len(question_text) > 200:
            return True
        
        # Check for unclear wording
        unclear_indicators = ['etc', 'and so on', '...']
        return any(indicator in question_text.lower() for indicator in unclear_indicators)
    
    def _is_question_relevant(self, question: Dict[str, Any], analysis: Dict[str, Any]) -> bool:
        """Check if question is relevant to the text content"""
        # Simple relevance check - ensure question contains words from the text
        question_words = set(re.findall(r'\b\w+\b', question['question'].lower()))
        text_words = set(re.findall(r'\b\w+\b', ' '.join(analysis['concepts']).lower()))
        
        # Check for overlap
        overlap = question_words.intersection(text_words)
        return len(overlap) > 0
    
    def _ensure_question_distribution(self, questions: List[Dict[str, Any]], num_questions: int, difficulty: str) -> List[Dict[str, Any]]:
        """Ensure proper distribution of question types and difficulty"""
        if not questions:
            return questions
        
        # Target distribution based on difficulty
        if difficulty == 'easy':
            target_distribution = {
                'factual': 0.4,
                'conceptual': 0.3,
                'analytical': 0.2,
                'application': 0.1,
                'critical_thinking': 0.0
            }
        elif difficulty == 'hard':
            target_distribution = {
                'factual': 0.1,
                'conceptual': 0.2,
                'analytical': 0.3,
                'application': 0.3,
                'critical_thinking': 0.1
            }
        else:  # medium
            target_distribution = {
                'factual': 0.2,
                'conceptual': 0.25,
                'analytical': 0.25,
                'application': 0.2,
                'critical_thinking': 0.1
            }
        
        # Count current distribution
        current_distribution = {}
        for question in questions:
            q_type = question.get('type', 'factual')
            current_distribution[q_type] = current_distribution.get(q_type, 0) + 1
        
        # Adjust if needed
        adjusted_questions = []
        for q_type, target_ratio in target_distribution.items():
            target_count = int(num_questions * target_ratio)
            current_count = current_distribution.get(q_type, 0)
            
            # Add questions of this type
            type_questions = [q for q in questions if q.get('type', 'factual') == q_type]
            adjusted_questions.extend(type_questions[:target_count])
        
        # Fill remaining slots
        remaining = num_questions - len(adjusted_questions)
        if remaining > 0:
            unused_questions = [q for q in questions if q not in adjusted_questions]
            adjusted_questions.extend(unused_questions[:remaining])
        
        return adjusted_questions[:num_questions]
    
    # Keep existing fallback methods for compatibility
    def _generate_fallback_questions(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """Enhanced fallback question generation"""
        # Use existing fallback logic but with enhanced templates
        return self.fallback_questions[:num_questions]
    
    def _extract_important_concepts(self, text: str) -> List[str]:
        """Enhanced concept extraction"""
        return self._extract_concepts(text)
    
    def _extract_facts_from_text(self, text: str) -> List[str]:
        """Enhanced fact extraction"""
        return self._extract_facts(text)
    
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
    
    # Keep existing question creation methods for fallback
    def _create_concept_question(self, concept: str, text: str) -> Dict[str, Any]:
        """Create a question about a specific concept"""
        template = random.choice(self.advanced_templates['conceptual'])
        question_text = template.format(topic=concept, concept1=concept, concept2="related concept")
        
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
            "explanation": f"Based on the text content, {concept} appears to be an important concept that is discussed in detail.",
            "difficulty": "medium",
            "type": "conceptual",
            "cognitive_level": "comprehension"
        }
    
    def _create_fact_based_question(self, facts: List[str], text: str) -> Dict[str, Any]:
        """Create a question based on factual information"""
        if not facts:
            return None
        
        fact = random.choice(facts)
        question_text = f"According to the provided text, which of the following statements is correct?"
        
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
            "explanation": f"This answer is directly supported by the factual information provided in the text.",
            "difficulty": "easy",
            "type": "factual",
            "cognitive_level": "knowledge"
        }
    
    def _create_date_question(self, dates: List[str], text: str) -> Dict[str, Any]:
        """Create a question about dates"""
        if not dates:
            return None
        
        date = random.choice(dates)
        question_text = f"Which of the following dates is mentioned in the text?"
        
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
            "explanation": f"The date {date} is explicitly mentioned in the provided text content.",
            "difficulty": "easy",
            "type": "factual",
            "cognitive_level": "knowledge"
        }
    
    def _create_number_question(self, numbers: List[str], text: str) -> Dict[str, Any]:
        """Create a question about numbers"""
        if not numbers:
            return None
        
        number = random.choice(numbers)
        question_text = f"Which of the following numbers is mentioned in the text?"
        
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
            "explanation": f"The number {number} is explicitly mentioned in the provided text content.",
            "difficulty": "easy",
            "type": "factual",
            "cognitive_level": "knowledge"
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
            "explanation": f"This answer matches the definition provided in the text content.",
            "difficulty": "medium",
            "type": "conceptual",
            "cognitive_level": "comprehension"
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
            "explanation": "This information is directly stated in the text.",
            "difficulty": "easy",
            "type": "factual",
            "cognitive_level": "knowledge"
        } 