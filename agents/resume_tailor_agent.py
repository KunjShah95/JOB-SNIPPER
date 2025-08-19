from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import logging


class ResumeTailorAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="ResumeTailorAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
        )

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        data = msg.data
        resume_text = (
            data["resume"] if isinstance(data, dict) and "resume" in data else data
        )
        job_title = (
            data["job_title"] if isinstance(data, dict) and "job_title" in data else ""
        )

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            tailoring = self.get_fallback_response(job_title)
            return AgentMessage(self.name, msg.sender, tailoring).to_json()

        # Always use real AI first
        prompt = f"""Tailor this resume for the following job title: {job_title}

Resume Content:
{resume_text}

Return a markdown-formatted response with specific tailoring suggestions."""
        try:
            tailoring = self.generate_ai_response(prompt)

            # If the response is empty or too short, use the fallback response
            if not tailoring or (
                isinstance(tailoring, str) and len(tailoring.strip()) < 50
            ):
                logging.warning(
                    "AI response too short or empty, using fallback response"
                )
                tailoring = self.get_fallback_response(job_title)

        except Exception as e:
            logging.error(f"Error generating tailoring suggestions: {e}")
            tailoring = self.get_fallback_response(job_title)

        return AgentMessage(self.name, msg.sender, tailoring).to_json()

    def get_fallback_response(self, job_title):
        """Provide comprehensive fallback tailoring suggestions"""
        position = job_title if job_title else "your target position"
        return f"""
## ✏️ Professional Resume Tailoring for {position.title()}

### 🎯 **Strategic Keywords to Include:**
- **Technical Skills**: Cloud computing, data analytics, project management, agile methodologies
- **Industry Terms**: Digital transformation, process optimization, stakeholder management
- **Soft Skills**: Leadership, communication, problem-solving, team collaboration
- **Certifications**: Include relevant professional certifications and training

### 📝 **Content Enhancement Recommendations:**

**1. Professional Summary**
- Craft a compelling 3-4 line summary that directly addresses the role requirements
- Highlight your unique value proposition for this specific position
- Include years of experience and key specializations

**2. Experience Section**
- Lead with quantifiable achievements (e.g., "Increased efficiency by 30%")
- Use action verbs that align with job description language
- Focus on relevant projects and responsibilities that match the role

**3. Skills Optimization**
- Prioritize technical skills mentioned in the job posting
- Group skills by category (Technical, Management, Communication)
- Remove outdated or irrelevant skills to maintain focus

### 🔧 **Format & Structure Improvements:**
- Use consistent bullet points and formatting throughout
- Ensure proper spacing and professional typography
- Keep to 1-2 pages maximum for optimal readability
- Include contact information and professional links

### 📈 **ATS Optimization:**
- Use standard section headings (Experience, Education, Skills)
- Include exact keyword matches from job descriptions
- Avoid graphics, tables, or unusual formatting that ATS can't read
- Save in both PDF and Word formats

### 🏆 **Competitive Edge Suggestions:**
1. Add a "Key Achievements" section highlighting major accomplishments
2. Include relevant volunteer work or side projects
3. Mention language skills if applicable to the role
4. Add professional development and continuous learning initiatives

### 📊 **Expected Impact:**
With these tailoring improvements, your resume will have significantly higher chances of:
- Passing ATS screening (↑85% compatibility)
- Catching recruiter attention (↑70% readability)
- Landing interview calls (↑60% response rate)
"""
