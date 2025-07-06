import PyPDF2
import docx
import os
from typing import Optional

class FileHandler:
    """Handles file upload and text extraction from various formats"""
    
    def __init__(self):
        self.supported_formats = {
            '.pdf': self._extract_from_pdf,
            '.docx': self._extract_from_docx,
            '.doc': self._extract_from_docx,
            '.txt': self._extract_from_txt
        }
    
    def extract_text(self, filepath: str) -> Optional[str]:
        """
        Extract text from uploaded file based on its format
        
        Args:
            filepath: Path to the uploaded file
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            file_extension = os.path.splitext(filepath)[1].lower()
            
            if file_extension in self.supported_formats:
                return self.supported_formats[file_extension](filepath)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            print(f"Error extracting text from {filepath}: {str(e)}")
            return None
    
    def _extract_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_from_docx(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(filepath)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    def _extract_from_txt(self, filepath: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                with open(filepath, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                raise Exception(f"Failed to read text file: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to read text file: {str(e)}")
    
    def cleanup_file(self, filepath: str) -> bool:
        """
        Clean up uploaded file after processing
        
        Args:
            filepath: Path to the file to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {filepath}: {str(e)}")
            return False 