"""
ATS-Friendly Resume Builder with Download Functionality
"""
import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import io
import base64

logger = logging.getLogger(__name__)

@dataclass
class PersonalInfo:
    """Personal information structure"""
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""

@dataclass
class Experience:
    """Work experience structure"""
    title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    description: List[str] = None
    
    def __post_init__(self):
        if self.description is None:
            self.description = []

@dataclass
class Education:
    """Education structure"""
    degree: str = ""
    institution: str = ""
    location: str = ""
    graduation_date: str = ""
    gpa: str = ""
    relevant_coursework: List[str] = None
    
    def __post_init__(self):
        if self.relevant_coursework is None:
            self.relevant_coursework = []

@dataclass
class Project:
    """Project structure"""
    name: str = ""
    description: str = ""
    technologies: List[str] = None
    link: str = ""
    
    def __post_init__(self):
        if self.technologies is None:
            self.technologies = []

@dataclass
class ResumeData:
    """Complete resume data structure"""
    personal_info: PersonalInfo = None
    summary: str = ""
    skills: List[str] = None
    experience: List[Experience] = None
    education: List[Education] = None
    projects: List[Project] = None
    certifications: List[str] = None
    
    def __post_init__(self):
        if self.personal_info is None:
            self.personal_info = PersonalInfo()
        if self.skills is None:
            self.skills = []
        if self.experience is None:
            self.experience = []
        if self.education is None:
            self.education = []
        if self.projects is None:
            self.projects = []
        if self.certifications is None:
            self.certifications = []

class ATSResumeBuilder:
    """ATS-Friendly Resume Builder"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for ATS-friendly formatting"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=colors.black
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.black,
            borderWidth=1,
            borderColor=colors.black,
            borderPadding=2
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            alignment=TA_LEFT
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
    
    def build_resume_pdf(self, resume_data: ResumeData) -> bytes:
        """Build ATS-friendly PDF resume"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            story = []
            
            # Header with personal information
            story.extend(self._build_header(resume_data.personal_info))
            
            # Professional summary
            if resume_data.summary:
                story.extend(self._build_summary(resume_data.summary))
            
            # Skills section
            if resume_data.skills:
                story.extend(self._build_skills(resume_data.skills))
            
            # Experience section
            if resume_data.experience:
                story.extend(self._build_experience(resume_data.experience))
            
            # Education section
            if resume_data.education:
                story.extend(self._build_education(resume_data.education))
            
            # Projects section
            if resume_data.projects:
                story.extend(self._build_projects(resume_data.projects))
            
            # Certifications section
            if resume_data.certifications:
                story.extend(self._build_certifications(resume_data.certifications))
            
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error building PDF resume: {e}")
            raise
    
    def _build_header(self, personal_info: PersonalInfo) -> List:
        """Build header section with contact information"""
        story = []
        
        # Name
        if personal_info.full_name:
            story.append(Paragraph(personal_info.full_name, self.styles['CustomHeader']))
        
        # Contact information
        contact_parts = []
        if personal_info.email:
            contact_parts.append(personal_info.email)
        if personal_info.phone:
            contact_parts.append(personal_info.phone)
        if personal_info.location:
            contact_parts.append(personal_info.location)
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        # Professional links
        links = []
        if personal_info.linkedin:
            links.append(f"LinkedIn: {personal_info.linkedin}")
        if personal_info.github:
            links.append(f"GitHub: {personal_info.github}")
        if personal_info.website:
            links.append(f"Website: {personal_info.website}")
        
        if links:
            links_text = " | ".join(links)
            story.append(Paragraph(links_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        return story
    
    def _build_summary(self, summary: str) -> List:
        """Build professional summary section"""
        story = []
        story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['SectionHeader']))
        story.append(Paragraph(summary, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        return story
    
    def _build_skills(self, skills: List[str]) -> List:
        """Build skills section"""
        story = []
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['SectionHeader']))
        
        # Group skills for better ATS parsing
        skills_text = " • ".join(skills)
        story.append(Paragraph(skills_text, self.styles['BodyText']))
        story.append(Spacer(1, 12))
        return story
    
    def _build_experience(self, experience: List[Experience]) -> List:
        """Build work experience section"""
        story = []
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['SectionHeader']))
        
        for exp in experience:
            # Job title and company
            title_company = f"<b>{exp.title}</b>"
            if exp.company:
                title_company += f" | {exp.company}"
            if exp.location:
                title_company += f" | {exp.location}"
            
            story.append(Paragraph(title_company, self.styles['BodyText']))
            
            # Dates
            if exp.start_date or exp.end_date:
                date_range = f"{exp.start_date} - {exp.end_date or 'Present'}"
                story.append(Paragraph(date_range, self.styles['BodyText']))
            
            # Description
            for desc in exp.description:
                story.append(Paragraph(f"• {desc}", self.styles['BodyText']))
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_education(self, education: List[Education]) -> List:
        """Build education section"""
        story = []
        story.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
        
        for edu in education:
            # Degree and institution
            edu_text = f"<b>{edu.degree}</b>"
            if edu.institution:
                edu_text += f" | {edu.institution}"
            if edu.location:
                edu_text += f" | {edu.location}"
            
            story.append(Paragraph(edu_text, self.styles['BodyText']))
            
            # Graduation date and GPA
            details = []
            if edu.graduation_date:
                details.append(f"Graduated: {edu.graduation_date}")
            if edu.gpa:
                details.append(f"GPA: {edu.gpa}")
            
            if details:
                story.append(Paragraph(" | ".join(details), self.styles['BodyText']))
            
            # Relevant coursework
            if edu.relevant_coursework:
                coursework = "Relevant Coursework: " + ", ".join(edu.relevant_coursework)
                story.append(Paragraph(coursework, self.styles['BodyText']))
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_projects(self, projects: List[Project]) -> List:
        """Build projects section"""
        story = []
        story.append(Paragraph("PROJECTS", self.styles['SectionHeader']))
        
        for project in projects:
            # Project name
            project_text = f"<b>{project.name}</b>"
            if project.link:
                project_text += f" | {project.link}"
            
            story.append(Paragraph(project_text, self.styles['BodyText']))
            
            # Description
            if project.description:
                story.append(Paragraph(project.description, self.styles['BodyText']))
            
            # Technologies
            if project.technologies:
                tech_text = "Technologies: " + ", ".join(project.technologies)
                story.append(Paragraph(tech_text, self.styles['BodyText']))
            
            story.append(Spacer(1, 6))
        
        return story
    
    def _build_certifications(self, certifications: List[str]) -> List:
        """Build certifications section"""
        story = []
        story.append(Paragraph("CERTIFICATIONS", self.styles['SectionHeader']))
        
        for cert in certifications:
            story.append(Paragraph(f"• {cert}", self.styles['BodyText']))
        
        return story
    
    def generate_ats_tips(self) -> List[str]:
        """Generate ATS optimization tips"""
        return [
            "Use standard section headers (Experience, Education, Skills)",
            "Include relevant keywords from the job description",
            "Use simple, clean formatting without graphics or tables",
            "Save in both PDF and Word formats",
            "Use standard fonts (Arial, Calibri, Times New Roman)",
            "Include your full contact information",
            "Use bullet points for easy scanning",
            "Quantify achievements with numbers and percentages",
            "Spell out acronyms on first use",
            "Avoid headers, footers, and text boxes"
        ]
    
    def optimize_for_keywords(self, resume_data: ResumeData, job_keywords: List[str]) -> ResumeData:
        """Optimize resume content for specific job keywords"""
        try:
            # This is a basic implementation - in a real system, you'd use more sophisticated NLP
            optimized_data = resume_data
            
            # Add missing keywords to skills if relevant
            current_skills_lower = [skill.lower() for skill in resume_data.skills]
            for keyword in job_keywords:
                if keyword.lower() not in current_skills_lower:
                    # Simple relevance check - in practice, you'd use more sophisticated matching
                    if any(tech in keyword.lower() for tech in ['python', 'java', 'sql', 'aws', 'react']):
                        optimized_data.skills.append(keyword)
            
            return optimized_data
            
        except Exception as e:
            logger.error(f"Error optimizing resume: {e}")
            return resume_data

def create_download_link(file_content: bytes, filename: str, file_type: str = "pdf") -> str:
    """Create a download link for the generated resume"""
    try:
        b64_content = base64.b64encode(file_content).decode()
        
        if file_type.lower() == "pdf":
            mime_type = "application/pdf"
        else:
            mime_type = "application/octet-stream"
        
        download_link = f'<a href="data:{mime_type};base64,{b64_content}" download="{filename}">📥 Download {filename}</a>'
        return download_link
        
    except Exception as e:
        logger.error(f"Error creating download link: {e}")
        return "Error creating download link"