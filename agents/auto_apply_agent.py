"""
AutoApplyAgent - Automates form-filling and job applications
Handles multiple job platforms, form parsing, and automated submissions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.multi_ai_base import MultiAIAgent
from utils.sqlite_logger import log_interaction
import json
import logging
from typing import Dict, List, Optional, Any
import re


class AutoApplyAgent(MultiAIAgent):
    """Agent that automates job application form filling and submission"""
    
    def __init__(self):
        super().__init__("AutoApplyAgent")
        self.supported_platforms = [
            "linkedin", "indeed", "glassdoor", "monster", "ziprecruiter",
            "workday", "greenhouse", "lever", "smartrecruiters", "taleo"
        ]
        self.application_templates = self._load_application_templates()
        self.form_field_mappings = self._create_field_mappings()
        
    def _load_application_templates(self) -> Dict[str, Dict]:
        """Load pre-configured application templates for different platforms"""
        return {
            "linkedin": {
                "required_fields": ["first_name", "last_name", "email", "phone", "resume_file"],
                "optional_fields": ["cover_letter", "portfolio_url", "linkedin_url", "work_authorization"],
                "field_selectors": {
                    "first_name": "input[name*='firstName'], input[id*='first-name']",
                    "last_name": "input[name*='lastName'], input[id*='last-name']",
                    "email": "input[type='email'], input[name*='email']",
                    "phone": "input[type='tel'], input[name*='phone']",
                    "resume_upload": "input[type='file'][accept*='pdf']"
                }
            },
            "indeed": {
                "required_fields": ["full_name", "email", "phone", "resume_file"],
                "optional_fields": ["cover_letter", "salary_expectation", "availability"],
                "field_selectors": {
                    "full_name": "input[name*='name'], input[id*='name']",
                    "email": "input[type='email']",
                    "phone": "input[name*='phone'], input[type='tel']",
                    "resume_upload": "input[type='file']"
                }
            },
            "workday": {
                "required_fields": ["first_name", "last_name", "email", "phone", "address"],
                "optional_fields": ["work_authorization", "sponsorship", "disability", "veteran_status"],
                "field_selectors": {
                    "first_name": "[data-automation-id*='firstName']",
                    "last_name": "[data-automation-id*='lastName']",
                    "email": "[data-automation-id*='email']",
                    "phone": "[data-automation-id*='phone']"
                }
            }
        }
    
    def _create_field_mappings(self) -> Dict[str, List[str]]:
        """Create intelligent field mappings for common form fields"""
        return {
            "name": ["first_name", "last_name", "full_name", "name", "firstName", "lastName"],
            "email": ["email", "email_address", "emailAddress", "e_mail"],
            "phone": ["phone", "phone_number", "phoneNumber", "mobile", "telephone"],
            "address": ["address", "street_address", "home_address", "location"],
            "city": ["city", "town", "municipality"],
            "state": ["state", "province", "region"],
            "zip": ["zip", "postal_code", "zipcode", "postcode"],
            "country": ["country", "nation"],
            "linkedin": ["linkedin", "linkedin_url", "linkedin_profile"],
            "portfolio": ["portfolio", "website", "personal_website", "portfolio_url"],
            "work_auth": ["work_authorization", "authorized_to_work", "visa_status"],
            "salary": ["salary", "salary_expectation", "expected_salary", "compensation"],
            "availability": ["start_date", "availability", "available_start_date"],
            "cover_letter": ["cover_letter", "coverletter", "message", "additional_info"]
        }
    
    def analyze_job_posting(self, job_url: str, job_description: str) -> Dict[str, Any]:
        """Analyze job posting to extract key requirements and optimize application"""
        prompt = f"""
        Analyze this job posting and provide strategic application insights:
        
        Job URL: {job_url}
        Job Description: {job_description}
        
        Please provide:
        1. Key requirements and must-have skills
        2. Nice-to-have skills and qualifications
        3. Company culture indicators
        4. Application strategy recommendations
        5. Keywords to emphasize in cover letter
        6. Salary range estimation (if not specified)
        7. Application deadline urgency level (1-10)
        8. Platform-specific application tips
        
        Format as JSON with clear sections.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            log_interaction("AutoApplyAgent", "analyze_job_posting", job_url, response)
            return self._parse_job_analysis(response)
        except Exception as e:
            logging.error(f"Error analyzing job posting: {e}")
            return self.get_fallback_response("job_analysis")
    
    def generate_tailored_cover_letter(self, job_analysis: Dict, resume_data: Dict, 
                                     company_research: Dict = None) -> str:
        """Generate a highly tailored cover letter for the specific job and company"""
        
        company_info = company_research or {}
        
        prompt = f"""
        Create a compelling, personalized cover letter based on:
        
        Job Analysis: {json.dumps(job_analysis, indent=2)}
        
        Resume Data: {json.dumps(resume_data, indent=2)}
        
        Company Research: {json.dumps(company_info, indent=2)}
        
        Requirements:
        1. Address specific job requirements mentioned
        2. Highlight relevant experience with quantified achievements
        3. Show knowledge of company/industry
        4. Use keywords from job description naturally
        5. Professional yet engaging tone
        6. 3-4 paragraphs, 250-300 words
        7. Strong opening and closing
        8. Avoid generic phrases
        
        Make it highly specific to this role and company.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            log_interaction("AutoApplyAgent", "generate_cover_letter", 
                          job_analysis.get("job_title", "Unknown"), response)
            return response.strip()
        except Exception as e:
            logging.error(f"Error generating cover letter: {e}")
            return self.get_fallback_response("cover_letter")
    
    def extract_application_form_fields(self, page_html: str, platform: str) -> Dict[str, Any]:
        """Extract and analyze form fields from job application page"""
        
        prompt = f"""
        Analyze this job application form HTML and extract all form fields:
        
        Platform: {platform}
        HTML Content: {page_html[:3000]}...
        
        Please identify:
        1. All input fields (name, type, required status)
        2. Select/dropdown options
        3. File upload fields
        4. Text areas
        5. Checkboxes and radio buttons
        6. Hidden fields
        7. Form submission URL and method
        8. Any special validation requirements
        
        Format as structured JSON with field metadata.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            return self._parse_form_analysis(response)
        except Exception as e:
            logging.error(f"Error extracting form fields: {e}")
            return {"error": str(e), "fields": []}
    
    def create_application_data(self, personal_info: Dict, resume_data: Dict, 
                              job_requirements: Dict, form_fields: List) -> Dict[str, Any]:
        """Create optimized application data matching form requirements"""
        
        # Base personal information
        application_data = {
            "personal": personal_info,
            "professional": resume_data,
            "job_specific": {}
        }
        
        # Map resume data to form fields intelligently
        field_mappings = {}
        for field in form_fields:
            field_name = field.get("name", "").lower()
            field_type = field.get("type", "text")
            
            # Smart field mapping based on field name and type
            mapped_value = self._map_field_value(field_name, field_type, 
                                               personal_info, resume_data)
            if mapped_value:
                field_mappings[field.get("name")] = mapped_value
        
        application_data["field_mappings"] = field_mappings
        
        # Generate responses for common application questions
        application_data["responses"] = self._generate_application_responses(
            job_requirements, resume_data
        )
        
        return application_data
    
    def _map_field_value(self, field_name: str, field_type: str, 
                        personal_info: Dict, resume_data: Dict) -> Optional[str]:
        """Intelligently map form field to appropriate data"""
        
        # Direct mappings
        if "email" in field_name:
            return personal_info.get("email")
        elif "phone" in field_name:
            return personal_info.get("phone")
        elif "name" in field_name:
            if "first" in field_name:
                return personal_info.get("first_name")
            elif "last" in field_name:
                return personal_info.get("last_name")
            else:
                return personal_info.get("full_name")
        elif "address" in field_name:
            return personal_info.get("address")
        elif "city" in field_name:
            return personal_info.get("city")
        elif "state" in field_name:
            return personal_info.get("state")
        elif "zip" in field_name:
            return personal_info.get("zip_code")
        elif "linkedin" in field_name:
            return personal_info.get("linkedin_url")
        elif "portfolio" in field_name or "website" in field_name:
            return personal_info.get("portfolio_url")
        
        # Experience-based mappings
        elif "experience" in field_name or "years" in field_name:
            return str(resume_data.get("total_experience_years", 0))
        elif "salary" in field_name:
            return personal_info.get("salary_expectation", "Negotiable")
        elif "availability" in field_name or "start" in field_name:
            return personal_info.get("availability", "Immediately")
        
        return None
    
    def _generate_application_responses(self, job_requirements: Dict, 
                                      resume_data: Dict) -> Dict[str, str]:
        """Generate responses to common application questions"""
        
        responses = {}
        
        # Why are you interested in this role?
        responses["interest_reason"] = f"""
        I am excited about this opportunity because it aligns perfectly with my {resume_data.get('total_experience_years', 'several')} years of experience in {', '.join(resume_data.get('top_skills', [])[:3])}. 
        The role's focus on {', '.join(job_requirements.get('key_requirements', [])[:2])} matches my proven track record in these areas.
        """
        
        # What makes you qualified?
        responses["qualification_summary"] = f"""
        My qualifications include {resume_data.get('education', {}).get('degree', 'relevant education')} and hands-on experience with {', '.join(resume_data.get('technical_skills', [])[:4])}. 
        I have successfully {resume_data.get('key_achievements', ['delivered impactful results'])[0] if resume_data.get('key_achievements') else 'contributed to organizational success'}.
        """
        
        # Work authorization
        responses["work_authorization"] = "Yes, I am authorized to work in this location."
        
        # Sponsorship
        responses["sponsorship_needed"] = "No sponsorship required."
        
        return responses
    
    def simulate_form_filling(self, application_data: Dict, form_fields: List, 
                            platform: str) -> Dict[str, Any]:
        """Simulate the form filling process and validate data"""
        
        filling_plan = {
            "platform": platform,
            "total_fields": len(form_fields),
            "filled_fields": 0,
            "validation_errors": [],
            "warnings": [],
            "completion_time_estimate": 0,
            "field_actions": []
        }
        
        field_mappings = application_data.get("field_mappings", {})
        
        for field in form_fields:
            field_name = field.get("name")
            field_type = field.get("type", "text")
            required = field.get("required", False)
            
            action = {
                "field_name": field_name,
                "field_type": field_type,
                "action": "fill",
                "value": None,
                "status": "pending"
            }
            
            # Check if we have data for this field
            if field_name in field_mappings:
                action["value"] = field_mappings[field_name]
                action["status"] = "ready"
                filling_plan["filled_fields"] += 1
            elif required:
                action["status"] = "missing_required"
                filling_plan["validation_errors"].append(
                    f"Required field '{field_name}' has no data"
                )
            else:
                action["status"] = "optional_skip"
                filling_plan["warnings"].append(
                    f"Optional field '{field_name}' will be skipped"
                )
            
            # Estimate time based on field type
            if field_type == "file":
                action["time_estimate"] = 10  # File upload takes longer
            elif field_type in ["select", "dropdown"]:
                action["time_estimate"] = 3
            else:
                action["time_estimate"] = 1
            
            filling_plan["completion_time_estimate"] += action["time_estimate"]
            filling_plan["field_actions"].append(action)
        
        # Calculate completion percentage
        filling_plan["completion_percentage"] = (
            filling_plan["filled_fields"] / filling_plan["total_fields"] * 100
            if filling_plan["total_fields"] > 0 else 0
        )
        
        return filling_plan
    
    def generate_application_strategy(self, job_analysis: Dict, competition_level: str,
                                    application_deadline: str = None) -> Dict[str, Any]:
        """Generate comprehensive application strategy"""
        
        strategy = {
            "priority_level": self._calculate_priority(job_analysis, competition_level),
            "application_timing": self._optimize_application_timing(application_deadline),
            "customization_level": "high",  # Always high for better results
            "follow_up_strategy": self._create_follow_up_plan(),
            "success_probability": self._estimate_success_probability(job_analysis),
            "recommendations": []
        }
        
        # Add specific recommendations
        if job_analysis.get("urgency_level", 5) > 7:
            strategy["recommendations"].append("Apply within 24 hours - high urgency")
        
        if competition_level == "high":
            strategy["recommendations"].append("Consider additional portfolio pieces")
            strategy["recommendations"].append("Research hiring manager on LinkedIn")
        
        strategy["recommendations"].append("Tailor resume keywords to job description")
        strategy["recommendations"].append("Prepare for potential screening questions")
        
        return strategy
    
    def _calculate_priority(self, job_analysis: Dict, competition_level: str) -> str:
        """Calculate application priority based on various factors"""
        score = 0
        
        # Job match score
        score += job_analysis.get("match_score", 50)
        
        # Competition level impact
        if competition_level == "low":
            score += 20
        elif competition_level == "medium":
            score += 10
        # high competition doesn't add points
        
        # Urgency level
        score += job_analysis.get("urgency_level", 5) * 2
        
        # Company rating impact
        score += job_analysis.get("company_rating", 3) * 5
        
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        else:
            return "low"
    
    def _optimize_application_timing(self, deadline: str = None) -> Dict[str, str]:
        """Optimize when to submit the application"""
        timing = {
            "recommended_day": "Tuesday or Wednesday",
            "recommended_time": "9-11 AM local time",
            "reasoning": "Higher HR activity and visibility"
        }
        
        if deadline:
            timing["deadline"] = deadline
            timing["latest_submit"] = "2 days before deadline"
            timing["reasoning"] += " | Submit well before deadline to avoid last-minute rush"
        
        return timing
    
    def _create_follow_up_plan(self) -> List[Dict[str, str]]:
        """Create a follow-up strategy plan"""
        return [
            {
                "timing": "1 week after application",
                "method": "LinkedIn connection with hiring manager",
                "message": "Brief, professional introduction"
            },
            {
                "timing": "2 weeks after application",
                "method": "Email follow-up",
                "message": "Polite inquiry about application status"
            },
            {
                "timing": "1 month after application",
                "method": "Final follow-up",
                "message": "Express continued interest, share recent achievements"
            }
        ]
    
    def _estimate_success_probability(self, job_analysis: Dict) -> Dict[str, Any]:
        """Estimate probability of application success"""
        base_probability = 15  # Average application response rate
        
        # Adjust based on match score
        match_score = job_analysis.get("match_score", 50)
        if match_score >= 80:
            base_probability += 25
        elif match_score >= 60:
            base_probability += 15
        elif match_score >= 40:
            base_probability += 5
        
        # Adjust based on experience level
        experience_match = job_analysis.get("experience_match", "medium")
        if experience_match == "perfect":
            base_probability += 20
        elif experience_match == "good":
            base_probability += 10
        
        return {
            "percentage": min(base_probability, 85),  # Cap at 85%
            "factors": [
                f"Job match score: {match_score}%",
                f"Experience alignment: {experience_match}",
                "Application customization: high"
            ]
        }
    
    def _parse_job_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI response for job analysis"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        # Fallback parsing
        return {
            "key_requirements": ["Requirements analysis in progress"],
            "nice_to_have": ["Additional qualifications being analyzed"],
            "company_culture": "Professional environment",
            "application_strategy": "Customize application to highlight relevant experience",
            "urgency_level": 5,
            "match_score": 60
        }
    
    def _parse_form_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI response for form analysis"""
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        
        return {
            "fields": [],
            "form_url": "",
            "method": "POST",
            "validation_requirements": []
        }
    
    def get_fallback_response(self, response_type: str) -> Any:
        """Provide fallback responses when AI is unavailable"""
        fallback_responses = {
            "job_analysis": {
                "key_requirements": ["Experience in relevant field", "Strong communication skills"],
                "application_strategy": "Highlight relevant experience and skills",
                "urgency_level": 5,
                "match_score": 60
            },
            "cover_letter": """Dear Hiring Manager,

I am writing to express my strong interest in this position. With my relevant experience and skills, I believe I would be a valuable addition to your team.

My background includes experience that directly relates to the requirements outlined in your job posting. I am particularly excited about the opportunity to contribute to your organization's continued success.

I would welcome the opportunity to discuss how my skills and experience can benefit your team. Thank you for your consideration.

Best regards,
[Your Name]""",
            "application_responses": {
                "interest_reason": "This role aligns with my career goals and experience",
                "qualification_summary": "I have relevant experience and skills for this position"
            }
        }
        
        return fallback_responses.get(response_type, "Fallback response not available")
    
    def get_platform_specific_tips(self, platform: str) -> List[str]:
        """Get platform-specific application tips"""
        tips_database = {
            "linkedin": [
                "Complete your LinkedIn profile before applying",
                "Connect with employees at the company",
                "Use LinkedIn's 'Easy Apply' feature for faster applications",
                "Follow the company page for updates",
                "Engage with company posts to show interest"
            ],
            "indeed": [
                "Upload a well-formatted PDF resume",
                "Complete your Indeed profile thoroughly",
                "Use Indeed's salary insights for negotiation",
                "Set up job alerts for similar positions",
                "Read company reviews before applying"
            ],
            "workday": [
                "Create a detailed Workday profile",
                "Save application progress frequently",
                "Prepare for lengthy application forms",
                "Upload all required documents in advance",
                "Double-check all information before submitting"
            ],
            "glassdoor": [
                "Research company reviews and ratings",
                "Check salary ranges for the position",
                "Look for interview experiences from other candidates",
                "Update your Glassdoor profile",
                "Consider company culture fit"
            ]
        }
        
        return tips_database.get(platform.lower(), [
            "Research the company thoroughly",
            "Tailor your application to the job description",
            "Follow up appropriately after applying",
            "Prepare for potential next steps"
        ])

    def run(self, job_data: Dict, personal_info: Dict, resume_data: Dict) -> Dict[str, Any]:
        """Main execution method for auto-apply functionality"""
        
        try:
            # Analyze the job posting
            job_analysis = self.analyze_job_posting(
                job_data.get("url", ""), 
                job_data.get("description", "")
            )
            
            # Generate tailored cover letter
            cover_letter = self.generate_tailored_cover_letter(
                job_analysis, resume_data, job_data.get("company_research", {})
            )
            
            # Create application strategy
            strategy = self.generate_application_strategy(
                job_analysis, 
                job_data.get("competition_level", "medium"),
                job_data.get("deadline")
            )
            
            # Get platform-specific tips
            platform = job_data.get("platform", "generic")
            tips = self.get_platform_specific_tips(platform)
            
            result = {
                "job_analysis": job_analysis,
                "cover_letter": cover_letter,
                "application_strategy": strategy,
                "platform_tips": tips,
                "success_probability": strategy["success_probability"],
                "next_steps": [
                    "Review and customize the generated cover letter",
                    "Prepare answers to common interview questions",
                    "Research the hiring manager on LinkedIn",
                    "Set up application tracking and follow-up reminders"
                ],
                "status": "ready_to_apply"
            }
            
            log_interaction("AutoApplyAgent", "run", 
                          job_data.get("title", "Unknown Job"), json.dumps(result, indent=2))
            
            return result
            
        except Exception as e:
            logging.error(f"Error in AutoApplyAgent.run: {e}")
            return {
                "error": str(e),
                "status": "error",
                "fallback_advice": [
                    "Review the job description manually",
                    "Create a custom cover letter",
                    "Apply directly on the company website",
                    "Follow up with a personalized message"
                ]
            }
