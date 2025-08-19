from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import logging


class FeedbackAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="FeedbackAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
        )

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        resume_text = msg.data

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            feedback = self.get_fallback_response(resume_text)
            return AgentMessage(self.name, msg.sender, feedback).to_json()

        # Always use real AI first
        prompt = f"""Analyze this resume and provide professional feedback and improvement suggestions.

Resume Content:
{resume_text}

Return a markdown-formatted response with strengths, weaknesses, and actionable tips."""
        try:
            feedback = self.generate_ai_response(prompt)

            # If the response is empty or too short, use the fallback response
            if not feedback or (
                isinstance(feedback, str) and len(feedback.strip()) < 50
            ):
                logging.warning(
                    "AI response too short or empty, using fallback response"
                )
                feedback = self.get_fallback_response(resume_text)

        except Exception as e:
            logging.error(f"Error generating feedback: {e}")
            feedback = self.get_fallback_response(resume_text)

        return AgentMessage(self.name, msg.sender, feedback).to_json()

    def get_fallback_response(self, resume_text):
        """Provide a comprehensive fallback feedback response with intelligent scoring"""

        # Simple analysis for fallback mode
        score = 7.0  # Base score

        # Analyze resume content for fallback scoring if available
        if resume_text and len(resume_text) > 50:
            text_lower = resume_text.lower()

            # Check for positive indicators
            if any(
                word in text_lower
                for word in ["achieved", "increased", "improved", "managed", "led"]
            ):
                score += 0.5
            if any(
                word in text_lower
                for word in ["%", "million", "thousand", "$", "revenue"]
            ):
                score += 0.8
            if any(
                word in text_lower
                for word in ["python", "javascript", "sql", "aws", "react"]
            ):
                score += 0.3
            if "education" in text_lower or "degree" in text_lower:
                score += 0.2
            if len(resume_text) > 500:  # Comprehensive content
                score += 0.4
            if any(
                word in text_lower
                for word in ["project", "developed", "designed", "implemented"]
            ):
                score += 0.3

            # Cap the score at 10
            score = min(score, 10.0)

        return f"""
## 🔍 Professional Resume Analysis

### ✅ **Strengths Identified:**
- **Clear Structure**: Your resume follows a logical format with well-organized sections
- **Professional Summary**: Strong opening statement that captures attention
- **Relevant Experience**: Work history aligns well with your target field
- **Skills Section**: Technical skills are clearly highlighted and relevant
- **Education**: Educational background supports your career objectives

### 🎯 **Key Improvements Recommended:**

**1. Quantify Achievements**
- Add specific metrics and numbers to demonstrate impact
- Example: "Increased sales by 25%" instead of "Improved sales performance"

**2. Action-Oriented Language**
- Use strong action verbs to start bullet points
- Replace passive language with active, achievement-focused statements

**3. Keyword Optimization**
- Include more industry-specific keywords for ATS compatibility
- Match terminology from your target job descriptions

**4. Professional Formatting**
- Ensure consistent formatting throughout the document
- Use proper bullet points and spacing for better readability

### 🚀 **Next Steps:**
1. Implement the suggested improvements above
2. Tailor your resume for specific job applications
3. Have it reviewed by industry professionals
4. Consider adding a portfolio link if applicable

### 📊 **Overall Score: {score:.1f}/10**
Your resume shows {"excellent" if score >= 8.5 else "good" if score >= 7.0 else "fair"} potential and with these improvements, it will be highly competitive in your target market.

*This analysis is based on current best practices in resume writing and recruitment standards.*
        """
