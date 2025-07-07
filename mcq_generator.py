import os
import json
import random
from typing import List, Dict, Any
from dotenv import load_dotenv
from gemini_mcq_generator import GeminiMCQGenerator

# Load environment variables
load_dotenv()

class MCQGenerator:
    """Generates BCS-style MCQ questions using Google Gemini AI"""
    
    def __init__(self):
        # Initialize Gemini MCQ Generator
        self.gemini_generator = GeminiMCQGenerator()
        print("✅ MCQ Generator initialized with Google Gemini AI")
        
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
        Generate MCQ questions from text content using Google Gemini AI
        
        Args:
            text: Processed text content
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            List of MCQ questions with options and answers
        """
        if not text:
            raise Exception("No text provided for MCQ generation.")
        # Use Gemini generator (exceptions will propagate)
        return self.gemini_generator.generate_questions(text, num_questions, difficulty)
    

    
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
            self._create_fact_based_question,
            self._create_concept_question,
            self._create_date_question,
            self._create_number_question,
            self._create_definition_question,
            self._create_comparison_question,
            self._create_process_question
        ]
        
        # Generate questions using different strategies
        for i in range(num_questions):
            generator = question_generators[i % len(question_generators)]
            
            if generator == self._create_fact_based_question and facts:
                question = generator(facts, text)
            elif generator == self._create_concept_question and concepts:
                question = generator(concepts[i % len(concepts)] if i < len(concepts) else random.choice(concepts), text)
            elif generator == self._create_date_question and dates:
                question = generator(dates, text)
            elif generator == self._create_number_question and numbers:
                question = generator(numbers, text)
            elif generator == self._create_definition_question and definitions:
                question = generator(definitions, text)
            elif generator == self._create_comparison_question:
                question = generator(text)
            elif generator == self._create_process_question:
                question = generator(text)
            else:
                # Fallback to concept questions
                if concepts:
                    question = self._create_concept_question(random.choice(concepts), text)
                else:
                    question = self._create_generic_question(text)
            
            if question and question not in questions:
                questions.append(question)
        
        # Ensure we have enough questions
        while len(questions) < num_questions:
            question = self._create_generic_question(text)
            if question and question not in questions:
                questions.append(question)
        
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
        return [word for word, freq in sorted_words[:20]]
    
    def _create_concept_question(self, concept: str, text: str) -> Dict[str, Any]:
        """Create a question based on a concept"""
        # Find sentences containing the concept
        sentences = text.split('.')
        relevant_sentences = [s for s in sentences if concept.lower() in s.lower()]
        
        if not relevant_sentences:
            return None
        
        # Get context from relevant sentences
        context_sentence = relevant_sentences[0]
        
        # Create specific question based on the concept and context
        if 'bcs' in concept.lower():
            question_text = f"According to the text, what is the primary role of {concept} in Bangladesh?"
            options = [
                f"A) {concept} serves as the backbone of administrative system",
                f"B) {concept} is only responsible for minor tasks",
                f"C) {concept} has no significant role in governance",
                f"D) {concept} is primarily focused on international affairs"
            ]
            correct_answer = "A"
            explanation = f"According to the text, {concept} is described as the backbone of the administrative system of Bangladesh."
            
        elif 'examination' in concept.lower() or 'exam' in concept.lower():
            question_text = f"What is the structure of the {concept} process as described in the text?"
            options = [
                f"A) It consists of multiple stages including preliminary, written, and viva voce",
                f"B) It is a single-stage process",
                f"C) It only includes written examination",
                f"D) It focuses only on oral interviews"
            ]
            correct_answer = "A"
            explanation = "The text clearly states that the BCS examination is conducted in multiple stages: Preliminary Examination, Written Examination, and Viva Voce."
            
        elif 'cadre' in concept.lower():
            question_text = f"What is the significance of different {concept}s in the BCS system?"
            options = [
                f"A) Each cadre is responsible for different aspects of government administration",
                f"B) All cadres perform the same functions",
                f"C) Cadres are only for organizational purposes",
                f"D) Cadres have no specific responsibilities"
            ]
            correct_answer = "A"
            explanation = "The text explains that BCS is divided into several cadres, each responsible for different aspects of government administration."
            
        elif 'preliminary' in concept.lower():
            question_text = f"What does the {concept} examination consist of?"
            options = [
                f"A) 200 multiple choice questions covering various subjects",
                f"B) Only subjective questions",
                f"C) Only language tests",
                f"D) Only mathematical problems"
            ]
            correct_answer = "A"
            explanation = "The text states that the preliminary examination consists of 200 multiple choice questions covering various subjects including languages, affairs, and technical subjects."
            
        else:
            # Generic but more specific question
            question_text = f"Which statement best describes the role of {concept} according to the provided text?"
            options = [
                f"A) {concept} plays an important role as mentioned in the text",
                f"B) {concept} is not discussed in the text",
                f"C) {concept} is only briefly mentioned",
                f"D) {concept} has no significance in the context"
            ]
            correct_answer = "A"
            explanation = f"The text discusses {concept} in detail, indicating its importance in the context."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": explanation
        }
    
    def _create_sentence_question(self, sentence: str, text: str) -> Dict[str, Any]:
        """Create a question based on a sentence"""
        # Extract key information from sentence
        words = sentence.split()
        if len(words) < 5:
            return None
        
        # Create specific questions based on sentence content
        if '1972' in sentence:
            question_text = "When was the BCS established according to the text?"
            options = [
                "A) 1972, following the independence of Bangladesh",
                "B) 1971, during the liberation war",
                "C) 1973, after the constitution was adopted",
                "D) 1970, before independence"
            ]
            correct_answer = "A"
            explanation = "The text clearly states that BCS was established in 1972, following the independence of Bangladesh."
            
        elif '200' in sentence and 'question' in sentence:
            question_text = "How many questions are there in the BCS preliminary examination?"
            options = [
                "A) 200 multiple choice questions",
                "B) 150 questions",
                "C) 250 questions",
                "D) 100 questions"
            ]
            correct_answer = "A"
            explanation = "The text specifies that the preliminary examination consists of 200 multiple choice questions."
            
        elif 'cadre' in sentence.lower():
            question_text = "What is the purpose of different BCS cadres?"
            options = [
                "A) Each cadre handles different aspects of government administration",
                "B) Cadres are only for organizational structure",
                "C) All cadres perform identical functions",
                "D) Cadres are temporary positions"
            ]
            correct_answer = "A"
            explanation = "The text explains that BCS is divided into several cadres, each responsible for different aspects of government administration."
            
        elif 'stages' in sentence.lower() or 'stage' in sentence.lower():
            question_text = "How many stages does the BCS examination process have?"
            options = [
                "A) Three stages: Preliminary, Written, and Viva Voce",
                "B) Two stages: Written and Interview",
                "C) Four stages including practical test",
                "D) Only one stage"
            ]
            correct_answer = "A"
            explanation = "The text describes three stages: Preliminary Examination, Written Examination, and Viva Voce."
            
        else:
            # Create a question about the main idea
            question_text = "What is the main point conveyed in the following statement?"
            
            # Create more specific options based on sentence content
            if 'bangladesh' in sentence.lower():
                options = [
                    f"A) The statement discusses Bangladesh's administrative system",
                    "B) The statement is about international relations",
                    "C) The statement focuses on economic policies",
                    "D) The statement is about cultural aspects"
                ]
            elif 'government' in sentence.lower():
                options = [
                    "A) The statement relates to government administration",
                    "B) The statement is about private sector",
                    "C) The statement discusses international organizations",
                    "D) The statement is about local governance only"
                ]
            else:
                options = [
                    f"A) {sentence[:60]}...",
                    "B) The statement contains general information",
                    "C) The statement is not relevant to BCS",
                    "D) The statement is about a different topic"
                ]
            
            correct_answer = "A"
            explanation = "The statement contains specific information relevant to the BCS topic being discussed."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": explanation
        }
    
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
        import re
        date_pattern = r'\b(19|20)\d{2}\b'
        dates = re.findall(date_pattern, text)
        return list(set(dates))
    
    def _extract_numbers(self, text: str) -> List[str]:
        """Extract important numbers from text"""
        import re
        number_pattern = r'\b\d+\b'
        numbers = re.findall(number_pattern, text)
        # Filter out common non-important numbers
        important_numbers = [num for num in numbers if int(num) > 10]
        return list(set(important_numbers))
    
    def _extract_definitions(self, text: str) -> List[str]:
        """Extract definition-like statements"""
        sentences = text.split('.')
        definitions = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 30:
                # Look for definition patterns
                if any(pattern in sentence.lower() for pattern in ['is the', 'refers to', 'means', 'defined as', 'known as']):
                    definitions.append(sentence)
        
        return definitions[:5]
    
    def _create_fact_based_question(self, facts: List[str], text: str) -> Dict[str, Any]:
        """Create question based on factual statements"""
        if not facts:
            return None
        
        fact = random.choice(facts)
        words = fact.split()
        
        # Create question about the fact
        if 'bcs' in fact.lower():
            question_text = "Which of the following statements about BCS is correct according to the text?"
        elif 'examination' in fact.lower():
            question_text = "What is stated about the examination process in the text?"
        elif 'cadre' in fact.lower():
            question_text = "What is mentioned about BCS cadres in the text?"
        else:
            question_text = "Which statement is supported by the text?"
        
        # Create options based on the fact
        fact_preview = fact[:80] + "..." if len(fact) > 80 else fact
        options = [
            f"A) {fact_preview}",
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
    
    def _create_date_question(self, dates: List[str], text: str) -> Dict[str, Any]:
        """Create question about dates"""
        if not dates:
            return None
        
        date = random.choice(dates)
        
        if date == "1972":
            question_text = "When was the BCS established?"
            options = [
                "A) 1972",
                "B) 1971",
                "C) 1973",
                "D) 1970"
            ]
            explanation = "The text states that BCS was established in 1972, following the independence of Bangladesh."
        else:
            question_text = f"What significant event occurred in {date}?"
            options = [
                f"A) An important development in {date}",
                f"B) No significant event in {date}",
                f"C) A different year was more important",
                f"D) The text doesn't mention {date}"
            ]
            explanation = f"The text mentions {date} as an important year."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": explanation
        }
    
    def _create_number_question(self, numbers: List[str], text: str) -> Dict[str, Any]:
        """Create question about numbers"""
        if not numbers:
            return None
        
        number = random.choice(numbers)
        
        if number == "200":
            question_text = "How many questions are there in the BCS preliminary examination?"
            options = [
                "A) 200",
                "B) 150",
                "C) 250",
                "D) 100"
            ]
            explanation = "The text specifies that the preliminary examination consists of 200 multiple choice questions."
        elif number == "6":
            question_text = "How many main BCS cadres are mentioned in the text?"
            options = [
                "A) 6",
                "B) 5",
                "C) 7",
                "D) 4"
            ]
            explanation = "The text lists 6 main BCS cadres: Administration, Police, Foreign Affairs, Audit and Accounts, Customs and Excise, and Taxation."
        else:
            question_text = f"What does the number {number} represent in the text?"
            options = [
                f"A) An important quantity mentioned in the text",
                f"B) A random number",
                f"C) A different number is more important",
                f"D) The text doesn't mention {number}"
            ]
            explanation = f"The number {number} is mentioned as an important figure in the text."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": explanation
        }
    
    def _create_definition_question(self, definitions: List[str], text: str) -> Dict[str, Any]:
        """Create question about definitions"""
        if not definitions:
            return None
        
        definition = random.choice(definitions)
        
        question_text = "Which of the following best defines the concept mentioned in the text?"
        options = [
            f"A) {definition[:100]}...",
            "B) A different definition",
            "C) An incomplete definition",
            "D) A definition from another source"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": f"This definition is provided in the text: {definition}"
        }
    
    def _create_comparison_question(self, text: str) -> Dict[str, Any]:
        """Create comparison question"""
        question_text = "Which of the following comparisons is supported by the text?"
        
        if 'preliminary' in text.lower() and 'written' in text.lower():
            options = [
                "A) Preliminary examination comes before written examination",
                "B) Written examination comes before preliminary examination",
                "C) Both examinations are held simultaneously",
                "D) There is no sequence mentioned"
            ]
            explanation = "The text describes the examination process in stages: Preliminary Examination, then Written Examination, then Viva Voce."
        else:
            options = [
                "A) The text provides specific comparisons",
                "B) No comparisons are made in the text",
                "C) Comparisons are implied but not stated",
                "D) The text avoids making comparisons"
            ]
            explanation = "The text contains specific information that allows for comparisons."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": explanation
        }
    
    def _create_process_question(self, text: str) -> Dict[str, Any]:
        """Create question about processes"""
        question_text = "What is the correct sequence of the process described in the text?"
        
        if 'preliminary' in text.lower() and 'written' in text.lower() and 'viva' in text.lower():
            options = [
                "A) Preliminary → Written → Viva Voce",
                "B) Written → Preliminary → Viva Voce",
                "C) Viva Voce → Written → Preliminary",
                "D) All stages are simultaneous"
            ]
            explanation = "The text clearly states the sequence: Preliminary Examination, Written Examination, and Viva Voce."
        else:
            options = [
                "A) The text describes a specific process sequence",
                "B) No process sequence is mentioned",
                "C) The process is random",
                "D) The process is not important"
            ]
            explanation = "The text contains information about processes and their sequences."
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": explanation
        }
    
    def _create_generic_question(self, text: str) -> Dict[str, Any]:
        """Create a generic but relevant question"""
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 30]
        
        if not sentences:
            return None
        
        sentence = random.choice(sentences)
        
        question_text = "What is the main point conveyed in the provided text?"
        options = [
            f"A) {sentence[:80]}...",
            "B) Information not mentioned in the text",
            "C) A different interpretation",
            "D) An unrelated topic"
        ]
        
        return {
            "question": question_text,
            "options": options,
            "correct_answer": "A",
            "explanation": "This information is directly stated in the text."
        }
    
    def create_quiz_session(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a quiz session with questions and tracking"""
        return {
            "session_id": f"quiz_{random.randint(10000, 99999)}",
            "questions": questions,
            "total_questions": len(questions),
            "current_question": 0,
            "score": 0,
            "answers": {},
            "start_time": None,
            "end_time": None
        } 