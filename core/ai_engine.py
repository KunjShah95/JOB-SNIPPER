"""
Advanced AI Engine with real AI capabilities
"""
import os
import logging
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import openai
from transformers import pipeline, AutoTokenizer, AutoModel
import spacy
import re
from datetime import datetime
import json

# Import at module level for better performance
pd.set_option('display.max_columns', None)

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Structured analysis result"""
    score: float
    details: Dict[str, Any]
    recommendations: List[str]
    confidence: float
    timestamp: datetime

class AIEngine:
    """Advanced AI Engine with real capabilities"""
    
    def __init__(self):
        self.openai_client = None
        self.nlp_model = None
        self.skill_extractor = None
        self.sentiment_analyzer = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            # Initialize OpenAI
            if os.getenv('OPENAI_API_KEY'):
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            
            # Initialize spaCy for NLP
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded")
            except OSError:
                logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            
            # Initialize transformers for skill extraction
            try:
                self.skill_extractor = pipeline(
                    "ner",
                    model="dbmdz/bert-large-cased-finetuned-conll03-english",
                    aggregation_strategy="simple"
                )
                logger.info("Skill extraction model loaded")
            except Exception as e:
                logger.warning(f"Could not load skill extraction model: {e}")
            
            # Initialize sentiment analyzer
            try:
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
                logger.info("Sentiment analyzer loaded")
            except Exception as e:
                logger.warning(f"Could not load sentiment analyzer: {e}")
                
        except Exception as e:
            logger.error(f"Error initializing AI models: {e}")
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> AnalysisResult:
        """
        Analyze resume with real AI capabilities
        
        Args:
            resume_text: The resume content
            job_description: Optional job description for matching
            
        Returns:
            AnalysisResult with detailed analysis
        """
        try:
            analysis_details = {}
            recommendations = []
            
            # Extract skills using NLP
            skills = self._extract_skills(resume_text)
            analysis_details['extracted_skills'] = skills
            
            # Analyze structure and content
            structure_score = self._analyze_resume_structure(resume_text)
            analysis_details['structure_score'] = structure_score
            
            # Extract experience and education
            experience = self._extract_experience(resume_text)
            education = self._extract_education(resume_text)
            analysis_details['experience'] = experience
            analysis_details['education'] = education
            
            # Calculate overall score
            overall_score = self._calculate_resume_score(
                skills, structure_score, experience, education
            )
            
            # Generate recommendations
            recommendations = self._generate_resume_recommendations(
                skills, structure_score, experience, education
            )
            
            # Job matching if job description provided
            if job_description:
                match_score = self._calculate_job_match(resume_text, job_description)
                analysis_details['job_match_score'] = match_score
                
                job_recommendations = self._generate_job_match_recommendations(
                    resume_text, job_description, match_score
                )
                recommendations.extend(job_recommendations)
            
            return AnalysisResult(
                score=overall_score,
                details=analysis_details,
                recommendations=recommendations,
                confidence=0.85,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return AnalysisResult(
                score=0.0,
                details={'error': str(e)},
                recommendations=['Please try uploading the resume again'],
                confidence=0.0,
                timestamp=datetime.now()
            )
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP"""
        try:
            skills = set()
            
            # Technical skills patterns
            tech_patterns = [
                r'\b(?:Python|Java|JavaScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin)\b',
                r'\b(?:React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel)\b',
                r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|Linux)\b',
                r'\b(?:SQL|MongoDB|PostgreSQL|MySQL|Redis|Elasticsearch)\b',
                r'\b(?:Machine Learning|AI|Data Science|Deep Learning|NLP)\b',
                r'\b(?:Agile|Scrum|DevOps|CI/CD|Microservices|REST|GraphQL)\b'
            ]
            
            for pattern in tech_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                skills.update([match.lower() for match in matches])
            
            # Use NER if available
            if self.skill_extractor:
                try:
                    entities = self.skill_extractor(text)
                    for entity in entities:
                        if entity['entity_group'] in ['MISC', 'ORG']:
                            skills.add(entity['word'].lower())
                except Exception as e:
                    logger.warning(f"NER extraction failed: {e}")
            
            # Use spaCy if available
            if self.nlp_model:
                try:
                    doc = self.nlp_model(text)
                    for ent in doc.ents:
                        if ent.label_ in ['PRODUCT', 'ORG', 'LANGUAGE']:
                            skills.add(ent.text.lower())
                except Exception as e:
                    logger.warning(f"spaCy extraction failed: {e}")
            
            return list(skills)
            
        except Exception as e:
            logger.error(f"Error extracting skills: {e}")
            return []
    
    def _analyze_resume_structure(self, text: str) -> float:
        """Analyze resume structure and formatting"""
        try:
            score = 0.0
            
            # Check for essential sections
            sections = {
                'contact': r'(?:email|phone|address|linkedin)',
                'experience': r'(?:experience|work|employment|career)',
                'education': r'(?:education|degree|university|college)',
                'skills': r'(?:skills|technologies|competencies)',
                'summary': r'(?:summary|objective|profile)'
            }
            
            for section, pattern in sections.items():
                if re.search(pattern, text, re.IGNORECASE):
                    score += 0.2
            
            # Check formatting quality
            lines = text.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            
            if len(non_empty_lines) > 10:  # Adequate content
                score += 0.1
            
            # Check for dates (experience timeline)
            date_pattern = r'\b(?:20\d{2}|19\d{2})\b'
            if re.search(date_pattern, text):
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error analyzing structure: {e}")
            return 0.5
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience from resume"""
        try:
            experience = []
            
            # Pattern for job titles and companies
            job_pattern = r'(?:^|\n)([A-Z][^,\n]+?)(?:\s+at\s+|\s+@\s+|\s+-\s+)([A-Z][^,\n]+?)(?:\s*\n|\s*,|\s*\|)'
            matches = re.findall(job_pattern, text, re.MULTILINE)
            
            for title, company in matches:
                experience.append({
                    'title': title.strip(),
                    'company': company.strip(),
                    'extracted_from': 'pattern_matching'
                })
            
            return experience
            
        except Exception as e:
            logger.error(f"Error extracting experience: {e}")
            return []
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information from resume"""
        try:
            education = []
            
            # Pattern for degrees and institutions
            edu_pattern = r'(?:Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|MBA).*?(?:from|at)?\s+([A-Z][^,\n]+?)(?:\s*\n|\s*,|\s*\|)'
            matches = re.findall(edu_pattern, text, re.IGNORECASE)
            
            for institution in matches:
                education.append({
                    'institution': institution.strip(),
                    'extracted_from': 'pattern_matching'
                })
            
            return education
            
        except Exception as e:
            logger.error(f"Error extracting education: {e}")
            return []
    
    def _calculate_resume_score(self, skills: List[str], structure_score: float, 
                               experience: List[Dict], education: List[Dict]) -> float:
        """Calculate overall resume score"""
        try:
            score = 0.0
            
            # Skills score (40%)
            skills_score = min(len(skills) / 10, 1.0) * 0.4
            
            # Structure score (30%)
            structure_weight = structure_score * 0.3
            
            # Experience score (20%)
            experience_score = min(len(experience) / 3, 1.0) * 0.2
            
            # Education score (10%)
            education_score = min(len(education) / 2, 1.0) * 0.1
            
            score = skills_score + structure_weight + experience_score + education_score
            
            return round(score, 2)
            
        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return 0.5
    
    def _generate_resume_recommendations(self, skills: List[str], structure_score: float,
                                       experience: List[Dict], education: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        try:
            if len(skills) < 5:
                recommendations.append("Add more technical skills to strengthen your profile")
            
            if structure_score < 0.7:
                recommendations.append("Improve resume structure by adding clear sections")
            
            if len(experience) < 2:
                recommendations.append("Include more work experience or projects")
            
            if not education:
                recommendations.append("Add education information to complete your profile")
            
            # Always provide positive recommendations
            recommendations.append("Consider adding quantifiable achievements to your experience")
            recommendations.append("Include relevant certifications if available")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Please review and update your resume"]
    
    def _calculate_job_match(self, resume_text: str, job_description: str) -> float:
        """Calculate job matching score"""
        try:
            resume_skills = set(self._extract_skills(resume_text))
            job_skills = set(self._extract_skills(job_description))
            
            if not job_skills:
                return 0.5
            
            matching_skills = resume_skills.intersection(job_skills)
            match_score = len(matching_skills) / len(job_skills)
            
            return round(match_score, 2)
            
        except Exception as e:
            logger.error(f"Error calculating job match: {e}")
            return 0.5
    
    def _generate_job_match_recommendations(self, resume_text: str, 
                                          job_description: str, match_score: float) -> List[str]:
        """Generate job-specific recommendations"""
        recommendations = []
        
        try:
            resume_skills = set(self._extract_skills(resume_text))
            job_skills = set(self._extract_skills(job_description))
            
            missing_skills = job_skills - resume_skills
            
            if missing_skills:
                recommendations.append(f"Consider learning: {', '.join(list(missing_skills)[:3])}")
            
            if match_score < 0.6:
                recommendations.append("Tailor your resume to better match the job requirements")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating job recommendations: {e}")
            return []

# Global AI engine instance
ai_engine = AIEngine()