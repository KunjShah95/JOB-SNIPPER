"""
MCP PDF Server - Model Context Protocol Server for PDF Processing
Provides PDF parsing tools via MCP protocol
"""

import asyncio
import json
import logging
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import os

# MCP and PDF processing imports
try:
    import pdfplumber
    import PyPDF2
    from mcp import McpServer, Tool
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logging.warning("MCP or PDF processing libraries not available")

class PDFMCPServer:
    def __init__(self):
        self.server = McpServer("pdf-processor") if MCP_AVAILABLE else None
        self.logger = logging.getLogger("PDFMCPServer")
        
        if MCP_AVAILABLE:
            self._register_tools()
    
    def _register_tools(self):
        """Register PDF processing tools with MCP server"""
        
        @self.server.tool("extract_text_from_pdf")
        async def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
            """Extract text content from PDF file"""
            try:
                text_content = ""
                metadata = {}
                
                # Try pdfplumber first (better for complex layouts)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        metadata = {
                            "pages": len(pdf.pages),
                            "title": pdf.metadata.get('Title', ''),
                            "author": pdf.metadata.get('Author', ''),
                            "creator": pdf.metadata.get('Creator', '')
                        }
                        
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text_content += page_text + "\n"
                
                except Exception as e:
                    self.logger.warning(f"pdfplumber failed: {e}, trying PyPDF2")
                    
                    # Fallback to PyPDF2
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        metadata = {
                            "pages": len(pdf_reader.pages),
                            "title": pdf_reader.metadata.get('/Title', '') if pdf_reader.metadata else '',
                            "author": pdf_reader.metadata.get('/Author', '') if pdf_reader.metadata else ''
                        }
                        
                        for page in pdf_reader.pages:
                            text_content += page.extract_text() + "\n"
                
                return {
                    "success": True,
                    "text": text_content.strip(),
                    "metadata": metadata,
                    "method": "pdf_extraction"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "text": "",
                    "metadata": {}
                }
        
        @self.server.tool("parse_resume_structure")
        async def parse_resume_structure(text_content: str) -> Dict[str, Any]:
            """Parse resume structure from text content"""
            try:
                # Enhanced resume parsing logic
                sections = self._identify_resume_sections(text_content)
                contact_info = self._extract_contact_info(text_content)
                skills = self._extract_skills(text_content)
                experience = self._extract_experience(text_content)
                education = self._extract_education(text_content)
                
                return {
                    "success": True,
                    "parsed_data": {
                        "sections": sections,
                        "contact_info": contact_info,
                        "skills": skills,
                        "experience": experience,
                        "education": education,
                        "raw_text": text_content
                    }
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "parsed_data": {}
                }
        
        @self.server.tool("validate_pdf_file")
        async def validate_pdf_file(file_path: str) -> Dict[str, Any]:
            """Validate PDF file integrity and readability"""
            try:
                if not os.path.exists(file_path):
                    return {"valid": False, "error": "File does not exist"}
                
                if not file_path.lower().endswith('.pdf'):
                    return {"valid": False, "error": "Not a PDF file"}
                
                # Try to open and read first page
                with pdfplumber.open(file_path) as pdf:
                    if len(pdf.pages) == 0:
                        return {"valid": False, "error": "PDF has no pages"}
                    
                    # Try to extract text from first page
                    first_page_text = pdf.pages[0].extract_text()
                    
                    return {
                        "valid": True,
                        "pages": len(pdf.pages),
                        "has_text": bool(first_page_text and first_page_text.strip()),
                        "file_size": os.path.getsize(file_path)
                    }
                    
            except Exception as e:
                return {"valid": False, "error": str(e)}
    
    def _identify_resume_sections(self, text: str) -> Dict[str, List[str]]:
        """Identify different sections in resume text"""
        import re
        
        sections = {
            "contact": [],
            "summary": [],
            "experience": [],
            "education": [],
            "skills": [],
            "projects": [],
            "certifications": []
        }
        
        lines = text.split('\n')
        current_section = None
        
        section_patterns = {
            "contact": r"(contact|phone|email|address|linkedin)",
            "summary": r"(summary|objective|profile|about)",
            "experience": r"(experience|employment|work|career)",
            "education": r"(education|academic|degree|university|college)",
            "skills": r"(skills|technical|competencies|technologies)",
            "projects": r"(projects|portfolio|work samples)",
            "certifications": r"(certifications|certificates|licenses)"
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line_lower) and len(line.strip()) < 50:
                    current_section = section
                    break
            
            # Add content to current section
            if current_section and line.strip():
                sections[current_section].append(line.strip())
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        import re
        
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact['email'] = emails[0]
        
        # Phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.search(linkedin_pattern, text.lower())
        if linkedin:
            contact['linkedin'] = linkedin.group()
        
        return contact
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        import re
        
        # Common technical skills
        skill_patterns = [
            r'\b(Python|Java|JavaScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin)\b',
            r'\b(React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|Laravel)\b',
            r'\b(AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|Linux|Windows)\b',
            r'\b(SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Cassandra)\b',
            r'\b(Machine Learning|AI|Data Science|Deep Learning|NLP|Computer Vision)\b',
            r'\b(TensorFlow|PyTorch|Scikit-learn|Pandas|NumPy|Matplotlib)\b'
        ]
        
        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        return list(skills)
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience"""
        import re
        
        # Look for date patterns and job titles
        date_pattern = r'(\d{4}|\d{1,2}/\d{4}|\w+\s+\d{4})'
        
        experiences = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if re.search(date_pattern, line) and len(line.strip()) > 10:
                # Potential experience entry
                experience = {
                    "title": line.strip(),
                    "description": ""
                }
                
                # Get following lines as description
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip() and not re.search(date_pattern, lines[j]):
                        experience["description"] += lines[j].strip() + " "
                
                if experience["description"]:
                    experiences.append(experience)
        
        return experiences[:5]  # Return top 5 experiences
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        import re
        
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|B\.Tech|M\.Tech)',
            r'(University|College|Institute|School)'
        ]
        
        lines = text.split('\n')
        for line in lines:
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    education.append({
                        "degree": line.strip(),
                        "institution": ""
                    })
                    break
        
        return education[:3]  # Return top 3 education entries
    
    async def start_server(self, host: str = "localhost", port: int = 8010):
        """Start the MCP server"""
        if not MCP_AVAILABLE:
            self.logger.error("MCP not available - cannot start server")
            return
        
        try:
            await self.server.start(host=host, port=port)
            self.logger.info(f"PDF MCP Server started on {host}:{port}")
        except Exception as e:
            self.logger.error(f"Failed to start MCP server: {e}")

# Standalone server runner
async def main():
    server = PDFMCPServer()
    await server.start_server()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
