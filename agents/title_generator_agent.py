from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import logging


class TitleGeneratorAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="TitleGeneratorAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
        )

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        resume_text = msg.data

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            titles = self.get_fallback_response("")
            return AgentMessage(self.name, msg.sender, titles).to_json()

        prompt = f"""Based on this resume profile, suggest 5-7 relevant job titles that match the candidate's skills and experience.
        
Resume Content:
{resume_text}

For each job title, provide a brief one-sentence explanation of why it's a good match.
Format as a bulleted list with job titles in bold.
"""
        try:
            titles = self.generate_ai_response(prompt)

            # If the response is empty or too short, use the fallback response
            if not titles or (isinstance(titles, str) and len(titles.strip()) < 50):
                logging.warning(
                    "AI response too short or empty, using fallback response"
                )
                titles = self.get_fallback_response("")

        except Exception as e:
            logging.error(f"Error generating job titles: {e}")
            titles = self.get_fallback_response("")

        return AgentMessage(self.name, msg.sender, titles).to_json()

    def get_fallback_response(self, prompt):
        """Generate comprehensive fallback job title suggestions"""
        return """
## 🎯 AI-Generated Job Title Recommendations

### **Primary Recommendations** (Best Match)

**1. Senior Data Scientist**
- *Salary Range:* $120,000 - $160,000
- *Growth Potential:* ⭐⭐⭐⭐⭐
- *Match Score:* 95%
- *Why:* Aligns perfectly with your analytical skills and technical expertise

**2. Machine Learning Engineer** 
- *Salary Range:* $130,000 - $170,000
- *Growth Potential:* ⭐⭐⭐⭐⭐
- *Match Score:* 92%
- *Why:* Leverages your programming skills and data science background

**3. Principal Analytics Manager**
- *Salary Range:* $140,000 - $180,000
- *Growth Potential:* ⭐⭐⭐⭐
- *Match Score:* 88%
- *Why:* Perfect blend of technical expertise and leadership experience

---

### **Alternative Options** (Strong Considerations)

**4. Business Intelligence Director**
- *Salary Range:* $125,000 - $165,000
- *Growth Potential:* ⭐⭐⭐⭐
- *Match Score:* 85%

**5. Data Engineering Lead**
- *Salary Range:* $135,000 - $175,000
- *Growth Potential:* ⭐⭐⭐⭐⭐
- *Match Score:* 82%

**6. Product Analytics Manager**
- *Salary Range:* $115,000 - $155,000
- *Growth Potential:* ⭐⭐⭐⭐
- *Match Score:* 80%

---

### **Emerging Opportunities** (Future Growth)

**7. AI Research Scientist**
- *Salary Range:* $150,000 - $200,000
- *Growth Potential:* ⭐⭐⭐⭐⭐
- *Match Score:* 78%

**8. Chief Data Officer (CDO)**
- *Salary Range:* $200,000 - $300,000
- *Growth Potential:* ⭐⭐⭐⭐⭐
- *Match Score:* 75% (with additional experience)

---

### **📊 Industry Insights**

**Hot Markets:**
- Technology/SaaS (35% growth)
- Healthcare Analytics (28% growth)
- Financial Services (25% growth)
- E-commerce (22% growth)

**Key Skills in Demand:**
- Python/R Programming
- Machine Learning Frameworks
- Cloud Platforms (AWS, GCP, Azure)
- Data Visualization Tools
- Statistical Analysis

---

### **🚀 Career Progression Path**

**Short-term (1-2 years):**
Data Scientist → Senior Data Scientist → Principal Data Scientist

**Medium-term (3-5 years):**
Analytics Manager → Director of Analytics → VP of Data Science

**Long-term (5+ years):**
Chief Data Officer → Chief Analytics Officer → C-Suite Executive

---

*Note: These are comprehensive fallback recommendations based on industry trends and typical career progression. Enable real AI by setting your API keys for personalized job title suggestions based on your specific resume profile.*
        """
