import PyPDF2
import docx
import os
from typing import Optional
import pdfplumber
import fitz  # PyMuPDF

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
        """Extract text from PDF file with enhanced Bangla support"""
        text = ""
        
        # Try pdfplumber first (best for complex scripts like Bangla)
        try:
            print("Attempting PDF extraction with pdfplumber...")
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                print("Successfully extracted text using pdfplumber")
                return text.strip()
        except Exception as e:
            print(f"pdfplumber failed: {str(e)}")
        
        # Try PyMuPDF (fitz) as second option
        try:
            print("Attempting PDF extraction with PyMuPDF...")
            doc = fitz.open(filepath)
            for page in doc:
                page_text = page.get_text()
                if page_text:
                    text += page_text + "\n"
            doc.close()
            
            if text.strip():
                print("Successfully extracted text using PyMuPDF")
                return text.strip()
        except Exception as e:
            print(f"PyMuPDF failed: {str(e)}")
        
        # Fallback to PyPDF2 (original method)
        try:
            print("Attempting PDF extraction with PyPDF2 (fallback)...")
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                print("Successfully extracted text using PyPDF2")
                return text.strip()
        except Exception as e:
            print(f"PyPDF2 failed: {str(e)}")
        
        # If all methods fail
        raise Exception("All PDF extraction methods failed. The PDF might be corrupted, password-protected, or contain unsupported content.")
    
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