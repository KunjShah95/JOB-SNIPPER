"""
Enhanced AI Engine with Advanced Features for Job Snipper AI
Includes real AI capabilities, job matching, and skill analysis
"""
import os
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import numpy as np
from collections import Counter

# AI and NLP imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Enhanced analysis result with comprehensive data"""
    score: float
    details: Dict[str, Any]
    recommendations: List[str]
    confidence: float
    timestamp: datetime
    job_match_score: Optional[float] = None
    skill_gaps: Optional[List[str]] = None
    improvement_areas: Optional[List[str]] = None

class EnhancedAIEngine:
    """Enhanced AI Engine with real capabilities and fallbacks"""
    
    def __init__(self):
        self.openai_client = None
        self.nlp_model = None
        self.skill_extractor = None
        self.sentence_model = None
        self.skill_database = self._load_skill_database()
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models with fallbacks"""
        try:
            # Initialize OpenAI
            if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                logger.info("✅ OpenAI client initialized")
            else:
                logger.warning("⚠️ OpenAI not available - using fallback methods")
            
            # Initialize spaCy
            if SPACY_AVAILABLE:
                try:
                    self.nlp_model = spacy.load("en_core_web_sm")
                    logger.info("✅ spaCy model loaded")
                except OSError:
                    logger.warning("⚠️ spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            
            # Initialize transformers
            if TRANSFORMERS_AVAILABLE:
                try:
                    self.skill_extractor = pipeline(
                        "ner",
                        model="dbmdz/bert-large-cased-finetuned-conll03-english",
                        aggregation_strategy="simple"
                    )
                    logger.info("✅ Skill extraction model loaded")
                except Exception as e:
                    logger.warning(f"⚠️ Could not load skill extraction model: {e}")
            
            # Initialize sentence transformers
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                try:
                    self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                    logger.info("✅ Sentence transformer loaded")
                except Exception as e:
                    logger.warning(f"⚠️ Could not load sentence transformer: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Error initializing AI models: {e}")
    
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skill database"""
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sqlite', 'cassandra', 'dynamodb', 'neo4j'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'kubernetes', 'docker', 'terraform', 'ansible'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'pandas', 'numpy', 'scikit-learn',
                'tensorflow', 'pytorch', 'keras', 'jupyter', 'tableau', 'power bi'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jenkins', 'docker', 'kubernetes',
                'jira', 'confluence', 'slack', 'figma', 'photoshop'
            ]
        }
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> AnalysisResult:
        """
        Comprehensive resume analysis with enhanced features
        """
        try:
            analysis_details = {}
            recommendations = []
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(resume_text)
            
            # Extract skills using multiple methods
            skills = self._extract_skills_comprehensive(cleaned_text)
            analysis_details['extracted_skills'] = skills
            
            # Analyze resume structure
            structure_score = self._analyze_resume_structure(cleaned_text)
            analysis_details['structure_score'] = structure_score
            
            # Extract experience and education
            experience = self._extract_experience(cleaned_text)
            education = self._extract_education(cleaned_text)
            analysis_details['experience'] = experience
            analysis_details['education'] = education
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(
                skills, structure_score, experience, education
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                skills, structure_score, experience, education
            )
            
            # Job matching if job description provided
            job_match_score = None
            skill_gaps = None
            if job_description:
                job_match_score, skill_gaps = self._analyze_job_match(
                    cleaned_text, job_description, skills
                )
                analysis_details['job_match_score'] = job_match_score
                analysis_details['skill_gaps'] = skill_gaps
            
            # Calculate confidence based on available models
            confidence = self._calculate_confidence()
            
            return AnalysisResult(
                score=overall_score,
                details=analysis_details,
                recommendations=recommendations,
                confidence=confidence,
                timestamp=datetime.now(),
                job_match_score=job_match_score,
                skill_gaps=skill_gaps
            )
            
        except Exception as e:
            logger.error(f"❌ Error in resume analysis: {e}")
            # Return fallback result
            return self._create_fallback_result(resume_text)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)@]', ' ', text)
        
        # Normalize common variations
        text = re.sub(r'\b(javascript|js)\b', 'javascript', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(typescript|ts)\b', 'typescript', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _extract_skills_comprehensive(self, text: str) -> List[str]:
        """Extract skills using multiple methods"""
        skills = set()
        text_lower = text.lower()
        
        # Method 1: Pattern matching with skill database
        for category, skill_list in self.skill_database.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.add(skill)
        
        # Method 2: NER with transformers (if available)
        if self.skill_extractor:
            try:
                entities = self.skill_extractor(text)
                for entity in entities:
                    if entity['entity_group'] in ['MISC', 'ORG'] and len(entity['word']) > 2:
                        skills.add(entity['word'].lower())
            except Exception as e:
                logger.warning(f"⚠️ NER extraction failed: {e}")
        
        # Method 3: spaCy NLP (if available)
        if self.nlp_model:
            try:
                doc = self.nlp_model(text)
                for ent in doc.ents:
                    if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE'] and len(ent.text) > 2:
                        skills.add(ent.text.lower())
            except Exception as e:
                logger.warning(f"⚠️ spaCy extraction failed: {e}")
        
        # Method 4: Regex patterns for common skills
        skill_patterns = [
            r'\b(python|java|javascript|typescript|c\+\+|c#)\b',
            r'\b(react|angular|vue|node\.?js|express)\b',
            r'\b(aws|azure|gcp|docker|kubernetes)\b',
            r'\b(mysql|postgresql|mongodb|redis)\b',
            r'\b(git|github|gitlab|jenkins)\b'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            skills.update(matches)
        
        return list(skills)[:20]  # Limit to top 20 skills
    
    def _analyze_resume_structure(self, text: str) -> float:
        """Analyze resume structure and format"""
        score = 0.0
        
        # Check for common resume sections
        sections = [
            'experience', 'education', 'skills', 'projects',
            'work experience', 'employment', 'qualifications'
        ]
        
        found_sections = sum(1 for section in sections if section in text.lower())
        score += min(found_sections / len(sections), 0.4)  # Max 40% for sections
        
        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if re.search(email_pattern, text):
            score += 0.15
        if re.search(phone_pattern, text):
            score += 0.15
        
        # Check for dates (experience timeline)
        date_patterns = [
            r'\b\d{4}\s*[-–]\s*\d{4}\b',
            r'\b\d{4}\s*[-–]\s*present\b',
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\b'
        ]
        
        date_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in date_patterns)
        if date_matches >= 2:
            score += 0.2
        
        # Check for quantified achievements
        achievement_patterns = [
            r'\b\d+%\b', r'\b\$\d+\b', r'\b\d+\s*(million|thousand|k)\b',
            r'\bincreased?\s+\w+\s+by\s+\d+', r'\breduced?\s+\w+\s+by\s+\d+'
        ]
        
        achievement_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in achievement_patterns)
        if achievement_matches >= 1:
            score += 0.1
        
        return min(score, 1.0)
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience information"""
        experience = []
        
        # Simple pattern matching for job titles and companies
        job_patterns = [
            r'(software engineer|developer|analyst|manager|director|lead|senior|junior)\s+at\s+([A-Za-z\s&]+)',
            r'([A-Za-z\s&]+)\s*[-–]\s*(software engineer|developer|analyst|manager|director)'
        ]
        
        for pattern in job_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:5]:  # Limit to 5 experiences
                if len(match) == 2:
                    experience.append({
                        'title': match[0].strip(),
                        'company': match[1].strip()
                    })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        
        # Pattern for degrees and institutions
        degree_patterns = [
            r'(bachelor|master|phd|doctorate|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?)\s+.*?\s+from\s+([A-Za-z\s&]+)',
            r'([A-Za-z\s&]+)\s+university',
            r'([A-Za-z\s&]+)\s+college'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:3]:  # Limit to 3 education entries
                if isinstance(match, tuple) and len(match) >= 2:
                    education.append({
                        'degree': match[0].strip(),
                        'institution': match[1].strip()
                    })
                elif isinstance(match, str):
                    education.append({
                        'institution': match.strip()
                    })
        
        return education
    
    def _calculate_overall_score(self, skills: List[str], structure_score: float,
                               experience: List[Dict], education: List[Dict]) -> float:
        """Calculate overall resume score"""
        # Weighted scoring
        skill_score = min(len(skills) / 10, 1.0) * 0.4  # 40% weight
        structure_weight = structure_score * 0.3  # 30% weight
        experience_score = min(len(experience) / 3, 1.0) * 0.2  # 20% weight
        education_score = min(len(education) / 2, 1.0) * 0.1  # 10% weight
        
        total_score = skill_score + structure_weight + experience_score + education_score
        return min(total_score, 1.0)
    
    def _generate_recommendations(self, skills: List[str], structure_score: float,
                                experience: List[Dict], education: List[Dict]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Skill-based recommendations
        if len(skills) < 5:
            recommendations.append("Add more technical skills to strengthen your profile")
        
        # Structure recommendations
        if structure_score < 0.6:
            recommendations.append("Improve resume structure with clear sections and contact info")
        
        # Experience recommendations
        if len(experience) < 2:
            recommendations.append("Include more work experience or relevant projects")
        
        # Quantification recommendations
        recommendations.append("Add quantified achievements (percentages, numbers, impact)")
        
        # Skill progression recommendations
        if 'python' in [s.lower() for s in skills]:
            recommendations.append("Consider adding Django, Flask, or FastAPI to complement Python skills")
        
        if 'javascript' in [s.lower() for s in skills]:
            recommendations.append("Add React, Node.js, or TypeScript to enhance JavaScript expertise")
        
        # General recommendations
        recommendations.extend([
            "Use action verbs to describe your accomplishments",
            "Tailor your resume to specific job requirements",
            "Keep your resume to 1-2 pages for optimal readability"
        ])
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def _analyze_job_match(self, resume_text: str, job_description: str,
                          resume_skills: List[str]) -> Tuple[float, List[str]]:
        """Analyze job matching with skill gap analysis"""
        try:
            # Extract skills from job description
            job_skills = self._extract_skills_comprehensive(job_description)
            
            # Calculate skill overlap
            resume_skills_lower = [s.lower() for s in resume_skills]
            job_skills_lower = [s.lower() for s in job_skills]
            
            common_skills = set(resume_skills_lower) & set(job_skills_lower)
            skill_match_score = len(common_skills) / max(len(job_skills_lower), 1)
            
            # Identify skill gaps
            skill_gaps = [s for s in job_skills if s.lower() not in resume_skills_lower]
            
            # Use sentence similarity if available
            if self.sentence_model:
                try:
                    resume_embedding = self.sentence_model.encode([resume_text])
                    job_embedding = self.sentence_model.encode([job_description])
                    
                    # Calculate cosine similarity
                    similarity = np.dot(resume_embedding[0], job_embedding[0]) / (
                        np.linalg.norm(resume_embedding[0]) * np.linalg.norm(job_embedding[0])
                    )
                    
                    # Combine skill match and semantic similarity
                    final_score = (skill_match_score * 0.6) + (similarity * 0.4)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Sentence similarity failed: {e}")
                    final_score = skill_match_score
            else:
                final_score = skill_match_score
            
            return min(final_score, 1.0), skill_gaps[:10]  # Limit gaps to 10
            
        except Exception as e:
            logger.error(f"❌ Job match analysis failed: {e}")
            return 0.5, []  # Fallback score
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence based on available models"""
        confidence = 0.5  # Base confidence
        
        if self.openai_client:
            confidence += 0.2
        if self.nlp_model:
            confidence += 0.15
        if self.skill_extractor:
            confidence += 0.1
        if self.sentence_model:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def _create_fallback_result(self, resume_text: str) -> AnalysisResult:
        """Create fallback result when AI models fail"""
        # Basic text analysis
        word_count = len(resume_text.split())
        basic_score = min(word_count / 500, 1.0)  # Assume 500 words is good
        
        return AnalysisResult(
            score=basic_score,
            details={
                'extracted_skills': [],
                'structure_score': 0.5,
                'experience': [],
                'education': [],
                'word_count': word_count
            },
            recommendations=[
                "Upload a more detailed resume for better analysis",
                "Ensure your resume includes skills, experience, and education sections",
                "Add quantified achievements to strengthen your profile"
            ],
            confidence=0.3,
            timestamp=datetime.now()
        )

# Create global instance
enhanced_ai_engine = EnhancedAIEngine()