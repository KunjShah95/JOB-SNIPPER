"""
Advanced Resume Parser Agent
============================

Sophisticated resume parsing with:
- Multi-layered NLP analysis
- Industry-specific pattern recognition
- Contextual skill extraction
- Experience quality assessment
- ATS compatibility scoring
"""

from agents.advanced_agent_base import AdvancedAgentBase, PromptTemplate, ReasoningMode, PromptComplexity
from agents.multi_ai_base import MultiAIAgent
from typing import Dict, Any, List, Optional
import json
import re
import logging
from datetime import datetime, timedelta
import spacy
from collections import Counter

class AdvancedResumeParserAgent(AdvancedAgentBase, MultiAIAgent):
    """
    Advanced resume parser with sophisticated NLP and industry intelligence
    """
    
    def __init__(self):
        AdvancedAgentBase.__init__(
            self,
            name="AdvancedResumeParser",
            version="2.0",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            complexity=PromptComplexity.EXPERT
        )
        MultiAIAgent.__init__(
            self,
            name="AdvancedResumeParser",
            use_gemini=True,
            use_mistral=True,
            return_mode="aggregate"
        )
        
        # Industry-specific skill databases
        self.skill_databases = self._load_skill_databases()
        self.industry_patterns = self._load_industry_patterns()
        self.ats_keywords = self._load_ats_keywords()
        
        # NLP model (optional - fallback to regex if not available)
        self.nlp_model = self._load_nlp_model()

    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Advanced resume processing with multi-layered analysis
        """
        try:
            resume_text = self._extract_resume_text(input_data)
            context = context or {}
            
            # Generate cache key
            cache_key = self._generate_cache_key(resume_text, context)
            
            # Check cache
            if self._cache and cache_key in self._cache:
                self.update_performance_metrics(True, 0, cached=True)
                return self._cache[cache_key]
            
            # Multi-stage parsing
            result = self.execute_with_retry(self._parse_resume_advanced, resume_text, context)
            
            # Cache result
            if self._cache:
                self._cache[cache_key] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Resume parsing failed: {e}")
            return self._get_fallback_result(input_data)

    def _parse_resume_advanced(self, resume_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced multi-stage resume parsing
        """
        # Stage 1: Pre-processing and text cleaning
        cleaned_text = self._preprocess_text(resume_text)
        
        # Stage 2: AI-powered structured extraction
        ai_result = self._ai_extraction(cleaned_text, context)
        
        # Stage 3: NLP enhancement and validation
        enhanced_result = self._enhance_with_nlp(ai_result, cleaned_text)
        
        # Stage 4: Industry-specific analysis
        industry_analysis = self._analyze_industry_fit(enhanced_result, cleaned_text)
        
        # Stage 5: ATS compatibility assessment
        ats_score = self._assess_ats_compatibility(cleaned_text, enhanced_result)
        
        # Stage 6: Quality scoring and recommendations
        quality_assessment = self._assess_resume_quality(enhanced_result, cleaned_text)
        
        # Combine all results
        final_result = {
            "parsed_data": enhanced_result,
            "industry_analysis": industry_analysis,
            "ats_compatibility": ats_score,
            "quality_assessment": quality_assessment,
            "metadata": {
                "parsing_confidence": self._calculate_parsing_confidence(enhanced_result),
                "processing_timestamp": datetime.now().isoformat(),
                "text_length": len(resume_text),
                "sections_identified": len(enhanced_result.keys())
            }
        }
        
        return final_result

    def _ai_extraction(self, resume_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered structured data extraction
        """
        prompt = self.create_advanced_prompt(
            task_description="Extract comprehensive structured information from this resume",
            input_data=resume_text,
            context=context,
            examples=self._get_parsing_examples(),
            constraints=self._get_parsing_constraints()
        )
        
        # Enhanced prompt for resume parsing
        enhanced_prompt = f"""
{prompt}

ADVANCED RESUME PARSING INSTRUCTIONS:

EXTRACTION REQUIREMENTS:
1. PERSONAL INFORMATION:
   - Full name (with confidence score)
   - Professional email addresses
   - Phone numbers (formatted consistently)
   - Location (city, state, country)
   - Professional profiles (LinkedIn, GitHub, Portfolio)
   - Professional headshot URL (if mentioned)

2. PROFESSIONAL SUMMARY:
   - Extract or synthesize professional summary
   - Identify career level (entry, mid, senior, executive)
   - Extract years of experience mentioned
   - Identify key value propositions

3. WORK EXPERIENCE (Enhanced Analysis):
   - Company names with industry classification
   - Job titles with seniority level assessment
   - Employment dates with gap analysis
   - Detailed responsibilities and achievements
   - Quantified accomplishments (numbers, percentages, metrics)
   - Technology stack and tools used
   - Team size and leadership scope
   - Industry context and company size

4. EDUCATION (Comprehensive):
   - Institution names with ranking/reputation
   - Degree types and majors
   - Graduation dates and GPA (if mentioned)
   - Relevant coursework and projects
   - Academic achievements and honors
   - Certifications and licenses
   - Continuing education and professional development

5. SKILLS (Multi-dimensional):
   - Technical skills with proficiency levels
   - Soft skills and leadership abilities
   - Industry-specific competencies
   - Programming languages and frameworks
   - Tools and software proficiency
   - Language skills with fluency levels
   - Certifications and their validity

6. PROJECTS (Detailed Analysis):
   - Project names and descriptions
   - Technologies and methodologies used
   - Role and contributions
   - Project outcomes and impact
   - Team collaboration aspects
   - Links to demos or repositories

7. ACHIEVEMENTS AND AWARDS:
   - Professional recognitions
   - Performance awards
   - Publications and patents
   - Speaking engagements
   - Community contributions

8. ADDITIONAL SECTIONS:
   - Volunteer work and community service
   - Professional memberships
   - Interests and hobbies (if relevant)
   - References (if provided)

ANALYSIS DEPTH:
- Identify implicit skills and competencies
- Assess career progression and growth
- Detect industry transitions and pivots
- Evaluate leadership and management experience
- Analyze technical depth vs. breadth
- Assess cultural fit indicators

OUTPUT FORMAT:
Provide a comprehensive JSON structure with confidence scores for each extracted element.
"""
        
        try:
            ai_response = self.generate_ai_response(enhanced_prompt)
            return self._parse_ai_response(ai_response)
        except Exception as e:
            self.logger.error(f"AI extraction failed: {e}")
            return self._fallback_extraction(resume_text)

    def _enhance_with_nlp(self, ai_result: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """
        Enhance AI results with NLP analysis
        """
        if not self.nlp_model:
            return ai_result
        
        try:
            doc = self.nlp_model(resume_text)
            
            # Extract entities
            entities = self._extract_entities(doc)
            
            # Enhance skills with NLP-detected skills
            ai_result = self._enhance_skills_with_nlp(ai_result, doc)
            
            # Improve experience descriptions
            ai_result = self._enhance_experience_with_nlp(ai_result, doc)
            
            # Add sentiment and tone analysis
            ai_result["communication_style"] = self._analyze_communication_style(doc)
            
            return ai_result
            
        except Exception as e:
            self.logger.error(f"NLP enhancement failed: {e}")
            return ai_result

    def _analyze_industry_fit(self, parsed_data: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """
        Analyze industry fit and career trajectory
        """
        try:
            # Identify primary industries from experience
            industries = self._identify_industries(parsed_data.get("experience", []))
            
            # Analyze skill alignment with industries
            skill_alignment = self._analyze_skill_industry_alignment(
                parsed_data.get("skills", []), industries
            )
            
            # Career progression analysis
            career_progression = self._analyze_career_progression(parsed_data.get("experience", []))
            
            # Industry transition potential
            transition_potential = self._assess_transition_potential(parsed_data)
            
            return {
                "primary_industries": industries,
                "skill_industry_alignment": skill_alignment,
                "career_progression": career_progression,
                "transition_potential": transition_potential,
                "industry_experience_years": self._calculate_industry_experience(parsed_data),
                "cross_functional_skills": self._identify_cross_functional_skills(parsed_data)
            }
            
        except Exception as e:
            self.logger.error(f"Industry analysis failed: {e}")
            return {"error": "Industry analysis unavailable"}

    def _assess_ats_compatibility(self, resume_text: str, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess ATS (Applicant Tracking System) compatibility
        """
        try:
            score = 0
            max_score = 100
            issues = []
            recommendations = []
            
            # Check for standard section headers
            section_score, section_issues = self._check_section_headers(resume_text)
            score += section_score
            issues.extend(section_issues)
            
            # Check for keyword density
            keyword_score, keyword_issues = self._check_keyword_density(resume_text, parsed_data)
            score += keyword_score
            issues.extend(keyword_issues)
            
            # Check formatting compatibility
            format_score, format_issues = self._check_format_compatibility(resume_text)
            score += format_score
            issues.extend(format_issues)
            
            # Check for contact information accessibility
            contact_score, contact_issues = self._check_contact_accessibility(parsed_data)
            score += contact_score
            issues.extend(contact_issues)
            
            # Generate recommendations
            recommendations = self._generate_ats_recommendations(issues)
            
            return {
                "overall_score": min(score, max_score),
                "grade": self._get_ats_grade(score),
                "issues": issues,
                "recommendations": recommendations,
                "detailed_scores": {
                    "section_headers": section_score,
                    "keyword_density": keyword_score,
                    "formatting": format_score,
                    "contact_info": contact_score
                }
            }
            
        except Exception as e:
            self.logger.error(f"ATS assessment failed: {e}")
            return {"error": "ATS assessment unavailable"}

    def _assess_resume_quality(self, parsed_data: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """
        Comprehensive resume quality assessment
        """
        try:
            quality_metrics = {}
            
            # Content quality
            quality_metrics["content_quality"] = self._assess_content_quality(parsed_data, resume_text)
            
            # Structure and organization
            quality_metrics["structure_quality"] = self._assess_structure_quality(resume_text)
            
            # Professional presentation
            quality_metrics["presentation_quality"] = self._assess_presentation_quality(resume_text)
            
            # Completeness assessment
            quality_metrics["completeness"] = self._assess_completeness(parsed_data)
            
            # Impact and achievements
            quality_metrics["impact_score"] = self._assess_impact_score(parsed_data)
            
            # Overall quality score
            overall_score = self._calculate_overall_quality_score(quality_metrics)
            
            return {
                "overall_score": overall_score,
                "grade": self._get_quality_grade(overall_score),
                "detailed_metrics": quality_metrics,
                "improvement_suggestions": self._generate_improvement_suggestions(quality_metrics),
                "strengths": self._identify_resume_strengths(quality_metrics),
                "weaknesses": self._identify_resume_weaknesses(quality_metrics)
            }
            
        except Exception as e:
            self.logger.error(f"Quality assessment failed: {e}")
            return {"error": "Quality assessment unavailable"}

    def get_specialized_prompt_template(self) -> PromptTemplate:
        """
        Get resume parser specific prompt template
        """
        return PromptTemplate(
            system_prompt=self._build_system_prompt(),
            user_prompt="Parse and analyze the provided resume comprehensively",
            reasoning_mode=ReasoningMode.CHAIN_OF_THOUGHT,
            complexity=PromptComplexity.EXPERT,
            context_variables={
                "industry_focus": "technology",
                "experience_level": "all",
                "parsing_depth": "comprehensive"
            },
            validation_rules=[
                "must_contain_personal_info",
                "must_have_confidence_scores",
                "must_include_metadata"
            ],
            examples=self._get_parsing_examples(),
            constraints=self._get_parsing_constraints()
        )

    # Helper methods for various functionalities
    def _load_skill_databases(self) -> Dict[str, List[str]]:
        """Load industry-specific skill databases"""
        return {
            "technology": [
                "Python", "Java", "JavaScript", "React", "Node.js", "AWS", "Docker",
                "Kubernetes", "Machine Learning", "Data Science", "AI", "SQL", "NoSQL"
            ],
            "marketing": [
                "SEO", "SEM", "Google Analytics", "Social Media Marketing", "Content Marketing",
                "Email Marketing", "Marketing Automation", "A/B Testing"
            ],
            "finance": [
                "Financial Modeling", "Risk Management", "Portfolio Management", "Excel",
                "Bloomberg Terminal", "Financial Analysis", "Accounting", "Compliance"
            ]
        }

    def _load_industry_patterns(self) -> Dict[str, List[str]]:
        """Load industry-specific patterns and keywords"""
        return {
            "technology": ["software", "development", "engineering", "programming", "tech"],
            "finance": ["financial", "banking", "investment", "trading", "accounting"],
            "healthcare": ["medical", "clinical", "patient", "healthcare", "pharmaceutical"],
            "marketing": ["marketing", "advertising", "brand", "campaign", "digital"]
        }

    def _load_ats_keywords(self) -> List[str]:
        """Load ATS-friendly keywords and phrases"""
        return [
            "experience", "skills", "education", "achievements", "responsibilities",
            "managed", "developed", "implemented", "improved", "increased", "decreased"
        ]

    def _load_nlp_model(self):
        """Load NLP model (spaCy) if available"""
        try:
            import spacy
            return spacy.load("en_core_web_sm")
        except:
            self.logger.warning("spaCy model not available, using fallback methods")
            return None

    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess resume text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common formatting issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Normalize bullet points
        text = re.sub(r'[•·▪▫◦‣⁃]', '•', text)
        
        return text.strip()

    def _extract_resume_text(self, input_data: Dict[str, Any]) -> str:
        """Extract resume text from various input formats"""
        if isinstance(input_data, str):
            return input_data
        elif isinstance(input_data, dict):
            return input_data.get('resume_text', input_data.get('text', str(input_data)))
        else:
            return str(input_data)

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Clean response
            cleaned = re.sub(r'```json\s*', '', response)
            cleaned = re.sub(r'```\s*$', '', cleaned)
            
            # Find JSON object
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            self.logger.error(f"Failed to parse AI response: {e}")
            return {}

    def _fallback_extraction(self, resume_text: str) -> Dict[str, Any]:
        """Fallback extraction using regex patterns"""
        return {
            "personal_info": self._extract_personal_info_regex(resume_text),
            "experience": self._extract_experience_regex(resume_text),
            "education": self._extract_education_regex(resume_text),
            "skills": self._extract_skills_regex(resume_text),
            "confidence_score": 60  # Lower confidence for fallback
        }

    def _extract_personal_info_regex(self, text: str) -> Dict[str, Any]:
        """Extract personal information using regex"""
        info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            info["email"] = emails[0]
        
        # Phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            info["phone"] = ''.join(phones[0])
        
        return info

    def _extract_experience_regex(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience using regex patterns"""
        # This is a simplified version - in practice, this would be much more sophisticated
        return []

    def _extract_education_regex(self, text: str) -> List[Dict[str, Any]]:
        """Extract education using regex patterns"""
        # This is a simplified version - in practice, this would be much more sophisticated
        return []

    def _extract_skills_regex(self, text: str) -> List[str]:
        """Extract skills using regex and keyword matching"""
        skills = []
        for category, skill_list in self.skill_databases.items():
            for skill in skill_list:
                if skill.lower() in text.lower():
                    skills.append(skill)
        return list(set(skills))

    def _get_parsing_examples(self) -> List[Dict[str, str]]:
        """Get example inputs and outputs for parsing"""
        return [
            {
                "input": "John Doe, Software Engineer with 5 years experience...",
                "output": '{"personal_info": {"name": "John Doe"}, "experience": [...]}'
            }
        ]

    def _get_parsing_constraints(self) -> List[str]:
        """Get parsing constraints and requirements"""
        return [
            "Extract all personal information accurately",
            "Maintain chronological order for experience",
            "Include confidence scores for all extractions",
            "Preserve original formatting where relevant"
        ]

    def _calculate_parsing_confidence(self, parsed_data: Dict[str, Any]) -> float:
        """Calculate overall parsing confidence score"""
        # Implement confidence calculation logic
        return 85.0

    def _get_fallback_result(self, input_data: Any) -> Dict[str, Any]:
        """Get fallback result when all parsing fails"""
        return {
            "error": "Resume parsing failed",
            "parsed_data": {},
            "confidence_score": 0,
            "recommendations": ["Please check resume format and try again"]
        }