"""
RecruiterViewAgent - For HRs to evaluate resumes with advanced scoring and ranking
Provides comprehensive candidate evaluation, comparison tools, and hiring insights
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.multi_ai_base import MultiAIAgent
from utils.sqlite_logger import log_interaction
import json
import logging
from typing import Dict, List,  Any, Tuple
from datetime import datetime
import statistics


class RecruiterViewAgent(MultiAIAgent):
    """Agent for HR professionals to evaluate and rank candidates"""
    
    def __init__(self):
        super().__init__("RecruiterViewAgent")
        self.evaluation_criteria = self._load_evaluation_criteria()
        self.scoring_weights = self._load_scoring_weights()
        self.red_flags = self._load_red_flags()
        self.industry_benchmarks = self._load_industry_benchmarks()
        
    def _load_evaluation_criteria(self) -> Dict[str, Dict]:
        """Load comprehensive evaluation criteria for different aspects"""
        return {
            "technical_skills": {
                "weight": 0.30,
                "subcriteria": [
                    "relevant_technologies",
                    "skill_depth",
                    "learning_progression",
                    "certification_value",
                    "practical_application"
                ]
            },
            "experience": {
                "weight": 0.25,
                "subcriteria": [
                    "years_of_experience",
                    "role_progression",
                    "company_quality",
                    "project_complexity",
                    "leadership_experience"
                ]
            },
            "education": {
                "weight": 0.15,
                "subcriteria": [
                    "degree_relevance",
                    "institution_ranking",
                    "academic_performance",
                    "continuous_learning",
                    "specialized_training"
                ]
            },
            "achievements": {
                "weight": 0.20,
                "subcriteria": [
                    "quantified_results",
                    "innovation_impact",
                    "recognition_awards",
                    "problem_solving",
                    "business_impact"
                ]
            },
            "soft_skills": {
                "weight": 0.10,
                "subcriteria": [
                    "communication_quality",
                    "teamwork_indicators",
                    "adaptability_signs",
                    "initiative_examples",
                    "cultural_fit_potential"
                ]
            }
        }
    
    def _load_scoring_weights(self) -> Dict[str, float]:
        """Load position-specific scoring weights"""
        return {
            "entry_level": {"experience": 0.15, "education": 0.25, "potential": 0.30},
            "mid_level": {"experience": 0.35, "skills": 0.30, "achievements": 0.25},
            "senior_level": {"leadership": 0.30, "achievements": 0.30, "experience": 0.25},
            "executive": {"leadership": 0.40, "strategy": 0.25, "results": 0.35}
        }
    
    def _load_red_flags(self) -> List[Dict[str, Any]]:
        """Load potential red flags to watch for in resumes"""
        return [
            {
                "type": "employment_gaps",
                "description": "Unexplained gaps > 6 months",
                "severity": "medium",
                "auto_detect": True
            },
            {
                "type": "job_hopping",
                "description": "Multiple jobs < 1 year duration",
                "severity": "medium",
                "auto_detect": True
            },
            {
                "type": "skill_inflation",
                "description": "Claims expertise without sufficient experience",
                "severity": "high",
                "auto_detect": False
            },
            {
                "type": "inconsistent_dates",
                "description": "Timeline inconsistencies",
                "severity": "high",
                "auto_detect": True
            },
            {
                "type": "overqualification",
                "description": "Significantly overqualified for position",
                "severity": "low",
                "auto_detect": False
            },
            {
                "type": "underqualification",
                "description": "Missing critical requirements",
                "severity": "high",
                "auto_detect": False
            }
        ]
    
    def _load_industry_benchmarks(self) -> Dict[str, Dict]:
        """Load industry benchmarks for comparison"""
        return {
            "technology": {
                "avg_experience_years": 5.2,
                "key_skills_expected": 8,
                "education_importance": 0.7,
                "salary_ranges": {
                    "entry": (50000, 80000),
                    "mid": (80000, 130000),
                    "senior": (130000, 200000)
                }
            },
            "finance": {
                "avg_experience_years": 6.8,
                "key_skills_expected": 6,
                "education_importance": 0.9,
                "salary_ranges": {
                    "entry": (55000, 85000),
                    "mid": (85000, 140000),
                    "senior": (140000, 250000)
                }
            },
            "healthcare": {
                "avg_experience_years": 7.5,
                "key_skills_expected": 10,
                "education_importance": 0.95,
                "salary_ranges": {
                    "entry": (45000, 75000),
                    "mid": (75000, 120000),
                    "senior": (120000, 180000)
                }
            },
            "marketing": {
                "avg_experience_years": 4.8,
                "key_skills_expected": 7,
                "education_importance": 0.6,
                "salary_ranges": {
                    "entry": (40000, 65000),
                    "mid": (65000, 100000),
                    "senior": (100000, 160000)
                }
            }
        }
    
    def evaluate_candidate(self, resume_data: Dict, job_requirements: Dict, 
                          position_level: str = "mid_level") -> Dict[str, Any]:
        """Comprehensive candidate evaluation with detailed scoring"""
        
        evaluation = {
            "candidate_id": resume_data.get("candidate_id", f"candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            "evaluation_timestamp": datetime.now().isoformat(),
            "position_level": position_level,
            "overall_score": 0,
            "category_scores": {},
            "strengths": [],
            "weaknesses": [],
            "red_flags": [],
            "recommendations": [],
            "interview_focus_areas": [],
            "salary_recommendation": {},
            "hiring_recommendation": "",
            "confidence_level": 0
        }
        
        # Evaluate each category
        for category, criteria in self.evaluation_criteria.items():
            score = self._evaluate_category(category, resume_data, job_requirements)
            evaluation["category_scores"][category] = score
            evaluation["overall_score"] += score * criteria["weight"]
        
        # Detect red flags
        evaluation["red_flags"] = self._detect_red_flags(resume_data)
        
        # Generate insights
        evaluation["strengths"] = self._identify_strengths(resume_data, evaluation["category_scores"])
        evaluation["weaknesses"] = self._identify_weaknesses(resume_data, evaluation["category_scores"])
        evaluation["recommendations"] = self._generate_recommendations(evaluation, job_requirements)
        evaluation["interview_focus_areas"] = self._suggest_interview_focus(evaluation, resume_data)
        
        # Salary recommendation
        evaluation["salary_recommendation"] = self._recommend_salary(resume_data, evaluation["overall_score"])
        
        # Final hiring recommendation
        evaluation["hiring_recommendation"] = self._generate_hiring_recommendation(evaluation)
        evaluation["confidence_level"] = self._calculate_confidence_level(evaluation)
        
        return evaluation
    
    def _evaluate_category(self, category: str, resume_data: Dict, job_requirements: Dict) -> float:
        """Evaluate a specific category with AI assistance"""
        
        prompt = f"""
        Evaluate the candidate's {category} based on their resume and job requirements:
        
        Resume Data: {json.dumps(resume_data.get(category, {}), indent=2)}
        Job Requirements: {json.dumps(job_requirements.get(category, {}), indent=2)}
        
        Evaluation Criteria for {category}:
        {json.dumps(self.evaluation_criteria[category], indent=2)}
        
        Please provide:
        1. Detailed analysis of how the candidate meets each subcriteria
        2. Specific examples from their background
        3. Areas where they excel
        4. Areas needing improvement
        5. Overall score (0-100) with justification
        
        Be objective and thorough in your evaluation.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            # Extract score from response
            score = self._extract_score_from_response(response)
            log_interaction("RecruiterViewAgent", f"evaluate_{category}", 
                          resume_data.get("name", "Unknown"), response)
            return score
        except Exception as e:
            logging.error(f"Error evaluating {category}: {e}")
            return self._get_fallback_category_score(category, resume_data)
    
    def _extract_score_from_response(self, response: str) -> float:
        """Extract numerical score from AI response"""
        import re
        
        # Look for score patterns
        score_patterns = [
            r'score[:\s]*(\d+(?:\.\d+)?)',
            r'rating[:\s]*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)[/\s]*(?:out of )?100',
            r'(\d+(?:\.\d+)?)%'
        ]
        
        for pattern in score_patterns:
            match = re.search(pattern, response.lower())
            if match:
                score = float(match.group(1))
                # Normalize to 0-100 scale
                if score <= 1:
                    score *= 100
                return min(100, max(0, score))
        
        # Fallback: analyze response sentiment
        positive_words = ['excellent', 'outstanding', 'strong', 'impressive', 'skilled']
        negative_words = ['weak', 'lacking', 'insufficient', 'poor', 'limited']
        
        positive_count = sum(1 for word in positive_words if word in response.lower())
        negative_count = sum(1 for word in negative_words if word in response.lower())
        
        base_score = 60  # Neutral score
        sentiment_adjustment = (positive_count - negative_count) * 10
        
        return min(100, max(0, base_score + sentiment_adjustment))
    
    def _get_fallback_category_score(self, category: str, resume_data: Dict) -> float:
        """Provide fallback scoring when AI is unavailable"""
        fallback_scores = {
            "technical_skills": len(resume_data.get("skills", [])) * 8,
            "experience": min(resume_data.get("total_experience_years", 0) * 15, 100),
            "education": 70 if resume_data.get("education", {}).get("degree") else 40,
            "achievements": len(resume_data.get("achievements", [])) * 20,
            "soft_skills": 65  # Average baseline
        }
        
        return min(100, fallback_scores.get(category, 60))
    
    def _detect_red_flags(self, resume_data: Dict) -> List[Dict[str, Any]]:
        """Detect potential red flags in the resume"""
        detected_flags = []
        
        for flag in self.red_flags:
            if flag["auto_detect"]:
                is_flagged = False
                details = ""
                
                if flag["type"] == "employment_gaps":
                    is_flagged, details = self._check_employment_gaps(resume_data)
                elif flag["type"] == "job_hopping":
                    is_flagged, details = self._check_job_hopping(resume_data)
                elif flag["type"] == "inconsistent_dates":
                    is_flagged, details = self._check_date_consistency(resume_data)
                
                if is_flagged:
                    detected_flags.append({
                        "type": flag["type"],
                        "description": flag["description"],
                        "severity": flag["severity"],
                        "details": details,
                        "recommendation": self._get_flag_recommendation(flag["type"])
                    })
        
        return detected_flags
    
    def _check_employment_gaps(self, resume_data: Dict) -> Tuple[bool, str]:
        """Check for employment gaps"""
        experiences = resume_data.get("experience", [])
        if len(experiences) < 2:
            return False, ""
        
        # Sort experiences by end date
        sorted_exp = sorted(experiences, key=lambda x: x.get("end_date", "9999"))
        
        gaps = []
        for i in range(len(sorted_exp) - 1):
            current_end = sorted_exp[i].get("end_date", "")
            next_start = sorted_exp[i + 1].get("start_date", "")
            
            if current_end and next_start:
                try:
                    end_date = datetime.strptime(current_end, "%Y-%m")
                    start_date = datetime.strptime(next_start, "%Y-%m")
                    gap_months = (start_date - end_date).days / 30
                    
                    if gap_months > 6:
                        gaps.append(f"{gap_months:.0f} months between {current_end} and {next_start}")
                except ValueError:
                    continue
        
        if gaps:
            return True, f"Employment gaps detected: {'; '.join(gaps)}"
        return False, ""
    
    def _check_job_hopping(self, resume_data: Dict) -> Tuple[bool, str]:
        """Check for job hopping pattern"""
        experiences = resume_data.get("experience", [])
        short_tenures = []
        
        for exp in experiences:
            start_date = exp.get("start_date", "")
            end_date = exp.get("end_date", "")
            
            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, "%Y-%m")
                    end = datetime.strptime(end_date, "%Y-%m")
                    tenure_months = (end - start).days / 30
                    
                    if tenure_months < 12:
                        short_tenures.append(f"{exp.get('company', 'Unknown')} ({tenure_months:.0f} months)")
                except ValueError:
                    continue
        
        if len(short_tenures) >= 2:
            return True, f"Multiple short tenures: {'; '.join(short_tenures)}"
        return False, ""
    
    def _check_date_consistency(self, resume_data: Dict) -> Tuple[bool, str]:
        """Check for date inconsistencies"""
        # This would involve more complex date validation logic
        # For now, return a simple check
        return False, ""
    
    def _get_flag_recommendation(self, flag_type: str) -> str:
        """Get recommendation for handling specific red flags"""
        recommendations = {
            "employment_gaps": "Ask about employment gaps during interview. May have valid reasons (education, family, health).",
            "job_hopping": "Inquire about reasons for frequent job changes. Assess commitment and stability.",
            "inconsistent_dates": "Verify employment history and dates during reference checks.",
            "skill_inflation": "Test technical skills through practical assessments or coding challenges.",
            "overqualification": "Discuss long-term career goals and commitment to the role.",
            "underqualification": "Assess potential for growth and willingness to learn."
        }
        return recommendations.get(flag_type, "Follow up during interview process.")
    
    def _identify_strengths(self, resume_data: Dict, category_scores: Dict) -> List[str]:
        """Identify candidate's key strengths"""
        strengths = []
        
        # Score-based strengths
        for category, score in category_scores.items():
            if score >= 80:
                strengths.append(f"Excellent {category.replace('_', ' ')}")
            elif score >= 70:
                strengths.append(f"Strong {category.replace('_', ' ')}")
        
        # Specific resume-based strengths
        if resume_data.get("total_experience_years", 0) > 10:
            strengths.append("Extensive industry experience")
        
        if len(resume_data.get("skills", [])) > 15:
            strengths.append("Diverse technical skill set")
        
        if resume_data.get("certifications", []):
            strengths.append("Professional certifications demonstrate commitment")
        
        if resume_data.get("leadership_experience"):
            strengths.append("Leadership and management experience")
        
        return strengths[:5]  # Limit to top 5 strengths
    
    def _identify_weaknesses(self, resume_data: Dict, category_scores: Dict) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        # Score-based weaknesses
        for category, score in category_scores.items():
            if score < 50:
                weaknesses.append(f"Needs improvement in {category.replace('_', ' ')}")
            elif score < 60:
                weaknesses.append(f"Could strengthen {category.replace('_', ' ')}")
        
        # Specific gaps
        if resume_data.get("total_experience_years", 0) < 2:
            weaknesses.append("Limited professional experience")
        
        if not resume_data.get("education", {}).get("degree"):
            weaknesses.append("No formal degree mentioned")
        
        if len(resume_data.get("achievements", [])) < 2:
            weaknesses.append("Limited quantified achievements")
        
        return weaknesses[:3]  # Limit to top 3 areas for improvement
    
    def _generate_recommendations(self, evaluation: Dict, job_requirements: Dict) -> List[str]:
        """Generate actionable recommendations for the hiring process"""
        recommendations = []
        overall_score = evaluation["overall_score"]
        
        if overall_score >= 85:
            recommendations.append("Strong candidate - fast-track for final rounds")
            recommendations.append("Consider for team lead or senior roles")
        elif overall_score >= 70:
            recommendations.append("Good candidate - proceed with standard interview process")
            recommendations.append("Focus interview on technical deep-dive")
        elif overall_score >= 55:
            recommendations.append("Marginal candidate - thorough evaluation needed")
            recommendations.append("Consider for entry-level or junior positions")
        else:
            recommendations.append("Below threshold - consider rejection or alternative roles")
        
        # Red flag specific recommendations
        if evaluation["red_flags"]:
            recommendations.append("Address red flags during interview process")
        
        # Category-specific recommendations
        weak_categories = [cat for cat, score in evaluation["category_scores"].items() if score < 60]
        if weak_categories:
            recommendations.append(f"Assess {', '.join(weak_categories)} thoroughly during interview")
        
        return recommendations
    
    def _suggest_interview_focus(self, evaluation: Dict, resume_data: Dict) -> List[str]:
        """Suggest areas to focus on during interviews"""
        focus_areas = []
        
        # Focus on weak areas
        weak_categories = [cat for cat, score in evaluation["category_scores"].items() if score < 65]
        for category in weak_categories:
            focus_areas.append(f"Deep dive into {category.replace('_', ' ')} capabilities")
        
        # Red flag areas
        for flag in evaluation["red_flags"]:
            if flag["severity"] in ["high", "medium"]:
                focus_areas.append(f"Address {flag['type'].replace('_', ' ')}")
        
        # General focus areas
        focus_areas.extend([
            "Cultural fit assessment",
            "Problem-solving approach",
            "Long-term career goals",
            "Salary expectations alignment"
        ])
        
        return focus_areas[:6]  # Limit to 6 focus areas
    
    def _recommend_salary(self, resume_data: Dict, overall_score: float) -> Dict[str, Any]:
        """Recommend salary range based on evaluation"""
        base_salary = 75000  # Default base
        experience_years = resume_data.get("total_experience_years", 0)
        
        # Experience multiplier
        base_salary += experience_years * 5000
        
        # Score multiplier
        score_multiplier = overall_score / 100
        base_salary = int(base_salary * score_multiplier)
        
        # Create range
        salary_range = {
            "min": int(base_salary * 0.9),
            "max": int(base_salary * 1.15),
            "recommended": base_salary,
            "justification": f"Based on {experience_years} years experience and {overall_score:.0f}% evaluation score"
        }
        
        return salary_range
    
    def _generate_hiring_recommendation(self, evaluation: Dict) -> str:
        """Generate final hiring recommendation"""
        overall_score = evaluation["overall_score"]
        red_flag_count = len([f for f in evaluation["red_flags"] if f["severity"] == "high"])
        
        if red_flag_count > 1:
            return "Not Recommended - Multiple high-severity red flags"
        elif overall_score >= 80:
            return "Highly Recommended - Excellent candidate"
        elif overall_score >= 70:
            return "Recommended - Good fit for the role"
        elif overall_score >= 60:
            return "Conditionally Recommended - Proceed with caution"
        elif overall_score >= 50:
            return "Not Recommended - Below minimum threshold"
        else:
            return "Strongly Not Recommended - Significant gaps identified"
    
    def _calculate_confidence_level(self, evaluation: Dict) -> float:
        """Calculate confidence level in the evaluation"""
        base_confidence = 0.8
        
        # Reduce confidence for red flags
        red_flag_penalty = len(evaluation["red_flags"]) * 0.05
        
        # Reduce confidence for extreme scores (might indicate insufficient data)
        score_variance = statistics.variance(evaluation["category_scores"].values()) if len(evaluation["category_scores"]) > 1 else 0
        if score_variance > 400:  # High variance indicates inconsistent evaluation
            base_confidence -= 0.1
        
        confidence = max(0.3, base_confidence - red_flag_penalty)
        return round(confidence, 2)
    
    def compare_candidates(self, candidates: List[Dict]) -> Dict[str, Any]:
        """Compare multiple candidates and provide ranking"""
        
        if not candidates:
            return {"error": "No candidates provided for comparison"}
        
        comparison = {
            "total_candidates": len(candidates),
            "comparison_timestamp": datetime.now().isoformat(),
            "ranking": [],
            "category_leaders": {},
            "summary_stats": {},
            "recommendations": []
        }
        
        # Sort candidates by overall score
        sorted_candidates = sorted(candidates, key=lambda x: x.get("overall_score", 0), reverse=True)
        
        # Create ranking
        for rank, candidate in enumerate(sorted_candidates, 1):
            comparison["ranking"].append({
                "rank": rank,
                "candidate_id": candidate.get("candidate_id", f"candidate_{rank}"),
                "overall_score": candidate.get("overall_score", 0),
                "strengths": candidate.get("strengths", [])[:3],
                "red_flags_count": len(candidate.get("red_flags", [])),
                "hiring_recommendation": candidate.get("hiring_recommendation", "Unknown")
            })
        
        # Find category leaders
        for category in self.evaluation_criteria.keys():
            best_candidate = max(candidates, key=lambda x: x.get("category_scores", {}).get(category, 0))
            comparison["category_leaders"][category] = {
                "candidate_id": best_candidate.get("candidate_id", "Unknown"),
                "score": best_candidate.get("category_scores", {}).get(category, 0)
            }
        
        # Calculate summary statistics
        scores = [c.get("overall_score", 0) for c in candidates]
        comparison["summary_stats"] = {
            "average_score": round(statistics.mean(scores), 1),
            "median_score": round(statistics.median(scores), 1),
            "score_range": {"min": min(scores), "max": max(scores)},
            "candidates_above_70": sum(1 for s in scores if s >= 70),
            "recommended_candidates": sum(1 for c in candidates if "Recommended" in c.get("hiring_recommendation", ""))
        }
        
        # Generate comparison insights
        comparison["recommendations"] = self._generate_comparison_recommendations(comparison, candidates)
        
        return comparison
    
    def _generate_comparison_recommendations(self, comparison: Dict, candidates: List[Dict]) -> List[str]:
        """Generate recommendations based on candidate comparison"""
        recommendations = []
        
        top_candidates = comparison["ranking"][:3]
        recommended_count = comparison["summary_stats"]["recommended_candidates"]
        
        if recommended_count == 0:
            recommendations.append("Consider expanding candidate pool or adjusting requirements")
        elif recommended_count == 1:
            recommendations.append("Single strong candidate identified - fast-track hiring process")
        elif recommended_count > 3:
            recommendations.append("Multiple strong candidates - consider team expansion or future roles")
        
        # Score distribution insights
        avg_score = comparison["summary_stats"]["average_score"]
        if avg_score < 60:
            recommendations.append("Overall candidate quality below expectations - review sourcing strategy")
        elif avg_score > 80:
            recommendations.append("Exceptional candidate pool - opportunity for selective hiring")
        
        # Specific candidate recommendations
        if top_candidates:
            top_candidate = top_candidates[0]
            recommendations.append(f"Top candidate ({top_candidate['candidate_id']}) shows {top_candidate['overall_score']:.0f}% match")
        
        return recommendations
    
    def generate_interview_guide(self, evaluation: Dict, job_requirements: Dict) -> Dict[str, Any]:
        """Generate comprehensive interview guide for the candidate"""
        
        guide = {
            "candidate_id": evaluation.get("candidate_id", "Unknown"),
            "interview_type": "structured",
            "estimated_duration": "60-90 minutes",
            "sections": []
        }
        
        # Introduction section
        guide["sections"].append({
            "section": "Introduction",
            "duration": "10 minutes",
            "objectives": ["Build rapport", "Explain interview process", "Set expectations"],
            "questions": [
                "Tell me about yourself and your career journey",
                "What interests you most about this role?",
                "What do you know about our company?"
            ]
        })
        
        # Technical assessment section
        weak_technical = evaluation["category_scores"].get("technical_skills", 100) < 70
        guide["sections"].append({
            "section": "Technical Assessment",
            "duration": "25-30 minutes" if weak_technical else "15-20 minutes",
            "objectives": ["Validate technical skills", "Assess problem-solving approach"],
            "questions": self._generate_technical_questions(evaluation, job_requirements),
            "focus_areas": evaluation.get("interview_focus_areas", [])
        })
        
        # Experience deep-dive
        guide["sections"].append({
            "section": "Experience Discussion",
            "duration": "20-25 minutes",
            "objectives": ["Understand past achievements", "Assess role fit"],
            "questions": [
                "Walk me through your most significant achievement",
                "Describe a challenging project and how you handled it",
                "Tell me about a time you had to learn something new quickly"
            ]
        })
        
        # Red flag address section
        if evaluation.get("red_flags"):
            guide["sections"].append({
                "section": "Clarifications",
                "duration": "10-15 minutes",
                "objectives": ["Address potential concerns", "Gather additional context"],
                "questions": [flag["recommendation"] for flag in evaluation["red_flags"][:3]]
            })
        
        # Closing section
        guide["sections"].append({
            "section": "Closing",
            "duration": "10 minutes",
            "objectives": ["Answer candidate questions", "Discuss next steps"],
            "questions": [
                "What questions do you have about the role or company?",
                "What are your salary expectations?",
                "What's your availability for starting?"
            ]
        })
        
        # Interview tips
        guide["interviewer_tips"] = [
            "Focus on behavioral questions for soft skills assessment",
            "Ask for specific examples and quantified results",
            "Take notes on red flag areas for reference checks",
            "Assess cultural fit throughout the conversation",
            "Be prepared to sell the role and company"
        ]
        
        return guide
    
    def _generate_technical_questions(self, evaluation: Dict, job_requirements: Dict) -> List[str]:
        """Generate role-specific technical questions"""
        questions = [
            "How would you approach solving [specific technical challenge from job requirements]?",
            "Explain your experience with [key technology from job requirements]",
            "Walk me through how you would [relevant technical task]"
        ]
        
        # Add questions based on weak areas
        weak_areas = [cat for cat, score in evaluation["category_scores"].items() if score < 65]
        if "technical_skills" in weak_areas:
            questions.extend([
                "How do you stay updated with new technologies?",
                "Describe a time when you had to quickly learn a new technology"
            ])
        
        return questions
    
    def get_fallback_response(self, response_type: str) -> Any:
        """Provide fallback responses when AI is unavailable"""
        fallback_responses = {
            "evaluation": {
                "overall_score": 65,
                "category_scores": {
                    "technical_skills": 65,
                    "experience": 60,
                    "education": 70,
                    "achievements": 55,
                    "soft_skills": 65
                },
                "hiring_recommendation": "Requires thorough evaluation",
                "confidence_level": 0.6
            },
            "comparison": "Detailed comparison requires AI analysis",
            "interview_guide": {
                "sections": [
                    {"section": "Technical Assessment", "duration": "30 minutes"},
                    {"section": "Experience Review", "duration": "20 minutes"},
                    {"section": "Cultural Fit", "duration": "10 minutes"}
                ]
            }
        }
        
        return fallback_responses.get(response_type, "Fallback response not available")
    
    def run(self, candidates_data: List[Dict], job_requirements: Dict, 
            analysis_type: str = "evaluate") -> Dict[str, Any]:
        """Main execution method for recruiter view functionality"""
        
        try:
            if analysis_type == "evaluate" and len(candidates_data) == 1:
                # Single candidate evaluation
                evaluation = self.evaluate_candidate(
                    candidates_data[0], 
                    job_requirements, 
                    job_requirements.get("position_level", "mid_level")
                )
                
                interview_guide = self.generate_interview_guide(evaluation, job_requirements)
                
                result = {
                    "analysis_type": "single_evaluation",
                    "evaluation": evaluation,
                    "interview_guide": interview_guide,
                    "next_steps": [
                        "Review evaluation details",
                        "Schedule interview if recommended",
                        "Prepare interview questions based on guide",
                        "Plan reference checks for red flag areas"
                    ]
                }
                
            elif analysis_type == "compare" and len(candidates_data) > 1:
                # Multiple candidate comparison
                evaluations = []
                for candidate in candidates_data:
                    eval_result = self.evaluate_candidate(candidate, job_requirements)
                    evaluations.append(eval_result)
                
                comparison = self.compare_candidates(evaluations)
                
                result = {
                    "analysis_type": "candidate_comparison",
                    "individual_evaluations": evaluations,
                    "comparison": comparison,
                    "next_steps": [
                        "Review top-ranked candidates",
                        "Schedule interviews based on ranking",
                        "Consider batch interview process for efficiency"
                    ]
                }
            
            else:
                result = {
                    "error": "Invalid analysis type or insufficient candidate data",
                    "supported_types": ["evaluate", "compare"],
                    "data_requirements": {
                        "evaluate": "Single candidate data required",
                        "compare": "Multiple candidate data required"
                    }
                }
            
            log_interaction("RecruiterViewAgent", "run", 
                          f"{analysis_type}_{len(candidates_data)}_candidates", 
                          json.dumps(result, indent=2, default=str))
            
            return result
            
        except Exception as e:
            logging.error(f"Error in RecruiterViewAgent.run: {e}")
            return {
                "error": str(e),
                "fallback_advice": [
                    "Review candidates manually using standard criteria",
                    "Focus on job requirement alignment",
                    "Conduct structured interviews",
                    "Check references thoroughly"
                ]
            }
