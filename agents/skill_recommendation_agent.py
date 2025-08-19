"""
SkillRecommendationAgent - Real-time skill recommendations with courses and learning paths
Provides personalized skill gap analysis, learning recommendations, and career advancement guidance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.multi_ai_base import MultiAIAgent
from utils.sqlite_logger import log_interaction
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import re


class SkillRecommendationAgent(MultiAIAgent):
    """Agent for skill gap analysis and learning recommendations"""
    
    def __init__(self):
        super().__init__("SkillRecommendationAgent")
        self.skill_categories = self._load_skill_categories()
        self.learning_platforms = self._load_learning_platforms()
        self.industry_trends = self._load_industry_trends()
        self.skill_priorities = self._load_skill_priorities()
        self.certification_map = self._load_certification_map()
        
    def _load_skill_categories(self) -> Dict[str, List[str]]:
        """Load comprehensive skill categories"""
        return {
            "technical_skills": {
                "programming_languages": [
                    "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript",
                    "Swift", "Kotlin", "PHP", "Ruby", "R", "MATLAB", "Scala", "SQL"
                ],
                "web_development": [
                    "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask",
                    "Spring Boot", "ASP.NET", "HTML5", "CSS3", "SASS", "Bootstrap", "Tailwind"
                ],
                "mobile_development": [
                    "React Native", "Flutter", "iOS Development", "Android Development",
                    "Xamarin", "Ionic", "PhoneGap", "Unity 3D"
                ],
                "cloud_platforms": [
                    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform",
                    "CloudFormation", "Serverless", "Lambda", "Azure Functions"
                ],
                "data_science": [
                    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas",
                    "NumPy", "Scikit-learn", "Jupyter", "Tableau", "Power BI", "Apache Spark"
                ],
                "devops": [
                    "Jenkins", "GitLab CI", "GitHub Actions", "Ansible", "Chef", "Puppet",
                    "Monitoring", "Logging", "CI/CD", "Infrastructure as Code"
                ],
                "databases": [
                    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "Cassandra",
                    "DynamoDB", "Oracle", "SQL Server", "Neo4j"
                ],
                "cybersecurity": [
                    "Penetration Testing", "SIEM", "Vulnerability Assessment", "Compliance",
                    "Incident Response", "Risk Management", "Cryptography", "Network Security"
                ]
            },
            "soft_skills": [
                "Leadership", "Communication", "Project Management", "Problem Solving",
                "Critical Thinking", "Teamwork", "Adaptability", "Time Management",
                "Negotiation", "Public Speaking", "Emotional Intelligence", "Creativity"
            ],
            "business_skills": [
                "Strategic Planning", "Financial Analysis", "Marketing", "Sales",
                "Business Development", "Operations Management", "Supply Chain",
                "Customer Service", "Quality Assurance", "Process Improvement"
            ],
            "design_skills": [
                "UI/UX Design", "Graphic Design", "Adobe Creative Suite", "Figma",
                "Sketch", "InVision", "Wireframing", "Prototyping", "User Research",
                "Design Systems", "Accessibility Design"
            ]
        }
    
    def _load_learning_platforms(self) -> Dict[str, Dict]:
        """Load learning platforms with their specialties and ratings"""
        return {
            "coursera": {
                "name": "Coursera",
                "url": "https://www.coursera.org",
                "specialties": ["University Courses", "Professional Certificates", "Degrees"],
                "rating": 4.5,
                "price_range": "Free - $79/month",
                "best_for": ["Academic rigor", "University partnerships", "Certificates"]
            },
            "udemy": {
                "name": "Udemy",
                "url": "https://www.udemy.com",
                "specialties": ["Technical Skills", "Creative Skills", "Business"],
                "rating": 4.3,
                "price_range": "$10 - $200 per course",
                "best_for": ["Practical skills", "Affordable courses", "Lifetime access"]
            },
            "pluralsight": {
                "name": "Pluralsight",
                "url": "https://www.pluralsight.com",
                "specialties": ["Technology", "Software Development", "IT Operations"],
                "rating": 4.4,
                "price_range": "$29 - $45/month",
                "best_for": ["Tech professionals", "Skill assessments", "Learning paths"]
            },
            "linkedin_learning": {
                "name": "LinkedIn Learning",
                "url": "https://www.linkedin.com/learning",
                "specialties": ["Business Skills", "Technology", "Creative Skills"],
                "rating": 4.2,
                "price_range": "$29.99/month",
                "best_for": ["Professional networking", "Business skills", "Short courses"]
            },
            "edx": {
                "name": "edX",
                "url": "https://www.edx.org",
                "specialties": ["University Courses", "Computer Science", "Data Science"],
                "rating": 4.3,
                "price_range": "Free - $300 per course",
                "best_for": ["University-level content", "Free auditing", "MicroMasters"]
            },
            "codecademy": {
                "name": "Codecademy",
                "url": "https://www.codecademy.com",
                "specialties": ["Programming", "Web Development", "Data Science"],
                "rating": 4.1,
                "price_range": "Free - $39.99/month",
                "best_for": ["Interactive coding", "Beginner-friendly", "Hands-on practice"]
            },
            "udacity": {
                "name": "Udacity",
                "url": "https://www.udacity.com",
                "specialties": ["Tech Skills", "AI/ML", "Programming", "Data Science"],
                "rating": 4.0,
                "price_range": "$399/month for Nanodegrees",
                "best_for": ["Industry projects", "Mentorship", "Career services"]
            },
            "aws_training": {
                "name": "AWS Training",
                "url": "https://aws.amazon.com/training",
                "specialties": ["Cloud Computing", "AWS Services", "DevOps"],
                "rating": 4.4,
                "price_range": "Free - $3000 for bootcamps",
                "best_for": ["AWS certification", "Cloud skills", "Hands-on labs"]
            }
        }
    
    def _load_industry_trends(self) -> Dict[str, Dict]:
        """Load current industry trends and emerging skills"""
        return {
            "2024_trending": {
                "hot_skills": [
                    "Artificial Intelligence", "Machine Learning", "Cloud Computing",
                    "Cybersecurity", "Data Analytics", "DevOps", "Blockchain",
                    "Internet of Things", "Robotic Process Automation", "5G Technology"
                ],
                "emerging_skills": [
                    "Prompt Engineering", "MLOps", "Edge Computing", "Quantum Computing",
                    "AR/VR Development", "Sustainable Technology", "Low-Code/No-Code"
                ],
                "declining_skills": [
                    "Flash Development", "Silverlight", "Internet Explorer Support",
                    "Legacy COBOL (in some contexts)", "Outdated PHP versions"
                ]
            },
            "by_industry": {
                "technology": {
                    "high_demand": ["AI/ML", "Cloud Architecture", "Full-Stack Development"],
                    "growth_rate": "15%",
                    "salary_impact": "25-40% increase"
                },
                "finance": {
                    "high_demand": ["FinTech", "Blockchain", "Data Analytics", "Risk Management"],
                    "growth_rate": "12%",
                    "salary_impact": "20-35% increase"
                },
                "healthcare": {
                    "high_demand": ["Health Informatics", "Telemedicine", "Data Privacy"],
                    "growth_rate": "18%",
                    "salary_impact": "15-30% increase"
                },
                "retail": {
                    "high_demand": ["E-commerce", "Digital Marketing", "Supply Chain Analytics"],
                    "growth_rate": "10%",
                    "salary_impact": "10-25% increase"
                }
            }
        }
    
    def _load_skill_priorities(self) -> Dict[str, int]:
        """Load skill priority weights for recommendations"""
        return {
            "market_demand": 30,      # How in-demand the skill is
            "salary_impact": 25,      # Impact on salary potential
            "learning_difficulty": 15, # How difficult to learn (inverse priority)
            "career_growth": 20,      # Impact on career advancement
            "future_relevance": 10    # Long-term relevance
        }
    
    def _load_certification_map(self) -> Dict[str, List[Dict]]:
        """Load certification recommendations for different skills"""
        return {
            "cloud_computing": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "provider": "Amazon Web Services",
                    "difficulty": "Intermediate",
                    "cost": "$150",
                    "validity": "3 years",
                    "market_value": "High"
                },
                {
                    "name": "Microsoft Azure Architect",
                    "provider": "Microsoft",
                    "difficulty": "Advanced",
                    "cost": "$165",
                    "validity": "2 years",
                    "market_value": "High"
                }
            ],
            "data_science": [
                {
                    "name": "Google Data Analytics Professional Certificate",
                    "provider": "Google",
                    "difficulty": "Beginner",
                    "cost": "$49/month",
                    "validity": "Lifetime",
                    "market_value": "Medium"
                },
                {
                    "name": "IBM Data Science Professional Certificate",
                    "provider": "IBM",
                    "difficulty": "Intermediate",
                    "cost": "$39/month",
                    "validity": "Lifetime",
                    "market_value": "Medium-High"
                }
            ],
            "project_management": [
                {
                    "name": "PMP (Project Management Professional)",
                    "provider": "PMI",
                    "difficulty": "Advanced",
                    "cost": "$555",
                    "validity": "3 years",
                    "market_value": "Very High"
                },
                {
                    "name": "Scrum Master Certification",
                    "provider": "Scrum Alliance",
                    "difficulty": "Intermediate",
                    "cost": "$1000-2000",
                    "validity": "2 years",
                    "market_value": "High"
                }
            ]
        }
    
    def analyze_skill_gaps(self, current_resume: Dict, target_job: Dict, 
                          career_goals: Dict = None) -> Dict[str, Any]:
        """Comprehensive skill gap analysis with prioritized recommendations"""
        
        analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "current_skills": self._extract_current_skills(current_resume),
            "required_skills": self._extract_required_skills(target_job),
            "skill_gaps": {},
            "strengths": [],
            "learning_priorities": [],
            "time_investment": {},
            "roi_analysis": {}
        }
        
        # Identify skill gaps
        current_skills = set(analysis["current_skills"])
        required_skills = set(analysis["required_skills"])
        
        analysis["skill_gaps"] = {
            "missing_critical": list(required_skills - current_skills),
            "present_skills": list(current_skills & required_skills),
            "additional_skills": list(current_skills - required_skills),
            "gap_percentage": len(required_skills - current_skills) / len(required_skills) * 100 if required_skills else 0
        }
        
        # Analyze strengths
        analysis["strengths"] = self._analyze_strengths(current_skills, required_skills)
        
        # Prioritize learning recommendations
        analysis["learning_priorities"] = self._prioritize_learning(
            analysis["skill_gaps"]["missing_critical"], 
            target_job, 
            career_goals
        )
        
        # Calculate time investment
        analysis["time_investment"] = self._calculate_time_investment(
            analysis["learning_priorities"]
        )
        
        # ROI Analysis
        analysis["roi_analysis"] = self._calculate_learning_roi(
            analysis["learning_priorities"], 
            target_job
        )
        
        return analysis
    
    def _extract_current_skills(self, resume_data: Dict) -> List[str]:
        """Extract and normalize current skills from resume"""
        skills = []
        
        # Technical skills
        if "technical_skills" in resume_data:
            skills.extend(resume_data["technical_skills"])
        
        # Skills from experience descriptions
        if "experience" in resume_data:
            for exp in resume_data["experience"]:
                description = exp.get("description", "")
                extracted_skills = self._extract_skills_from_text(description)
                skills.extend(extracted_skills)
        
        # Skills from education
        if "education" in resume_data:
            for edu in resume_data["education"]:
                courses = edu.get("relevant_courses", [])
                skills.extend(courses)
        
        # Certifications
        if "certifications" in resume_data:
            for cert in resume_data["certifications"]:
                cert_skills = self._map_certification_to_skills(cert)
                skills.extend(cert_skills)
        
        # Normalize and deduplicate
        normalized_skills = list(set([self._normalize_skill(skill) for skill in skills]))
        return [skill for skill in normalized_skills if skill]
    
    def _extract_required_skills(self, job_data: Dict) -> List[str]:
        """Extract required skills from job description"""
        required_skills = []
        
        # Explicit requirements
        if "required_skills" in job_data:
            required_skills.extend(job_data["required_skills"])
        
        # Extract from job description
        if "description" in job_data:
            extracted_skills = self._extract_skills_from_text(job_data["description"])
            required_skills.extend(extracted_skills)
        
        # Extract from job title
        if "title" in job_data:
            title_skills = self._extract_skills_from_text(job_data["title"])
            required_skills.extend(title_skills)
        
        # Normalize and deduplicate
        normalized_skills = list(set([self._normalize_skill(skill) for skill in required_skills]))
        return [skill for skill in normalized_skills if skill]
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text using pattern matching"""
        skills = []
        text_lower = text.lower()
        
        # Check against all skill categories
        for category, skill_dict in self.skill_categories.items():
            if isinstance(skill_dict, dict):
                for subcategory, skill_list in skill_dict.items():
                    for skill in skill_list:
                        if skill.lower() in text_lower:
                            skills.append(skill)
            elif isinstance(skill_dict, list):
                for skill in skill_dict:
                    if skill.lower() in text_lower:
                        skills.append(skill)
        
        return skills
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill names for consistency"""
        if not skill:
            return ""
        
        # Common normalizations
        normalizations = {
            "js": "JavaScript",
            "ts": "TypeScript",
            "py": "Python",
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence",
            "aws": "AWS",
            "gcp": "Google Cloud",
            "k8s": "Kubernetes",
            "react.js": "React",
            "vue.js": "Vue.js",
            "node.js": "Node.js"
        }
        
        skill_lower = skill.lower().strip()
        return normalizations.get(skill_lower, skill.title())
    
    def _map_certification_to_skills(self, certification: str) -> List[str]:
        """Map certifications to related skills"""
        cert_lower = certification.lower()
        
        if "aws" in cert_lower:
            return ["AWS", "Cloud Computing", "DevOps"]
        elif "azure" in cert_lower:
            return ["Azure", "Cloud Computing", "Microsoft Technologies"]
        elif "google cloud" in cert_lower or "gcp" in cert_lower:
            return ["Google Cloud", "Cloud Computing", "Data Analytics"]
        elif "pmp" in cert_lower:
            return ["Project Management", "Leadership", "Strategic Planning"]
        elif "scrum" in cert_lower:
            return ["Agile", "Scrum", "Project Management"]
        elif "cissp" in cert_lower:
            return ["Cybersecurity", "Information Security", "Risk Management"]
        
        return []
    
    def _analyze_strengths(self, current_skills: set, required_skills: set) -> List[Dict[str, Any]]:
        """Analyze candidate's strengths"""
        strengths = []
        
        # Direct matches
        matching_skills = current_skills & required_skills
        if matching_skills:
            strengths.append({
                "type": "direct_match",
                "description": f"Direct match on {len(matching_skills)} required skills",
                "skills": list(matching_skills),
                "impact": "high"
            })
        
        # Transferable skills
        transferable = self._identify_transferable_skills(current_skills, required_skills)
        if transferable:
            strengths.append({
                "type": "transferable",
                "description": "Transferable skills that add value",
                "skills": transferable,
                "impact": "medium"
            })
        
        # Emerging technology adoption
        emerging_skills = self._identify_emerging_skills(current_skills)
        if emerging_skills:
            strengths.append({
                "type": "future_ready",
                "description": "Experience with emerging technologies",
                "skills": emerging_skills,
                "impact": "high"
            })
        
        return strengths
    
    def _identify_transferable_skills(self, current_skills: set, required_skills: set) -> List[str]:
        """Identify skills that are transferable to required skills"""
        transferable = []
        
        # Define skill relationships
        skill_relationships = {
            "JavaScript": ["TypeScript", "Node.js", "React", "Vue.js"],
            "Python": ["Django", "Flask", "Machine Learning", "Data Science"],
            "Java": ["Spring Boot", "Android Development", "Kotlin"],
            "SQL": ["Database Design", "Data Analytics", "Business Intelligence"],
            "Project Management": ["Agile", "Scrum", "Leadership"],
            "Machine Learning": ["AI", "Data Science", "Deep Learning"]
        }
        
        for current_skill in current_skills:
            related_skills = skill_relationships.get(current_skill, [])
            for required_skill in required_skills:
                if required_skill in related_skills:
                    transferable.append(f"{current_skill} → {required_skill}")
        
        return transferable
    
    def _identify_emerging_skills(self, current_skills: set) -> List[str]:
        """Identify emerging technology skills in current skill set"""
        emerging = []
        trending_skills = self.industry_trends["2024_trending"]["hot_skills"]
        
        for skill in current_skills:
            if skill in trending_skills:
                emerging.append(skill)
        
        return emerging
    
    def _prioritize_learning(self, missing_skills: List[str], target_job: Dict, 
                           career_goals: Dict = None) -> List[Dict[str, Any]]:
        """Prioritize learning recommendations based on multiple factors"""
        
        priorities = []
        
        for skill in missing_skills:
            priority_score = self._calculate_priority_score(skill, target_job, career_goals)
            
            learning_info = {
                "skill": skill,
                "priority_score": priority_score,
                "priority_level": self._get_priority_level(priority_score),
                "market_demand": self._get_market_demand(skill),
                "learning_difficulty": self._get_learning_difficulty(skill),
                "time_to_proficiency": self._estimate_learning_time(skill),
                "salary_impact": self._get_salary_impact(skill),
                "recommended_resources": self._get_learning_resources(skill),
                "certifications": self._get_relevant_certifications(skill),
                "prerequisites": self._get_prerequisites(skill)
            }
            
            priorities.append(learning_info)
        
        # Sort by priority score
        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return priorities
    
    def _calculate_priority_score(self, skill: str, target_job: Dict, 
                                career_goals: Dict = None) -> float:
        """Calculate priority score for a skill"""
        score = 0
        
        # Market demand factor
        market_demand = self._get_market_demand(skill)
        score += market_demand * self.skill_priorities["market_demand"] / 100
        
        # Salary impact factor
        salary_impact = self._get_salary_impact(skill)
        score += salary_impact * self.skill_priorities["salary_impact"] / 100
        
        # Learning difficulty (inverse)
        difficulty = self._get_learning_difficulty(skill)
        score += (100 - difficulty) * self.skill_priorities["learning_difficulty"] / 100
        
        # Career growth potential
        growth_potential = self._get_career_growth_potential(skill, career_goals)
        score += growth_potential * self.skill_priorities["career_growth"] / 100
        
        # Future relevance
        future_relevance = self._get_future_relevance(skill)
        score += future_relevance * self.skill_priorities["future_relevance"] / 100
        
        return round(score, 2)
    
    def _get_market_demand(self, skill: str) -> float:
        """Get market demand score for a skill (0-100)"""
        hot_skills = self.industry_trends["2024_trending"]["hot_skills"]
        emerging_skills = self.industry_trends["2024_trending"]["emerging_skills"]
        
        if skill in hot_skills:
            return 90
        elif skill in emerging_skills:
            return 75
        elif skill in ["Python", "JavaScript", "React", "AWS", "Machine Learning"]:
            return 85
        elif skill in ["Java", "SQL", "Project Management", "Data Analytics"]:
            return 70
        else:
            return 50
    
    def _get_learning_difficulty(self, skill: str) -> float:
        """Get learning difficulty score for a skill (0-100, higher means more difficult)"""
        difficulty_map = {
            "Machine Learning": 85,
            "Deep Learning": 90,
            "Kubernetes": 80,
            "System Design": 85,
            "Blockchain": 75,
            "React": 60,
            "Python": 40,
            "JavaScript": 50,
            "SQL": 45,
            "HTML/CSS": 30,
            "Project Management": 55,
            "Communication": 35
        }
        
        return difficulty_map.get(skill, 60)  # Default medium difficulty
    
    def _estimate_learning_time(self, skill: str) -> Dict[str, str]:
        """Estimate time to learn a skill to proficiency"""
        time_estimates = {
            "Python": {"beginner": "3-4 months", "proficient": "8-12 months", "expert": "2-3 years"},
            "JavaScript": {"beginner": "2-3 months", "proficient": "6-9 months", "expert": "1.5-2 years"},
            "React": {"beginner": "1-2 months", "proficient": "4-6 months", "expert": "1-1.5 years"},
            "Machine Learning": {"beginner": "6-8 months", "proficient": "1-2 years", "expert": "3-5 years"},
            "AWS": {"beginner": "2-3 months", "proficient": "6-12 months", "expert": "2-3 years"},
            "SQL": {"beginner": "1-2 months", "proficient": "4-6 months", "expert": "1-2 years"},
            "Project Management": {"beginner": "2-3 months", "proficient": "6-12 months", "expert": "2-4 years"}
        }
        
        return time_estimates.get(skill, {
            "beginner": "2-4 months", 
            "proficient": "6-12 months", 
            "expert": "1-3 years"
        })
    
    def _get_salary_impact(self, skill: str) -> float:
        """Get potential salary impact of learning a skill (0-100)"""
        high_impact_skills = [
            "Machine Learning", "AI", "Cloud Architecture", "DevOps", "Data Science",
            "Cybersecurity", "Blockchain", "System Design"
        ]
        
        medium_impact_skills = [
            "React", "Python", "AWS", "Docker", "Kubernetes", "JavaScript",
            "Project Management", "SQL", "Data Analytics"
        ]
        
        if skill in high_impact_skills:
            return 85
        elif skill in medium_impact_skills:
            return 65
        else:
            return 45
    
    def _get_career_growth_potential(self, skill: str, career_goals: Dict = None) -> float:
        """Get career growth potential score for a skill (0-100)"""
        leadership_skills = ["Project Management", "Leadership", "Strategic Planning", "Communication"]
        technical_leadership = ["System Design", "Architecture", "DevOps", "Cloud Computing"]
        
        if career_goals and career_goals.get("target_role"):
            target_role = career_goals["target_role"].lower()
            if "manager" in target_role or "lead" in target_role:
                if skill in leadership_skills:
                    return 90
                elif skill in technical_leadership:
                    return 80
            elif "architect" in target_role or "senior" in target_role:
                if skill in technical_leadership:
                    return 85
        
        # Default scoring
        if skill in leadership_skills:
            return 75
        elif skill in technical_leadership:
            return 70
        else:
            return 60
    
    def _get_future_relevance(self, skill: str) -> float:
        """Get future relevance score for a skill (0-100)"""
        future_proof_skills = [
            "AI", "Machine Learning", "Cloud Computing", "Cybersecurity",
            "Data Science", "Communication", "Leadership", "Critical Thinking"
        ]
        
        declining_skills = self.industry_trends["2024_trending"]["declining_skills"]
        
        if skill in future_proof_skills:
            return 90
        elif skill in declining_skills:
            return 20
        else:
            return 70
    
    def _get_priority_level(self, priority_score: float) -> str:
        """Convert priority score to level"""
        if priority_score >= 80:
            return "Critical"
        elif priority_score >= 65:
            return "High"
        elif priority_score >= 50:
            return "Medium"
        else:
            return "Low"
    
    def _get_learning_resources(self, skill: str) -> List[Dict[str, Any]]:
        """Get recommended learning resources for a skill"""
        resources = []
        
        # Skill-specific platform recommendations
        skill_platforms = {
            "Python": ["codecademy", "udemy", "coursera"],
            "JavaScript": ["codecademy", "udemy", "pluralsight"],
            "React": ["udemy", "pluralsight", "linkedin_learning"],
            "Machine Learning": ["coursera", "edx", "udacity"],
            "AWS": ["aws_training", "udemy", "pluralsight"],
            "Data Science": ["coursera", "edx", "udacity"],
            "Project Management": ["coursera", "udemy", "linkedin_learning"]
        }
        
        recommended_platforms = skill_platforms.get(skill, ["udemy", "coursera", "pluralsight"])
        
        for platform_key in recommended_platforms[:3]:  # Top 3 recommendations
            platform_info = self.learning_platforms.get(platform_key, {})
            if platform_info:
                resources.append({
                    "platform": platform_info["name"],
                    "url": platform_info["url"],
                    "price_range": platform_info["price_range"],
                    "rating": platform_info["rating"],
                    "best_for": platform_info["best_for"],
                    "recommendation_reason": self._get_recommendation_reason(skill, platform_key)
                })
        
        return resources
    
    def _get_recommendation_reason(self, skill: str, platform_key: str) -> str:
        """Get reason for recommending a specific platform for a skill"""
        reasons = {
            ("Python", "codecademy"): "Interactive coding environment perfect for beginners",
            ("Machine Learning", "coursera"): "University-level courses with strong theoretical foundation",
            ("AWS", "aws_training"): "Official AWS training with hands-on labs and real scenarios",
            ("React", "udemy"): "Practical project-based courses with lifetime access"
        }
        
        return reasons.get((skill, platform_key), "Highly rated courses for this skill")
    
    def _get_relevant_certifications(self, skill: str) -> List[Dict[str, Any]]:
        """Get relevant certifications for a skill"""
        skill_lower = skill.lower()
        
        for cert_category, certifications in self.certification_map.items():
            if any(keyword in skill_lower for keyword in cert_category.split('_')):
                return certifications
        
        return []
    
    def _get_prerequisites(self, skill: str) -> List[str]:
        """Get prerequisites for learning a skill"""
        prerequisites_map = {
            "React": ["JavaScript", "HTML", "CSS"],
            "Machine Learning": ["Python", "Statistics", "Linear Algebra"],
            "Deep Learning": ["Machine Learning", "Python", "Neural Networks"],
            "Kubernetes": ["Docker", "Linux", "Networking"],
            "AWS": ["Cloud Computing Basics", "Linux", "Networking"],
            "Data Science": ["Python", "Statistics", "SQL"],
            "DevOps": ["Linux", "Scripting", "Version Control"]
        }
        
        return prerequisites_map.get(skill, [])
    
    def _calculate_time_investment(self, learning_priorities: List[Dict]) -> Dict[str, Any]:
        """Calculate total time investment for learning plan"""
        total_beginner_months = 0
        total_proficient_months = 0
        
        for priority in learning_priorities[:5]:  # Top 5 priorities
            time_est = priority["time_to_proficiency"]
            
            # Parse time estimates (simplified)
            beginner_time = time_est.get("beginner", "3 months")
            proficient_time = time_est.get("proficient", "6 months")
            
            # Extract months (simplified parsing)
            beginner_months = self._parse_time_to_months(beginner_time)
            proficient_months = self._parse_time_to_months(proficient_time)
            
            total_beginner_months += beginner_months
            total_proficient_months += proficient_months
        
        return {
            "total_beginner_level": f"{total_beginner_months} months",
            "total_proficient_level": f"{total_proficient_months} months",
            "recommended_approach": "Focus on 2-3 skills simultaneously for optimal learning",
            "daily_commitment": "2-3 hours per day recommended",
            "learning_phases": [
                {"phase": "Foundation", "duration": "3-6 months", "focus": "Core skills"},
                {"phase": "Specialization", "duration": "6-12 months", "focus": "Advanced topics"},
                {"phase": "Mastery", "duration": "12+ months", "focus": "Expert-level application"}
            ]
        }
    
    def _parse_time_to_months(self, time_str: str) -> int:
        """Parse time string to months (simplified)"""
        if "month" in time_str.lower():
            numbers = re.findall(r'\d+', time_str)
            if numbers:
                return int(numbers[0])
        elif "year" in time_str.lower():
            numbers = re.findall(r'\d+', time_str)
            if numbers:
                return int(numbers[0]) * 12
        return 3  # Default fallback
    
    def _calculate_learning_roi(self, learning_priorities: List[Dict], 
                              target_job: Dict) -> Dict[str, Any]:
        """Calculate return on investment for learning recommendations"""
        
        total_investment = 0
        potential_salary_increase = 0
        
        for priority in learning_priorities[:3]:  # Top 3 priorities
            # Estimate learning cost (assuming $50/month average)
            learning_months = self._parse_time_to_months(
                priority["time_to_proficiency"].get("proficient", "6 months")
            )
            skill_cost = learning_months * 50
            total_investment += skill_cost
            
            # Estimate salary impact
            salary_impact = priority["salary_impact"]
            current_salary = target_job.get("salary_range", {}).get("average", 75000)
            salary_increase = current_salary * (salary_impact / 100) * 0.1  # Conservative estimate
            potential_salary_increase += salary_increase
        
        roi_percentage = ((potential_salary_increase - total_investment) / total_investment * 100) if total_investment > 0 else 0
        
        return {
            "total_investment": f"${total_investment:,.0f}",
            "potential_annual_increase": f"${potential_salary_increase:,.0f}",
            "roi_percentage": f"{roi_percentage:.1f}%",
            "payback_period": f"{max(1, total_investment / (potential_salary_increase / 12)):.1f} months",
            "5_year_value": f"${(potential_salary_increase * 5 - total_investment):,.0f}",
            "confidence_level": "Medium - based on industry averages",
            "factors": [
                "Market demand for skills",
                "Geographic location impact",
                "Company size and industry",
                "Individual performance and negotiation"
            ]
        }
    
    def create_learning_roadmap(self, skill_analysis: Dict, timeframe: str = "12_months") -> Dict[str, Any]:
        """Create a detailed learning roadmap"""
        
        roadmap = {
            "timeframe": timeframe,
            "created_date": datetime.now().isoformat(),
            "phases": [],
            "milestones": [],
            "weekly_schedule": {},
            "progress_tracking": {},
            "resources": [],
            "certification_timeline": []
        }
        
        priorities = skill_analysis.get("learning_priorities", [])[:5]  # Top 5 skills
        
        # Create phases based on timeframe
        if timeframe == "6_months":
            phases = [
                {"name": "Foundation", "duration": "2 months", "skills": priorities[:2]},
                {"name": "Building", "duration": "2 months", "skills": priorities[2:4]},
                {"name": "Integration", "duration": "2 months", "skills": priorities[4:5]}
            ]
        elif timeframe == "12_months":
            phases = [
                {"name": "Foundation", "duration": "3 months", "skills": priorities[:2]},
                {"name": "Expansion", "duration": "4 months", "skills": priorities[2:4]},
                {"name": "Specialization", "duration": "3 months", "skills": priorities[4:5]},
                {"name": "Mastery", "duration": "2 months", "skills": "All skills - advanced topics"}
            ]
        
        for i, phase in enumerate(phases):
            phase_detail = {
                "phase_number": i + 1,
                "name": phase["name"],
                "duration": phase["duration"],
                "objectives": self._get_phase_objectives(phase["name"]),
                "skills_focus": phase["skills"] if isinstance(phase["skills"], str) else [s["skill"] for s in phase["skills"]],
                "deliverables": self._get_phase_deliverables(phase["name"]),
                "success_metrics": self._get_phase_metrics(phase["name"])
            }
            roadmap["phases"].append(phase_detail)
        
        # Create milestones
        roadmap["milestones"] = self._create_milestones(priorities, timeframe)
        
        # Weekly schedule
        roadmap["weekly_schedule"] = self._create_weekly_schedule(priorities)
        
        # Progress tracking
        roadmap["progress_tracking"] = self._create_progress_tracking(priorities)
        
        # Certification timeline
        roadmap["certification_timeline"] = self._create_certification_timeline(priorities, timeframe)
        
        return roadmap
    
    def _get_phase_objectives(self, phase_name: str) -> List[str]:
        """Get objectives for a learning phase"""
        objectives_map = {
            "Foundation": [
                "Build strong fundamental understanding",
                "Complete basic tutorials and exercises",
                "Set up development environment",
                "Create first simple projects"
            ],
            "Building": [
                "Develop intermediate skills",
                "Work on practical projects",
                "Learn best practices and patterns",
                "Start building portfolio"
            ],
            "Expansion": [
                "Explore advanced topics",
                "Integrate multiple skills",
                "Contribute to open source projects",
                "Network with professionals"
            ],
            "Specialization": [
                "Focus on specific domain expertise",
                "Lead complex projects",
                "Mentor others",
                "Prepare for certifications"
            ],
            "Integration": [
                "Combine all learned skills",
                "Complete capstone project",
                "Prepare for job applications",
                "Practice interviews"
            ],
            "Mastery": [
                "Achieve expert-level proficiency",
                "Teach and share knowledge",
                "Stay updated with latest trends",
                "Plan next learning goals"
            ]
        }
        
        return objectives_map.get(phase_name, ["Continue skill development"])
    
    def _get_phase_deliverables(self, phase_name: str) -> List[str]:
        """Get deliverables for a learning phase"""
        deliverables_map = {
            "Foundation": [
                "Completed course certificates",
                "Basic project implementations",
                "Learning journal/notes",
                "Skill assessment results"
            ],
            "Building": [
                "Portfolio projects",
                "Code repositories",
                "Technical blog posts",
                "Peer review participation"
            ],
            "Expansion": [
                "Advanced project implementations",
                "Open source contributions",
                "Technical presentations",
                "Professional networking"
            ],
            "Specialization": [
                "Domain-specific projects",
                "Industry certifications",
                "Thought leadership content",
                "Mentorship activities"
            ],
            "Integration": [
                "Capstone project",
                "Updated resume and portfolio",
                "Interview preparation materials",
                "Job application submissions"
            ],
            "Mastery": [
                "Expert-level projects",
                "Teaching/training materials",
                "Industry conference participation",
                "Next learning plan"
            ]
        }
        
        return deliverables_map.get(phase_name, ["Phase completion documentation"])
    
    def _get_phase_metrics(self, phase_name: str) -> List[str]:
        """Get success metrics for a learning phase"""
        return [
            "Skill assessment scores",
            "Project completion rate",
            "Time spent learning",
            "Peer feedback scores",
            "Certification progress"
        ]
    
    def _create_milestones(self, priorities: List[Dict], timeframe: str) -> List[Dict]:
        """Create learning milestones"""
        milestones = []
        
        # Calculate milestone intervals
        total_months = 12 if timeframe == "12_months" else 6
        milestone_interval = total_months // 4
        
        for i in range(4):
            month = (i + 1) * milestone_interval
            milestone = {
                "milestone_number": i + 1,
                "target_month": month,
                "title": f"Milestone {i + 1}",
                "description": self._get_milestone_description(i + 1),
                "skills_to_complete": [p["skill"] for p in priorities[:(i + 1) * 2]][:5],
                "success_criteria": [
                    "Pass skill assessments",
                    "Complete practical projects",
                    "Demonstrate proficiency",
                    "Update portfolio"
                ]
            }
            milestones.append(milestone)
        
        return milestones
    
    def _get_milestone_description(self, milestone_number: int) -> str:
        """Get description for a milestone"""
        descriptions = {
            1: "Foundation skills established",
            2: "Intermediate proficiency achieved",
            3: "Advanced skills demonstrated",
            4: "Job-ready competency reached"
        }
        return descriptions.get(milestone_number, f"Milestone {milestone_number} completed")
    
    def _create_weekly_schedule(self, priorities: List[Dict]) -> Dict[str, Any]:
        """Create recommended weekly learning schedule"""
        return {
            "total_hours_per_week": "15-20 hours",
            "daily_breakdown": {
                "monday": {"hours": "2-3", "focus": "New concept learning"},
                "tuesday": {"hours": "2-3", "focus": "Hands-on practice"},
                "wednesday": {"hours": "2-3", "focus": "Project work"},
                "thursday": {"hours": "2-3", "focus": "Review and reinforcement"},
                "friday": {"hours": "2-3", "focus": "Portfolio development"},
                "saturday": {"hours": "3-4", "focus": "Extended project time"},
                "sunday": {"hours": "2-3", "focus": "Planning and reflection"}
            },
            "skill_rotation": "Focus on 2-3 skills per week",
            "break_recommendations": "Take breaks every 45-60 minutes",
            "weekly_goals": [
                "Complete 2-3 learning modules",
                "Finish 1 practical exercise",
                "Update portfolio with new work",
                "Review and plan next week"
            ]
        }
    
    def _create_progress_tracking(self, priorities: List[Dict]) -> Dict[str, Any]:
        """Create progress tracking system"""
        return {
            "tracking_methods": [
                "Weekly self-assessments",
                "Project completion tracking",
                "Skill level evaluations",
                "Time investment logging",
                "Portfolio updates"
            ],
            "assessment_schedule": {
                "weekly": "Quick skill check-ins",
                "monthly": "Comprehensive skill assessment",
                "quarterly": "Portfolio review and goal adjustment"
            },
            "key_metrics": [
                "Hours spent learning each skill",
                "Number of projects completed",
                "Skill assessment scores",
                "Course completion rates",
                "Job application success rate"
            ],
            "tracking_tools": [
                "Learning management system",
                "Time tracking apps",
                "GitHub for code projects",
                "Portfolio website",
                "Learning journal"
            ]
        }
    
    def _create_certification_timeline(self, priorities: List[Dict], timeframe: str) -> List[Dict]:
        """Create certification timeline"""
        timeline = []
        
        for i, priority in enumerate(priorities[:3]):
            certifications = priority.get("certifications", [])
            if certifications:
                cert = certifications[0]  # Take the first certification
                target_month = (i + 1) * (6 if timeframe == "12_months" else 3)
                
                timeline.append({
                    "certification": cert["name"],
                    "provider": cert["provider"],
                    "target_month": target_month,
                    "difficulty": cert["difficulty"],
                    "cost": cert["cost"],
                    "preparation_time": "6-8 weeks",
                    "prerequisites": priority.get("prerequisites", []),
                    "study_plan": [
                        "Review certification guide",
                        "Complete practice exams",
                        "Hands-on lab exercises",
                        "Schedule and take exam"
                    ]
                })
        
        return timeline
    
    def get_fallback_response(self, response_type: str) -> Any:
        """Provide fallback responses when AI is unavailable"""
        fallback_responses = {
            "skill_gaps": {
                "missing_critical": ["Skills analysis in progress"],
                "gap_percentage": 30,
                "learning_priorities": [
                    {
                        "skill": "Python",
                        "priority_level": "High",
                        "time_to_proficiency": {"beginner": "3 months", "proficient": "8 months"},
                        "market_demand": 85
                    }
                ]
            },
            "learning_roadmap": {
                "phases": [
                    {"name": "Foundation", "duration": "3 months"},
                    {"name": "Building", "duration": "4 months"},
                    {"name": "Specialization", "duration": "3 months"}
                ],
                "total_investment": "$1,500",
                "expected_roi": "250%"
            }
        }
        
        return fallback_responses.get(response_type, "Fallback response not available")
    
    def run(self, resume_data: Dict, target_job: Dict, career_goals: Dict = None,
            analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Main execution method for skill recommendation functionality"""
        
        try:
            # Perform skill gap analysis
            skill_analysis = self.analyze_skill_gaps(resume_data, target_job, career_goals)
            
            result = {
                "analysis_type": analysis_type,
                "skill_analysis": skill_analysis,
                "personalized_recommendations": [],
                "learning_roadmap": {},
                "industry_insights": {},
                "next_steps": []
            }
            
            if analysis_type in ["comprehensive", "roadmap"]:
                # Create learning roadmap
                timeframe = career_goals.get("timeframe", "12_months") if career_goals else "12_months"
                result["learning_roadmap"] = self.create_learning_roadmap(skill_analysis, timeframe)
            
            if analysis_type in ["comprehensive", "industry"]:
                # Add industry insights
                result["industry_insights"] = {
                    "trending_skills": self.industry_trends["2024_trending"]["hot_skills"][:5],
                    "emerging_opportunities": self.industry_trends["2024_trending"]["emerging_skills"][:3],
                    "salary_impact_skills": [p["skill"] for p in skill_analysis["learning_priorities"][:3] if p["salary_impact"] > 70]
                }
            
            # Generate personalized recommendations
            result["personalized_recommendations"] = self._generate_personalized_recommendations(
                skill_analysis, target_job, career_goals
            )
            
            # Next steps
            result["next_steps"] = [
                "Review prioritized skill recommendations",
                "Select 2-3 skills to focus on initially",
                "Enroll in recommended courses",
                "Set up progress tracking system",
                "Plan first milestone goals"
            ]
            
            log_interaction("SkillRecommendationAgent", "run", 
                          target_job.get("title", "Unknown Job"), 
                          json.dumps(result, indent=2, default=str))
            
            return result
            
        except Exception as e:
            logging.error(f"Error in SkillRecommendationAgent.run: {e}")
            return {
                "error": str(e),
                "fallback_advice": [
                    "Research industry skill requirements manually",
                    "Use online skill assessment tools",
                    "Network with professionals in target field",
                    "Consider general skill development courses"
                ]
            }
    
    def _generate_personalized_recommendations(self, skill_analysis: Dict, 
                                             target_job: Dict, career_goals: Dict = None) -> List[Dict]:
        """Generate personalized recommendations based on analysis"""
        recommendations = []
        
        # Top skill recommendations
        top_skills = skill_analysis.get("learning_priorities", [])[:3]
        for skill_info in top_skills:
            recommendations.append({
                "type": "skill_development",
                "title": f"Learn {skill_info['skill']}",
                "priority": skill_info["priority_level"],
                "reasoning": f"High market demand ({skill_info['market_demand']}%) and significant salary impact",
                "action_items": [
                    f"Start with {skill_info['recommended_resources'][0]['platform']} course",
                    "Practice with hands-on projects",
                    "Join relevant online communities",
                    "Consider certification path"
                ],
                "timeline": skill_info["time_to_proficiency"]["proficient"]
            })
        
        # Career-specific recommendations
        if career_goals:
            target_role = career_goals.get("target_role", "")
            if "senior" in target_role.lower() or "lead" in target_role.lower():
                recommendations.append({
                    "type": "leadership_development",
                    "title": "Develop Leadership Skills",
                    "priority": "High",
                    "reasoning": "Essential for senior/leadership roles",
                    "action_items": [
                        "Take project management courses",
                        "Seek mentorship opportunities",
                        "Lead team projects",
                        "Develop communication skills"
                    ],
                    "timeline": "6-12 months"
                })
        
        # Industry-specific recommendations
        industry = target_job.get("industry", "technology")
        if industry in self.industry_trends["by_industry"]:
            industry_data = self.industry_trends["by_industry"][industry]
            recommendations.append({
                "type": "industry_alignment",
                "title": f"Align with {industry.title()} Industry Trends",
                "priority": "Medium",
                "reasoning": f"Industry growing at {industry_data['growth_rate']} annually",
                "action_items": [
                    f"Focus on {', '.join(industry_data['high_demand'][:2])}",
                    "Follow industry thought leaders",
                    "Attend industry conferences/webinars",
                    "Build industry-specific portfolio"
                ],
                "timeline": "3-6 months"
            })
        
        return recommendations
