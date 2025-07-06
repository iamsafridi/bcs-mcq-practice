import re
import string
from typing import List

class TextProcessor:
    """Processes and cleans extracted text for MCQ generation"""
    
    def __init__(self):
        self.noise_patterns = [
            r'\b\d+\s*\.\s*',  # Remove numbered lists
            r'^\s*[-*]\s*',    # Remove bullet points
            r'\s+',            # Multiple spaces
            r'[^\w\s\.\,\;\:\!\?\-\(\)]',  # Remove special characters except basic punctuation
        ]
        
        self.sentence_endings = ['.', '!', '?', '।']  # Including Bengali full stop
    
    def process_text(self, text: str) -> str:
        """
        Clean and process extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned and processed text
        """
        if not text:
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        # Remove extra whitespace and normalize
        text = self._normalize_whitespace(text)
        
        # Remove noise patterns
        text = self._remove_noise(text)
        
        # Clean up punctuation
        text = self._clean_punctuation(text)
        
        # Remove empty lines and normalize paragraphs
        text = self._normalize_paragraphs(text)
        
        # Ensure proper sentence endings
        text = self._ensure_sentence_endings(text)
        
        return text.strip()
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace characters"""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace from each line
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        
        return '\n'.join(lines)
    
    def _remove_noise(self, text: str) -> str:
        """Remove noise patterns from text"""
        for pattern in self.noise_patterns:
            text = re.sub(pattern, ' ', text)
        
        return text
    
    def _clean_punctuation(self, text: str) -> str:
        """Clean up punctuation marks"""
        # Remove multiple punctuation marks
        text = re.sub(r'[\.\!\?]+', '.', text)
        text = re.sub(r'[\,\;]+', ',', text)
        
        # Ensure proper spacing around punctuation
        text = re.sub(r'\s*([\.\!\?\,\;])\s*', r'\1 ', text)
        
        return text
    
    def _normalize_paragraphs(self, text: str) -> str:
        """Normalize paragraph structure"""
        # Split into paragraphs
        paragraphs = text.split('\n')
        
        # Remove empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # Join paragraphs with proper spacing
        return ' '.join(paragraphs)
    
    def _ensure_sentence_endings(self, text: str) -> str:
        """Ensure text ends with proper sentence ending"""
        if text and text[-1] not in self.sentence_endings:
            text += '.'
        
        return text
    
    def extract_key_concepts(self, text: str, max_concepts: int = 20) -> List[str]:
        """
        Extract key concepts from text for MCQ generation
        
        Args:
            text: Processed text
            max_concepts: Maximum number of concepts to extract
            
        Returns:
            List of key concepts
        """
        # Split into sentences
        sentences = re.split(r'[.!?।]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Extract potential concepts (words that appear multiple times)
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent words as concepts
        concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        concepts = [concept[0] for concept in concepts[:max_concepts]]
        
        return concepts
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Split text into manageable chunks for processing
        
        Args:
            text: Processed text
            chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        sentences = re.split(r'[.!?।]', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks 