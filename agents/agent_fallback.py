"""
Agent Fallback Handler - Provides fallback implementations for all agent functions
Used when main agent implementations are not available or fail
"""

import random
import logging


class AgentFallbackHandler:
    """Provides fallback implementations for all agent methods when actual agents fail"""

    @staticmethod
    def controller_analyze_resume(resume_text, job_title=""):
        """Fallback for resume analysis"""
        logging.warning("Using fallback resume analysis")

        # Generate random skills for demonstration
        all_skills = [
            "Python",
            "JavaScript",
            "React",
            "Data Analysis",
            "SQL",
            "Machine Learning",
            "Project Management",
            "Communication",
            "Leadership",
            "Problem Solving",
        ]
        matched_skills = random.sample(all_skills, k=random.randint(3, 6))
        suggested_skills = [s for s in all_skills if s not in matched_skills][
            : random.randint(2, 4)
        ]

        return {
            "match_result": {
                "match_percent": random.randint(65, 92),
                "matched_skills": matched_skills,
                "suggested_skills": suggested_skills,
                "additional_skills": random.sample(matched_skills, k=2),
            },
            "feedback": "This is a placeholder feedback for your resume. In production, our AI would provide detailed feedback on your resume's strengths and areas for improvement.",
            "job_titles": "Based on your resume, you might be a good fit for:\n\n1. **Software Developer**\n2. **Data Analyst**\n3. **Project Manager**",
            "job_description": "# Sample Job Description\n\nThis is a placeholder job description. In production, our AI would generate a custom job description tailored to your skills and experience.",
        }

    @staticmethod
    def company_research(company_name):
        """Fallback for company research"""
        logging.warning("Using fallback company research")

        return {
            "overview": {
                "founded": "2010",
                "employee_count": "500-1000",
                "industry": "Technology",
                "description": f"This is a placeholder description for {company_name}. In production, our AI would provide detailed information about the company's history, products, services, and market position.",
            },
            "culture": {
                "values": [
                    "Innovation",
                    "Teamwork",
                    "Customer Focus",
                    "Integrity",
                    "Excellence",
                ],
                "work_environment": f"Employees at {company_name} generally report a positive work environment with opportunities for growth and development.",
            },
            "recent_news": [
                {
                    "title": f"{company_name} Announces New Product",
                    "date": "June 15, 2025",
                    "summary": "The company recently announced a new product line focusing on sustainability.",
                },
                {
                    "title": f"{company_name} Expands to New Markets",
                    "date": "May 22, 2025",
                    "summary": "The company is expanding operations to international markets.",
                },
            ],
        }

    @staticmethod
    def generate_skill_recommendations(current_skills, target_job):
        """Fallback for skill recommendations"""
        logging.warning("Using fallback skill recommendations")

        all_tech_skills = [
            "Python",
            "JavaScript",
            "React",
            "Angular",
            "Vue.js",
            "Node.js",
            "AWS",
            "Azure",
            "SQL",
            "NoSQL",
            "Docker",
            "Kubernetes",
            "Machine Learning",
            "Data Analysis",
            "Big Data",
            "DevOps",
            "CI/CD",
            "Git",
            "Agile",
            "Scrum",
        ]

        all_soft_skills = [
            "Communication",
            "Leadership",
            "Problem Solving",
            "Critical Thinking",
            "Teamwork",
            "Time Management",
            "Creativity",
            "Adaptability",
            "Emotional Intelligence",
        ]

        # Convert input to list if it's a string
        if isinstance(current_skills, str):
            current_skills = [s.strip() for s in current_skills.split(",")]

        # Generate random recommendations
        missing_tech = [s for s in all_tech_skills if s not in current_skills][:3]
        missing_soft = [s for s in all_soft_skills if s not in current_skills][:2]

        return {
            "skill_analysis": {
                "skill_gaps": {
                    "gap_percentage": random.randint(15, 40),
                    "present_skills": current_skills,
                    "missing_critical": missing_tech + missing_soft,
                },
                "learning_priorities": [
                    {
                        "skill": skill,
                        "priority_level": "High" if i < 2 else "Medium",
                        "market_demand": random.randint(75, 95),
                        "salary_impact": random.randint(5, 15),
                        "learning_difficulty": random.randint(30, 70),
                        "time_to_proficiency": {
                            "proficient": f"{random.randint(1, 6)} months"
                        },
                        "prerequisites": random.sample(
                            current_skills, k=min(2, len(current_skills))
                        ),
                        "recommended_resources": [
                            {
                                "platform": "Udemy",
                                "url": "https://udemy.com",
                                "price_range": "$10-$20",
                            },
                            {
                                "platform": "Coursera",
                                "url": "https://coursera.org",
                                "price_range": "$39-$79/month",
                            },
                        ],
                    }
                    for i, skill in enumerate(missing_tech[:3] + missing_soft[:1])
                ],
            }
        }

    @staticmethod
    def salary_negotiation_advice(
        job_title, experience_level="mid", current_salary=None, location=""
    ):
        """Fallback for salary negotiation advice"""
        logging.warning("Using fallback salary negotiation advice")

        # Generate placeholder salary data
        avg_salary = random.randint(70000, 120000)
        salary_range = {
            "low": int(avg_salary * 0.85),
            "median": avg_salary,
            "high": int(avg_salary * 1.15),
        }

        # Adjust based on experience level
        if experience_level.lower() == "senior":
            for key in salary_range:
                salary_range[key] = int(salary_range[key] * 1.3)
        elif experience_level.lower() == "junior":
            for key in salary_range:
                salary_range[key] = int(salary_range[key] * 0.7)

        return {
            "market_data": {
                "salary_range": salary_range,
                "location_adjustment": f"Salaries in {location or 'your area'} are typically {random.choice(['above', 'at', 'slightly below'])} the national average.",
            },
            "negotiation_tips": [
                "Research the market rate for your role and experience level",
                "Highlight your unique skills and accomplishments",
                "Consider the total compensation package, not just salary",
                "Practice your negotiation conversation ahead of time",
                "Start slightly higher than your target salary",
                "Be confident but collaborative in your approach",
            ],
            "scripts": {
                "initial_response": f"Thank you for the offer. I'm excited about the opportunity to join your team. Based on my research and experience, I was expecting a salary in the range of ${salary_range['median']} to ${salary_range['high']}.",
                "counter_offer": "I understand your constraints. Would it be possible to meet in the middle at $X? I believe this reflects the value I'll bring to the team.",
                "benefits_discussion": "Besides the base salary, I'd like to discuss other aspects of compensation such as bonuses, equity, professional development, and flexible work arrangements.",
            },
        }

    @staticmethod
    def job_market_intelligence(job_title, location=""):
        """Fallback for job market intelligence"""
        logging.warning("Using fallback job market intelligence")

        # Sample job market data
        return {
            "market_trends": {
                "growth_rate": f"{random.randint(2, 15)}% annual growth",
                "demand_level": random.choice(["High", "Moderate", "Very High"]),
                "competition": random.choice(["High", "Moderate", "Increasing"]),
            },
            "location_insights": {
                "top_hiring_regions": [
                    "San Francisco",
                    "New York",
                    "Austin",
                    "Seattle",
                    "Boston",
                ],
                "remote_opportunities": f"{random.randint(30, 70)}% of positions offer remote work",
                "cost_of_living_adjustment": f"Salaries in {location or 'major tech hubs'} are typically {random.randint(5, 25)}% higher than the national average",
            },
            "industry_sectors": {
                "fastest_growing": [
                    "Healthcare Tech",
                    "Fintech",
                    "E-commerce",
                    "Cybersecurity",
                    "AI/ML",
                ],
                "highest_paying": [
                    "Finance",
                    "Healthcare",
                    "Technology",
                    "Consulting",
                    "Pharmaceuticals",
                ],
            },
            "required_skills": {
                "technical": [
                    "Data Analysis",
                    "Programming",
                    "Project Management",
                    "Cloud Computing",
                    "AI/ML",
                ],
                "soft": [
                    "Communication",
                    "Leadership",
                    "Problem Solving",
                    "Adaptability",
                    "Teamwork",
                ],
            },
            "education_requirements": {
                "degree_levels": {
                    "Bachelor's": f"{random.randint(50, 70)}%",
                    "Master's": f"{random.randint(20, 40)}%",
                    "PhD": f"{random.randint(1, 10)}%",
                    "No Degree Required": f"{random.randint(5, 15)}%",
                }
            },
            "future_outlook": {
                "prediction": f"The demand for {job_title} is expected to {random.choice(['increase', 'remain strong', 'grow significantly'])} over the next 3-5 years.",
                "emerging_skills": [
                    "AI Ethics",
                    "Quantum Computing",
                    "Sustainability",
                    "Remote Team Management",
                ],
            },
        }
