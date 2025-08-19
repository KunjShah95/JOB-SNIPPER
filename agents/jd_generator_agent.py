from agents.multi_ai_base import MultiAIAgent
from agents.message_protocol import AgentMessage
import logging


class JDGeneratorAgent(MultiAIAgent):
    def __init__(self):
        super().__init__(
            name="JDGeneratorAgent",
            use_gemini=True,
            use_mistral=True,
            return_mode="compare",  # Use compare to see both model outputs
        )

    def run(self, message_json):
        msg = AgentMessage.from_json(message_json)
        resume_text = msg.data

        if not resume_text or len(resume_text) < 10:
            logging.warning("Resume text is too short or empty")
            jd = self.get_fallback_response("")
            return AgentMessage(self.name, msg.sender, jd).to_json()

        prompt = f"""Generate a professional job description that would be ideal for this candidate's profile.

Resume Content:
{resume_text}

Include the following sections:
1. Job Title
2. Company Overview
3. Responsibilities
4. Requirements (Skills, Education, Experience)
5. Benefits & Perks

Make it compelling and tailored to match the candidate's experience level and skills."""

        try:
            jd = self.generate_ai_response(prompt)

            # If the response is empty or too short, use the fallback response
            if not jd or (isinstance(jd, str) and len(jd.strip()) < 100):
                logging.warning(
                    "AI response too short or empty, using fallback response"
                )
                jd = self.get_fallback_response("")

        except Exception as e:
            logging.error(f"Error generating job description: {e}")
            jd = self.get_fallback_response("")

        return AgentMessage(self.name, msg.sender, jd).to_json()

    def get_fallback_response(self, prompt):
        """Generate a comprehensive fallback job description"""
        return """
## 📃 AI-Generated Professional Job Description

### **Position:** Senior Data Scientist
### **Company:** InnovateTech Solutions
### **Location:** San Francisco, CA (Hybrid)
### **Employment Type:** Full-Time

---

## 🎯 **Job Summary**
We are seeking a highly skilled Senior Data Scientist to join our cutting-edge analytics team. This role offers the opportunity to work with large-scale datasets, develop machine learning models, and drive data-driven decision making across the organization. The ideal candidate will have strong technical expertise combined with business acumen to translate complex data insights into actionable strategies.

---

## 🔧 **Key Responsibilities**

**Data Analysis & Modeling:**
- Design and implement advanced machine learning algorithms and statistical models
- Analyze large, complex datasets to identify trends, patterns, and business opportunities
- Develop predictive models to support business forecasting and strategic planning
- Create automated data pipelines and ensure data quality and integrity

**Business Intelligence:**
- Collaborate with stakeholders to understand business requirements and translate them into analytical solutions
- Present findings and recommendations to executive leadership and cross-functional teams
- Develop dashboards and visualizations to communicate insights effectively
- Support A/B testing and experimentation frameworks

**Technical Leadership:**
- Mentor junior data scientists and provide technical guidance
- Establish best practices for data science workflows and methodologies
- Stay current with emerging technologies and industry trends
- Contribute to the development of the company's data science strategy

---

## 📋 **Required Qualifications**

**Education & Experience:**
- Master's or PhD in Data Science, Statistics, Computer Science, or related field
- 5+ years of experience in data science, machine learning, or analytics roles
- Proven track record of delivering successful data science projects

**Technical Skills:**
- **Programming:** Expert proficiency in Python and R; SQL for database querying
- **Machine Learning:** Experience with scikit-learn, TensorFlow, PyTorch, or similar frameworks
- **Data Tools:** Proficiency with Pandas, NumPy, Jupyter, and data visualization libraries
- **Cloud Platforms:** Experience with AWS, GCP, or Azure data services
- **Big Data:** Familiarity with Spark, Hadoop, or other distributed computing frameworks

**Soft Skills:**
- Excellent communication and presentation skills
- Strong problem-solving and analytical thinking abilities
- Ability to work collaboratively in cross-functional teams
- Business acumen and strategic thinking capabilities

---

## 🌟 **Preferred Qualifications**
- Experience in the technology or SaaS industry
- Knowledge of deep learning and neural networks
- Familiarity with MLOps and model deployment practices
- Experience with real-time data processing and streaming analytics
- Background in experimental design and causal inference

---

## 💼 **What We Offer**

**Compensation & Benefits:**
- Competitive salary range: $140,000 - $180,000 annually
- Performance-based bonuses and equity participation
- Comprehensive health, dental, and vision insurance
- 401(k) with company matching up to 6%

**Work-Life Balance:**
- Flexible hybrid work arrangement (3 days in office, 2 days remote)
- Unlimited PTO policy
- Paid parental leave (12 weeks)
- Mental health and wellness support programs

**Professional Development:**
- $3,000 annual learning and development budget
- Conference attendance and certification reimbursement
- Internal mentorship and career growth programs
- Access to cutting-edge tools and technologies

**Additional Perks:**
- Modern office space with collaborative work areas
- Daily catered meals and premium coffee
- Team building events and company retreats
- Commuter benefits and parking assistance

---

## 🚀 **About InnovateTech Solutions**
InnovateTech Solutions is a rapidly growing technology company focused on delivering innovative data-driven solutions to enterprise clients. We pride ourselves on fostering a collaborative, inclusive culture where every team member can thrive and make a meaningful impact.

**Ready to join our team?** Apply now and become part of our mission to transform how businesses leverage data for success!

---

*Note: This is a comprehensive fallback job description. Enable real AI by setting your API keys for personalized job descriptions based on specific resume profiles.*
        """
