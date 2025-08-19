from agents.multi_ai_base import MultiAIAgent
from agents.web_scraper_agent import WebScraperAgent
import logging
from typing import Dict, List


class AdvancedInterviewPrepAgent(MultiAIAgent):
    """Advanced interview preparation with real-time company and role research"""
    
    def __init__(self, firecrawl_api_key: str = None):
        super().__init__(
            name="AdvancedInterviewPrepAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )
        self.web_scraper = WebScraperAgent(firecrawl_api_key)
    
    def comprehensive_interview_prep(self, user_data: Dict, job_data: Dict) -> Dict:
        """Generate comprehensive interview preparation with live research"""
        try:
            # Research company using Firecrawl
            company_research = self.web_scraper.scrape_company_info(
                job_data.get("company", ""),
                job_data.get("company_url", "")
            )
            
            # Scrape interview questions from Glassdoor and other sources
            interview_questions = self.web_scraper.scrape_interview_questions(
                job_data.get("company", ""),
                job_data.get("title", "")
            )
            
            # Generate personalized preparation
            prep_content = self._generate_personalized_prep(user_data, job_data, company_research)
            
            # Create mock interview scenarios
            mock_interviews = self._create_mock_interview_scenarios(user_data, job_data, company_research)
            
            # Generate follow-up strategies
            follow_up_plan = self._generate_follow_up_plan(job_data, company_research)
            
            return {
                "success": True,
                "company_research": company_research,
                "interview_questions": interview_questions,
                "personalized_prep": prep_content,
                "mock_interviews": mock_interviews,
                "follow_up_plan": follow_up_plan,
                "preparation_timeline": self._create_prep_timeline(),
                "confidence_boosters": self._generate_confidence_tips(user_data)
            }
            
        except Exception as e:
            logging.error(f"Error in comprehensive interview prep: {e}")
            return self._fallback_comprehensive_prep(user_data, job_data)
    
    def practice_interview_simulation(self, user_data: Dict, job_data: Dict, difficulty: str = "medium") -> Dict:
        """Create interactive interview simulation"""
        try:
            # Generate questions based on difficulty
            questions = self._generate_simulation_questions(job_data, difficulty)
            
            # Create evaluation criteria
            evaluation_criteria = self._create_evaluation_criteria(job_data)
            
            # Generate sample answers for reference
            sample_answers = self._generate_sample_answers(questions, user_data)
            
            return {
                "success": True,
                "simulation_questions": questions,
                "evaluation_criteria": evaluation_criteria,
                "sample_answers": sample_answers,
                "difficulty_level": difficulty,
                "estimated_duration": f"{len(questions) * 3} minutes",
                "tips": self._generate_simulation_tips()
            }
            
        except Exception as e:
            logging.error(f"Error in interview simulation: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_personalized_prep(self, user_data: Dict, job_data: Dict, company_research: Dict) -> Dict:
        """Generate personalized interview preparation content"""
        
        company_insights = company_research.get("insights", {})
        
        prompt = f"""
        Create personalized interview preparation for this candidate:
        
        Candidate Profile:
        - Name: {user_data.get('name', '')}
        - Experience: {user_data.get('years_experience', 0)} years
        - Current Role: {user_data.get('current_role', '')}
        - Skills: {', '.join(user_data.get('skills', [])[:10])}
        - Achievements: {', '.join(user_data.get('achievements', [])[:3])}
        
        Target Position:
        - Role: {job_data.get('title', '')}
        - Company: {job_data.get('company', '')}
        - Job Description: {job_data.get('description', '')[:1000]}
        
        Company Research:
        - Overview: {company_insights.get('company_overview', '')}
        - Culture: {company_insights.get('company_culture', '')}
        - Values: {', '.join(company_insights.get('values', []))}
        - Recent News: {', '.join(company_insights.get('recent_news', [])[:3])}
        
        Generate:
        1. Personalized talking points that connect candidate's experience to role
        2. Company-specific questions to ask interviewer
        3. Stories to tell using STAR method based on candidate's background
        4. How to address potential weaknesses or gaps
        5. Salary negotiation strategy based on role and experience
        6. Cultural fit talking points
        
        Make it specific and actionable.
        """
        
        try:
            prep_response = self.generate_ai_response(prompt)
            return {"content": prep_response, "personalized": True}
        except Exception:
            return {"content": "Personalized preparation content unavailable", "personalized": False}
    
    def _create_mock_interview_scenarios(self, user_data: Dict, job_data: Dict, company_research: Dict) -> List[Dict]:
        """Create realistic mock interview scenarios"""
        
        scenarios = [
            {
                "scenario_name": "Technical Deep Dive",
                "description": "Technical questions specific to the role",
                "duration": "20-30 minutes",
                "focus_areas": ["Technical skills", "Problem-solving", "System design"],
                "sample_questions": self._generate_technical_questions(job_data)
            },
            {
                "scenario_name": "Behavioral Assessment",
                "description": "Behavioral and situational questions",
                "duration": "15-25 minutes", 
                "focus_areas": ["Leadership", "Teamwork", "Conflict resolution"],
                "sample_questions": self._generate_behavioral_questions(user_data)
            },
            {
                "scenario_name": "Company Culture Fit",
                "description": "Questions about values and culture alignment",
                "duration": "10-15 minutes",
                "focus_areas": ["Values alignment", "Cultural fit", "Motivation"],
                "sample_questions": self._generate_culture_questions(company_research)
            }
        ]
        
        return scenarios
    
    def _generate_technical_questions(self, job_data: Dict) -> List[str]:
        """Generate technical questions based on job requirements"""
        
        job_description = job_data.get("description", "")
        
        prompt = f"""
        Generate 10 technical interview questions for this role:
        
        Job Title: {job_data.get('title', '')}
        Job Description: {job_description[:1500]}
        
        Create questions that test:
        1. Core technical skills mentioned in job description
        2. Problem-solving abilities
        3. System design thinking
        4. Best practices knowledge
        5. Real-world application scenarios
        
        Make questions specific and challenging but fair.
        """
        
        try:
            questions_response = self.generate_ai_response(prompt)
            return questions_response.split('\n')[:10]
        except Exception:
            return [
                "Describe your approach to solving complex technical problems",
                "How do you ensure code quality in your projects?",
                "Explain a challenging technical decision you made recently",
                "How do you stay updated with new technologies?",
                "Describe your experience with the technologies mentioned in the job description"
            ]
    
    def _generate_follow_up_plan(self, job_data: Dict, company_research: Dict) -> Dict:
        """Generate post-interview follow-up strategy"""
        
        return {
            "immediate_followup": {
                "timing": "Within 24 hours",
                "actions": [
                    "Send personalized thank-you email to each interviewer",
                    "Reiterate interest and key qualifications",
                    "Address any concerns raised during interview",
                    "Provide additional information if requested"
                ]
            },
            "week_1_followup": {
                "timing": "1 week after interview",
                "actions": [
                    "Send brief check-in email if no response",
                    "Share relevant article or insight related to company/role",
                    "Connect with interviewers on LinkedIn"
                ]
            },
            "ongoing_engagement": {
                "timing": "Throughout process",
                "actions": [
                    "Engage with company content on social media",
                    "Attend company events or webinars",
                    "Continue researching company developments",
                    "Prepare for potential additional rounds"
                ]
            },
            "email_templates": self._generate_followup_templates(job_data, company_research)
        }
    
    def _generate_followup_templates(self, job_data: Dict, company_research: Dict) -> Dict:
        """Generate email templates for follow-up"""
        
        company_name = job_data.get("company", "")
        role_title = job_data.get("title", "")
        
        return {
            "thank_you_email": f"""
Subject: Thank you for the {role_title} interview

Dear [Interviewer Name],

Thank you for taking the time to discuss the {role_title} position with me today. I was excited to learn more about [specific project/initiative mentioned] and how this role contributes to {company_name}'s mission.

Our conversation reinforced my enthusiasm for this opportunity, particularly [specific aspect discussed]. I believe my experience in [relevant experience] would enable me to make a meaningful contribution to your team.

Please let me know if you need any additional information from me. I look forward to hearing about the next steps.

Best regards,
[Your Name]
            """,
            "follow_up_email": f"""
Subject: Following up on {role_title} interview

Dear [Interviewer Name],

I wanted to follow up on our interview for the {role_title} position. I remain very interested in the opportunity and excited about the possibility of joining the {company_name} team.

Since our conversation, I've been thinking about [specific topic discussed] and wanted to share [additional insight/resource] that might be relevant to the challenges you mentioned.

I'm happy to provide any additional information that would be helpful for your decision-making process.

Thank you again for your time and consideration.

Best regards,
[Your Name]
            """
        }