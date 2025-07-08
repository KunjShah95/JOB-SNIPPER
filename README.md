# 🎯 JobSniper AI

**AI-Powered Resume Analysis & Job Matching Platform**

A modern, clean, and deployable job matching application that analyzes resumes and finds the best job matches using AI.

## ✨ Features

- 📄 **Resume Analysis**: Upload and analyze resumes (PDF, DOCX, TXT)
- 🎯 **Job Matching**: AI-powered job recommendations based on skills
- 📊 **Analytics Dashboard**: Track your job search progress
- 🎨 **Modern UI**: Clean, responsive Streamlit interface
- 🚀 **Easy Deployment**: Ready for Streamlit Cloud, Heroku, or Docker

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/KunjShah95/JOB-SNIPPER.git
cd JOB-SNIPPER
git checkout complete-revamp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

### 4. Open in browser
Navigate to `http://localhost:8501` to use the application.

## 🎮 Demo Mode

The application runs in demo mode by default with:
- Mock resume analysis
- Sample job matches
- No external API dependencies

## 🔧 Configuration (Optional)

For enhanced AI features, create a `.env` file:

```env
# Optional: Add AI API keys for enhanced functionality
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 📱 Deployment

### Streamlit Cloud
1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy the `complete-revamp` branch
4. Set `app.py` as the main file

### Docker
```bash
# Build image
docker build -t jobsniper-ai .

# Run container
docker run -p 8501:8501 jobsniper-ai
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: Google Gemini / OpenAI (optional)
- **File Processing**: PyPDF2, python-docx
- **Data**: Pandas, NumPy

## 📊 Features Overview

### Resume Analysis
- Extract skills and experience
- Calculate match scores
- Provide improvement recommendations

### Job Matching
- AI-powered job recommendations
- Skill-based matching algorithm
- Filter by location, salary, and match score

### Analytics
- Track analysis history
- Skill frequency analysis
- Progress visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- 📧 Email: [your-email@example.com](mailto:your-email@example.com)
- 🐛 Issues: [GitHub Issues](https://github.com/KunjShah95/JOB-SNIPPER/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/KunjShah95/JOB-SNIPPER/discussions)

---

**Built with ❤️ by [Kunj Shah](https://github.com/KunjShah95)**
  streamlit run ui/app.py
  ```
- **Demo Mode:**
  - Works without API keys using realistic mock data.
- **Production:**
  - Add your API keys and email credentials to `.env` for full functionality.

---

## 📁 Project Structure
```
job-snipper-ai/
├── agents/                 # AI agents
│   ├── controller_agent.py
│   ├── auto_apply_agent.py
│   ├── recruiter_view_agent.py
│   ├── skill_recommendation_agent.py
│   └── agent_fallback.py
├── ui/
│   └── app.py             # Streamlit interface
├── utils/
│   ├── config.py
│   ├── pdf_reader.py
│   ├── sqlite_logger.py
│   └── exporter.py
├── requirements.txt
├── .env                   # API keys (create this)
└── ARCHITECTURE.md        # System architecture diagram
```

---

## 🔧 Configuration & Extensibility
- **AI Provider Priority:**
  1. Google Gemini (if valid key provided)
  2. Mistral AI (if Gemini unavailable)
  3. Demo Mode (if no valid keys)
- **Modular agent design:** Easily add new AI providers or business logic.
- **Docker-ready** for production deployment.

---

## 🛡️ Security & Privacy
- API keys and credentials are loaded from `.env` (never hardcoded).
- No resumes or user data are stored unless explicitly exported by the user.
- All processing is local or via secure API calls.

---

## 🧪 Testing & Troubleshooting
- **Demo Mode:** All features work with realistic mock data for development/testing.
- **Test script:**
  ```bash
  python test_ui_data.py
  ```
- **Troubleshooting:**
  - Check console output for error messages
  - Verify API keys and email credentials
  - Use demo mode for testing without API costs

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License
This project is licensed under the MIT License.

---

## ❤️ Made for better hiring and career journeys
