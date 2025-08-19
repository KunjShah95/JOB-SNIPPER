from agents.multi_ai_base import MultiAIAgent
import logging


class InterviewPrepAgent(MultiAIAgent):
    """AI Agent for comprehensive interview preparation and coaching"""
    
    def __init__(self):
        super().__init__(
            name="InterviewPrepAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare"
        )

    def run(self, resume_data, job_data, prep_type="comprehensive"):
        """Generate interview preparation materials"""
        try:
            if prep_type == "comprehensive":
                return self._generate_comprehensive_prep(resume_data, job_data)
            elif prep_type == "technical":
                return self._generate_technical_prep(resume_data, job_data)
            elif prep_type == "behavioral":
                return self._generate_behavioral_prep(resume_data, job_data)
            elif prep_type == "company":
                return self._generate_company_prep(job_data)
            else:
                return self._generate_comprehensive_prep(resume_data, job_data)
                
        except Exception as e:
            logging.error(f"Error in interview preparation: {e}")
            return self._get_fallback_prep(job_data.get("title", ""), prep_type)

    def _generate_comprehensive_prep(self, resume_data, job_data):
        """Generate comprehensive interview preparation"""
        
        prompt = f"""
        Create a comprehensive interview preparation guide for this candidate:
        
        Job Title: {job_data.get('title', '')}
        Company: {job_data.get('company', '')}
        Job Description: {job_data.get('description', '')[:1000]}
        
        Candidate Background:
        - Skills: {', '.join(resume_data.get('skills', [])[:10])}
        - Experience: {resume_data.get('experience', '')}
        - Education: {resume_data.get('education', '')}
        
        Generate:
        1. 15 likely interview questions with detailed answers
        2. Technical questions specific to the role
        3. Behavioral questions with STAR method examples
        4. Questions to ask the interviewer
        5. Company research talking points
        6. Salary negotiation strategy
        7. Follow-up email template
        
        Format as structured content with clear sections.
        """
        
        try:
            response = self.generate_ai_response(prompt)
            return self._parse_prep_response(response, "comprehensive")
        except Exception:
            return self._get_fallback_prep(job_data.get("title", ""), "comprehensive")

    def _parse_prep_response(self, response, prep_type):
        """Parse AI response into structured format"""
        return {
            "prep_type": prep_type,
            "content": response,
            "questions": self._extract_questions(response),
            "tips": self._extract_tips(response),
            "resources": self._generate_resources(prep_type),
            "timeline": self._generate_prep_timeline(prep_type)
        }

    def _get_fallback_prep(self, job_title, prep_type):
        """Fallback interview preparation when AI is unavailable"""
        return {
            "prep_type": prep_type,
            "content": f"""
# 🎯 Interview Preparation for {job_title}

## 📝 Common Interview Questions
1. Tell me about yourself
2. Why are you interested in this position?
3. What are your greatest strengths?
4. What is your biggest weakness?
5. Where do you see yourself in 5 years?

## 🎯 STAR Method Framework
**Situation**: Set the context
**Task**: Describe your responsibility  
**Action**: Explain what you did
**Result**: Share the outcome

## 💡 Interview Tips
1. Research the company thoroughly
2. Prepare specific examples from your experience
3. Practice your answers out loud
4. Arrive 10-15 minutes early
5. Follow up with a thank-you email
            """,
            "questions": [
                "Tell me about yourself",
                "Why are you interested in this position?",
                "What are your greatest strengths?"
            ],
            "tips": [
                "Research the company thoroughly",
                "Prepare specific examples",
                "Practice your answers out loud"
            ],
            "resources": self._generate_resources(prep_type),
            "timeline": self._generate_prep_timeline(prep_type)
        }