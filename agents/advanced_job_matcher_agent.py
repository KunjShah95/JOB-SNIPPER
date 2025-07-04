"""
Advanced Job Matcher Agent
==========================

Sophisticated job matching with:
- Multi-dimensional compatibility scoring
- Skills gap analysis with learning paths
- Cultural fit assessment
- Salary expectation alignment
- Career progression mapping
- Industry trend integration
"""

from agents.advanced_agent_base import AdvancedAgentBase, PromptTemplate, ReasoningMode, PromptComplexity
from agents.multi_ai_base import MultiAIAgent
from typing import Dict, Any, List, Optional, Tuple
import json
import logging
import numpy as np
from datetime import datetime
from collections import defaultdict
import math

class AdvancedJobMatcherAgent(AdvancedAgentBase, MultiAIAgent):
    """
    Advanced job matching with ML-powered algorithms and comprehensive analysis
    """
    
    def __init__(self):
        AdvancedAgentBase.__init__(
            self,
            name="AdvancedJobMatcher",
            version="2.0",
            reasoning_mode=ReasoningMode.MULTI_PERSPECTIVE,
            complexity=PromptComplexity.EXPERT
        )
        MultiAIAgent.__init__(
            self,
            name="AdvancedJobMatcher",
            use_gemini=True,
            use_mistral=True,
            return_mode="aggregate"
        )
        
        # Load matching databases and models
        self.skill_taxonomy = self._load_skill_taxonomy()
        self.industry_data = self._load_industry_data()
        self.salary_data = self._load_salary_data()
        self.company_culture_data = self._load_company_culture_data()
        self.career_progression_paths = self._load_career_paths()
        
        # Matching weights and parameters
        self.matching_weights = {
            "skills_match": 0.35,
            "experience_match": 0.25,
            "education_match": 0.15,
            "cultural_fit": 0.10,
            "location_match": 0.05,
            "salary_alignment": 0.10
        }

    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Advanced job matching with comprehensive analysis
        """
        try:
            # Extract candidate profile and job requirements
            candidate_profile = self._extract_candidate_profile(input_data)
            job_requirements = self._extract_job_requirements(input_data, context)
            
            # Generate cache key
            cache_key = self._generate_cache_key(
                json.dumps(candidate_profile) + json.dumps(job_requirements), 
                context
            )
            
            # Check cache
            if self._cache and cache_key in self._cache:
                self.update_performance_metrics(True, 0, cached=True)
                return self._cache[cache_key]
            
            # Perform comprehensive matching
            result = self.execute_with_retry(
                self._perform_advanced_matching, 
                candidate_profile, 
                job_requirements, 
                context or {}
            )
            
            # Cache result
            if self._cache:
                self._cache[cache_key] = result
            
            return result
            
        except Exception as e:
            self.logger.error(f"Job matching failed: {e}")
            return self._get_fallback_matching_result()

    def _perform_advanced_matching(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive job matching analysis
        """
        # Stage 1: AI-powered compatibility analysis
        ai_analysis = self._ai_compatibility_analysis(candidate_profile, job_requirements, context)
        
        # Stage 2: Skills matching with gap analysis
        skills_analysis = self._analyze_skills_compatibility(candidate_profile, job_requirements)
        
        # Stage 3: Experience and career level matching
        experience_analysis = self._analyze_experience_compatibility(candidate_profile, job_requirements)
        
        # Stage 4: Cultural fit assessment
        cultural_fit = self._assess_cultural_fit(candidate_profile, job_requirements)
        
        # Stage 5: Salary and compensation alignment
        salary_analysis = self._analyze_salary_alignment(candidate_profile, job_requirements)
        
        # Stage 6: Career progression potential
        career_potential = self._assess_career_progression_potential(candidate_profile, job_requirements)
        
        # Stage 7: Location and remote work compatibility
        location_analysis = self._analyze_location_compatibility(candidate_profile, job_requirements)
        
        # Stage 8: Calculate overall match score
        overall_score = self._calculate_overall_match_score({
            "skills": skills_analysis["match_score"],
            "experience": experience_analysis["match_score"],
            "cultural_fit": cultural_fit["match_score"],
            "salary": salary_analysis["match_score"],
            "location": location_analysis["match_score"]
        })
        
        # Stage 9: Generate recommendations and action items
        recommendations = self._generate_matching_recommendations(
            candidate_profile, job_requirements, {
                "skills": skills_analysis,
                "experience": experience_analysis,
                "cultural_fit": cultural_fit,
                "salary": salary_analysis,
                "career_potential": career_potential
            }
        )
        
        return {
            "overall_match": {
                "score": overall_score,
                "grade": self._get_match_grade(overall_score),
                "confidence": ai_analysis.get("confidence", 85)
            },
            "detailed_analysis": {
                "skills_compatibility": skills_analysis,
                "experience_compatibility": experience_analysis,
                "cultural_fit_assessment": cultural_fit,
                "salary_alignment": salary_analysis,
                "career_progression_potential": career_potential,
                "location_compatibility": location_analysis
            },
            "ai_insights": ai_analysis,
            "recommendations": recommendations,
            "action_items": self._generate_action_items(skills_analysis, experience_analysis),
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "matching_algorithm_version": "2.0",
                "data_sources": ["ai_analysis", "skill_taxonomy", "industry_data"]
            }
        }

    def _ai_compatibility_analysis(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI-powered comprehensive compatibility analysis
        """
        prompt = self.create_advanced_prompt(
            task_description="Analyze job-candidate compatibility with deep insights",
            input_data={
                "candidate_profile": candidate_profile,
                "job_requirements": job_requirements
            },
            context=context,
            examples=self._get_matching_examples(),
            constraints=self._get_matching_constraints()
        )
        
        enhanced_prompt = f"""
{prompt}

ADVANCED JOB MATCHING ANALYSIS:

COMPREHENSIVE COMPATIBILITY ASSESSMENT:

1. SKILLS ALIGNMENT ANALYSIS:
   - Technical skills match percentage
   - Soft skills compatibility
   - Leadership and management capabilities
   - Industry-specific competencies
   - Emerging skills and future readiness
   - Skill transferability assessment

2. EXPERIENCE RELEVANCE EVALUATION:
   - Years of relevant experience vs. requirements
   - Industry experience alignment
   - Company size and culture experience
   - Role progression and career trajectory
   - Project complexity and scope match
   - Team leadership and collaboration experience

3. CULTURAL AND ORGANIZATIONAL FIT:
   - Work style preferences alignment
   - Company values compatibility
   - Team dynamics fit
   - Communication style match
   - Innovation and change adaptability
   - Work-life balance expectations

4. GROWTH AND DEVELOPMENT POTENTIAL:
   - Learning agility and adaptability
   - Career advancement potential
   - Skill development opportunities
   - Long-term retention likelihood
   - Contribution to team growth
   - Knowledge transfer capabilities

5. COMPENSATION AND BENEFITS ALIGNMENT:
   - Salary expectations vs. budget
   - Benefits package compatibility
   - Equity and bonus structure fit
   - Career advancement opportunities
   - Professional development support
   - Work flexibility requirements

6. RISK ASSESSMENT:
   - Overqualification risk
   - Underqualification concerns
   - Cultural misalignment risks
   - Retention probability
   - Performance prediction
   - Integration challenges

ANALYSIS FRAMEWORK:
- Use multi-dimensional scoring (0-100 for each category)
- Provide confidence intervals for predictions
- Identify potential red flags and concerns
- Highlight unique strengths and differentiators
- Assess both short-term fit and long-term potential
- Consider market conditions and industry trends

OUTPUT REQUIREMENTS:
Provide detailed JSON analysis with:
- Overall compatibility score (0-100)
- Category-specific scores and explanations
- Strengths and weaknesses identification
- Risk factors and mitigation strategies
- Recommendations for both candidate and employer
- Confidence levels for all assessments
"""
        
        try:
            ai_response = self.generate_ai_response(enhanced_prompt)
            return self._parse_ai_response(ai_response)
        except Exception as e:
            self.logger.error(f"AI compatibility analysis failed: {e}")
            return {"error": "AI analysis unavailable", "confidence": 50}

    def _analyze_skills_compatibility(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Comprehensive skills compatibility analysis
        """
        try:
            candidate_skills = self._normalize_skills(candidate_profile.get("skills", []))
            required_skills = self._normalize_skills(job_requirements.get("required_skills", []))
            preferred_skills = self._normalize_skills(job_requirements.get("preferred_skills", []))
            
            # Calculate skill matches
            required_matches = self._calculate_skill_matches(candidate_skills, required_skills)
            preferred_matches = self._calculate_skill_matches(candidate_skills, preferred_skills)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(candidate_skills, required_skills + preferred_skills)
            
            # Calculate transferable skills
            transferable_skills = self._identify_transferable_skills(candidate_skills, required_skills)
            
            # Generate learning path for gaps
            learning_path = self._generate_learning_path(skill_gaps)
            
            # Calculate overall skills match score
            required_score = (len(required_matches) / max(len(required_skills), 1)) * 100
            preferred_score = (len(preferred_matches) / max(len(preferred_skills), 1)) * 100
            overall_score = (required_score * 0.7) + (preferred_score * 0.3)
            
            return {
                "match_score": overall_score,
                "required_skills_match": {
                    "score": required_score,
                    "matched_skills": required_matches,
                    "missing_skills": [skill for skill in required_skills if skill not in required_matches]
                },
                "preferred_skills_match": {
                    "score": preferred_score,
                    "matched_skills": preferred_matches,
                    "missing_skills": [skill for skill in preferred_skills if skill not in preferred_matches]
                },
                "skill_gaps": skill_gaps,
                "transferable_skills": transferable_skills,
                "learning_path": learning_path,
                "additional_skills": [skill for skill in candidate_skills if skill not in required_skills + preferred_skills]
            }
            
        except Exception as e:
            self.logger.error(f"Skills analysis failed: {e}")
            return {"match_score": 0, "error": "Skills analysis failed"}

    def _analyze_experience_compatibility(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze experience level and relevance compatibility
        """
        try:
            candidate_experience = candidate_profile.get("experience", [])
            required_years = job_requirements.get("years_experience", 0)
            required_level = job_requirements.get("experience_level", "mid")
            
            # Calculate total years of experience
            total_years = self._calculate_total_experience_years(candidate_experience)
            
            # Calculate relevant experience
            relevant_years = self._calculate_relevant_experience_years(
                candidate_experience, 
                job_requirements.get("industry", ""), 
                job_requirements.get("role_type", "")
            )
            
            # Assess experience level match
            level_match = self._assess_experience_level_match(candidate_experience, required_level)
            
            # Analyze career progression
            progression_analysis = self._analyze_career_progression(candidate_experience)
            
            # Calculate experience match score
            years_score = min((relevant_years / max(required_years, 1)) * 100, 100)
            level_score = level_match["score"]
            progression_score = progression_analysis["score"]
            
            overall_score = (years_score * 0.4) + (level_score * 0.4) + (progression_score * 0.2)
            
            return {
                "match_score": overall_score,
                "total_years": total_years,
                "relevant_years": relevant_years,
                "required_years": required_years,
                "experience_level_match": level_match,
                "career_progression": progression_analysis,
                "industry_experience": self._analyze_industry_experience(candidate_experience),
                "leadership_experience": self._analyze_leadership_experience(candidate_experience)
            }
            
        except Exception as e:
            self.logger.error(f"Experience analysis failed: {e}")
            return {"match_score": 0, "error": "Experience analysis failed"}

    def _assess_cultural_fit(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess cultural fit between candidate and organization
        """
        try:
            # Extract cultural indicators from candidate profile
            candidate_culture = self._extract_cultural_indicators(candidate_profile)
            
            # Extract company culture requirements
            company_culture = job_requirements.get("company_culture", {})
            
            # Analyze work style compatibility
            work_style_match = self._analyze_work_style_compatibility(candidate_culture, company_culture)
            
            # Assess values alignment
            values_alignment = self._assess_values_alignment(candidate_culture, company_culture)
            
            # Evaluate communication style fit
            communication_fit = self._evaluate_communication_fit(candidate_culture, company_culture)
            
            # Calculate overall cultural fit score
            overall_score = (
                work_style_match["score"] * 0.4 +
                values_alignment["score"] * 0.4 +
                communication_fit["score"] * 0.2
            )
            
            return {
                "match_score": overall_score,
                "work_style_compatibility": work_style_match,
                "values_alignment": values_alignment,
                "communication_fit": communication_fit,
                "cultural_strengths": self._identify_cultural_strengths(candidate_culture, company_culture),
                "potential_challenges": self._identify_cultural_challenges(candidate_culture, company_culture)
            }
            
        except Exception as e:
            self.logger.error(f"Cultural fit analysis failed: {e}")
            return {"match_score": 75, "error": "Cultural fit analysis unavailable"}

    def _analyze_salary_alignment(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze salary expectations and budget alignment
        """
        try:
            candidate_salary_expectation = candidate_profile.get("salary_expectation")
            job_salary_range = job_requirements.get("salary_range", {})
            
            if not candidate_salary_expectation or not job_salary_range:
                return {"match_score": 80, "note": "Salary information not available"}
            
            # Calculate alignment score
            alignment_score = self._calculate_salary_alignment_score(
                candidate_salary_expectation, 
                job_salary_range
            )
            
            # Market analysis
            market_analysis = self._analyze_market_salary(
                job_requirements.get("role_title", ""),
                job_requirements.get("location", ""),
                candidate_profile.get("experience_years", 0)
            )
            
            return {
                "match_score": alignment_score,
                "candidate_expectation": candidate_salary_expectation,
                "job_budget": job_salary_range,
                "market_analysis": market_analysis,
                "negotiation_potential": self._assess_negotiation_potential(
                    candidate_salary_expectation, job_salary_range, market_analysis
                )
            }
            
        except Exception as e:
            self.logger.error(f"Salary analysis failed: {e}")
            return {"match_score": 80, "error": "Salary analysis unavailable"}

    def _assess_career_progression_potential(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess career progression and growth potential
        """
        try:
            # Analyze current career trajectory
            current_trajectory = self._analyze_current_trajectory(candidate_profile)
            
            # Identify growth opportunities in the role
            growth_opportunities = self._identify_growth_opportunities(job_requirements)
            
            # Assess skill development potential
            skill_development = self._assess_skill_development_potential(candidate_profile, job_requirements)
            
            # Calculate progression potential score
            progression_score = (
                current_trajectory["score"] * 0.3 +
                growth_opportunities["score"] * 0.4 +
                skill_development["score"] * 0.3
            )
            
            return {
                "progression_score": progression_score,
                "current_trajectory": current_trajectory,
                "growth_opportunities": growth_opportunities,
                "skill_development_potential": skill_development,
                "recommended_career_path": self._recommend_career_path(candidate_profile, job_requirements),
                "timeline_projections": self._project_career_timeline(candidate_profile, job_requirements)
            }
            
        except Exception as e:
            self.logger.error(f"Career progression analysis failed: {e}")
            return {"progression_score": 75, "error": "Career progression analysis unavailable"}

    def _analyze_location_compatibility(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze location and remote work compatibility
        """
        try:
            candidate_location = candidate_profile.get("location", "")
            job_location = job_requirements.get("location", "")
            remote_options = job_requirements.get("remote_work", {})
            
            # Calculate location match
            location_match = self._calculate_location_match(candidate_location, job_location)
            
            # Assess remote work compatibility
            remote_compatibility = self._assess_remote_work_compatibility(
                candidate_profile, remote_options
            )
            
            # Calculate overall location score
            if remote_options.get("fully_remote", False):
                overall_score = 100
            elif remote_options.get("hybrid", False):
                overall_score = max(location_match * 0.5 + 50, 75)
            else:
                overall_score = location_match
            
            return {
                "match_score": overall_score,
                "location_match": location_match,
                "remote_compatibility": remote_compatibility,
                "relocation_required": location_match < 80 and not remote_options.get("fully_remote", False),
                "commute_analysis": self._analyze_commute_feasibility(candidate_location, job_location)
            }
            
        except Exception as e:
            self.logger.error(f"Location analysis failed: {e}")
            return {"match_score": 85, "error": "Location analysis unavailable"}

    def _calculate_overall_match_score(self, component_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall match score
        """
        total_score = 0
        total_weight = 0
        
        for component, score in component_scores.items():
            if component in self.matching_weights:
                weight = self.matching_weights[component]
                total_score += score * weight
                total_weight += weight
        
        return total_score / max(total_weight, 1)

    def _generate_matching_recommendations(
        self, 
        candidate_profile: Dict[str, Any], 
        job_requirements: Dict[str, Any], 
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive matching recommendations
        """
        recommendations = {
            "for_candidate": [],
            "for_employer": [],
            "interview_focus_areas": [],
            "development_opportunities": []
        }
        
        # Candidate recommendations
        skills_analysis = analysis_results.get("skills", {})
        if skills_analysis.get("skill_gaps"):
            recommendations["for_candidate"].append({
                "type": "skill_development",
                "priority": "high",
                "action": f"Develop skills in: {', '.join(skills_analysis['skill_gaps'][:3])}",
                "timeline": "1-3 months",
                "resources": skills_analysis.get("learning_path", [])
            })
        
        # Employer recommendations
        experience_analysis = analysis_results.get("experience", {})
        if experience_analysis.get("match_score", 0) > 85:
            recommendations["for_employer"].append({
                "type": "strong_match",
                "priority": "high",
                "action": "Fast-track this candidate through the interview process",
                "reasoning": "Excellent experience match with strong career progression"
            })
        
        return recommendations

    def _generate_action_items(
        self, 
        skills_analysis: Dict[str, Any], 
        experience_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate specific action items for candidate improvement
        """
        action_items = []
        
        # Skills-based actions
        if skills_analysis.get("skill_gaps"):
            action_items.append({
                "category": "skill_development",
                "priority": "high",
                "title": "Address Critical Skill Gaps",
                "description": f"Focus on developing: {', '.join(skills_analysis['skill_gaps'][:3])}",
                "estimated_time": "2-4 weeks",
                "resources": skills_analysis.get("learning_path", [])
            })
        
        return action_items

    def get_specialized_prompt_template(self) -> PromptTemplate:
        """
        Get job matcher specific prompt template
        """
        return PromptTemplate(
            system_prompt=self._build_system_prompt(),
            user_prompt="Analyze job-candidate compatibility comprehensively",
            reasoning_mode=ReasoningMode.MULTI_PERSPECTIVE,
            complexity=PromptComplexity.EXPERT,
            context_variables={
                "matching_algorithm": "advanced_ml",
                "analysis_depth": "comprehensive",
                "industry_focus": "technology"
            },
            validation_rules=[
                "must_include_match_scores",
                "must_provide_recommendations",
                "must_include_confidence_levels"
            ],
            examples=self._get_matching_examples(),
            constraints=self._get_matching_constraints()
        )

    # Helper methods (simplified implementations)
    def _load_skill_taxonomy(self) -> Dict[str, Any]:
        """Load comprehensive skill taxonomy"""
        return {"technology": {"programming": ["Python", "Java"], "frameworks": ["React", "Django"]}}

    def _load_industry_data(self) -> Dict[str, Any]:
        """Load industry-specific data"""
        return {"technology": {"growth_rate": 15, "avg_salary": 95000}}

    def _load_salary_data(self) -> Dict[str, Any]:
        """Load salary benchmarking data"""
        return {"software_engineer": {"entry": 70000, "mid": 95000, "senior": 130000}}

    def _load_company_culture_data(self) -> Dict[str, Any]:
        """Load company culture assessment data"""
        return {"startup": {"pace": "fast", "structure": "flexible"}}

    def _load_career_paths(self) -> Dict[str, Any]:
        """Load career progression paths"""
        return {"software_engineer": ["senior_engineer", "tech_lead", "engineering_manager"]}

    def _extract_candidate_profile(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract candidate profile from input"""
        return input_data.get("candidate_profile", input_data)

    def _extract_job_requirements(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract job requirements from input"""
        return input_data.get("job_requirements", context.get("job_requirements", {}))

    def _normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize skill names for comparison"""
        return [skill.lower().strip() for skill in skills if skill]

    def _calculate_skill_matches(self, candidate_skills: List[str], required_skills: List[str]) -> List[str]:
        """Calculate skill matches between candidate and requirements"""
        return [skill for skill in candidate_skills if skill in required_skills]

    def _identify_skill_gaps(self, candidate_skills: List[str], required_skills: List[str]) -> List[str]:
        """Identify missing skills"""
        return [skill for skill in required_skills if skill not in candidate_skills]

    def _identify_transferable_skills(self, candidate_skills: List[str], required_skills: List[str]) -> List[str]:
        """Identify transferable skills"""
        # Simplified implementation
        return []

    def _generate_learning_path(self, skill_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate learning path for skill gaps"""
        return [{"skill": skill, "resources": ["online_course", "practice_projects"]} for skill in skill_gaps[:3]]

    def _calculate_total_experience_years(self, experience: List[Dict[str, Any]]) -> float:
        """Calculate total years of experience"""
        # Simplified implementation
        return len(experience) * 2.5  # Assume average 2.5 years per role

    def _calculate_relevant_experience_years(self, experience: List[Dict[str, Any]], industry: str, role_type: str) -> float:
        """Calculate relevant experience years"""
        # Simplified implementation
        return self._calculate_total_experience_years(experience) * 0.8

    def _assess_experience_level_match(self, experience: List[Dict[str, Any]], required_level: str) -> Dict[str, Any]:
        """Assess experience level match"""
        return {"score": 85, "level": "mid", "match": True}

    def _analyze_career_progression(self, experience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze career progression pattern"""
        return {"score": 80, "trend": "upward", "consistency": "good"}

    def _get_match_grade(self, score: float) -> str:
        """Convert match score to letter grade"""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "B+"
        elif score >= 75: return "B"
        elif score >= 70: return "C+"
        elif score >= 65: return "C"
        else: return "D"

    def _get_matching_examples(self) -> List[Dict[str, str]]:
        """Get matching examples"""
        return []

    def _get_matching_constraints(self) -> List[str]:
        """Get matching constraints"""
        return ["Provide objective analysis", "Include confidence scores", "Consider cultural fit"]

    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response"""
        try:
            cleaned = re.sub(r'```json\s*', '', response)
            cleaned = re.sub(r'```\s*$', '', cleaned)
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return {}
        except:
            return {}

    def _get_fallback_matching_result(self) -> Dict[str, Any]:
        """Get fallback matching result"""
        return {
            "overall_match": {"score": 75, "grade": "B", "confidence": 50},
            "error": "Advanced matching unavailable, using fallback analysis"
        }