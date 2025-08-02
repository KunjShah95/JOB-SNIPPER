# 🎯 Job Snipper AI - Enhanced Resume Analysis Platform

A comprehensive AI-powered resume analysis, job matching, and career development platform with advanced features including job scraping, interview preparation, and intelligent recommendations.

## ✨ Enhanced Features

### 🔒 Security & File Processing
- **Advanced File Validation**: Multi-layer security checks for uploaded files
- **MIME Type Verification**: Prevents malicious file uploads
- **Content Scanning**: Intelligent malware pattern detection
- **Secure Processing**: Temporary file management with automatic cleanup
- **Format Support**: PDF, DOC, DOCX, TXT with robust text extraction

### 🤖 AI-Powered Analysis
- **Enhanced AI Engine**: Advanced NLP with fallback mechanisms
- **Smart Skill Extraction**: Multi-method skill identification using spaCy, Transformers
- **Structure Analysis**: Comprehensive resume formatting and completeness scoring
- **Job Compatibility**: AI-powered matching with semantic similarity
- **Personalized Recommendations**: Context-aware improvement suggestions

### 🔍 Job Search & Matching
- **Multi-Platform Scraping**: Search jobs across Indeed, LinkedIn, Glassdoor, Stack Overflow
- **Intelligent Matching**: AI-powered job-resume compatibility scoring
- **Skill Gap Analysis**: Identify missing skills for target positions
- **Application Recommendations**: Smart guidance on job applications

### 🎤 Interview Preparation
- **AI-Generated Questions**: Personalized interview questions based on skills
- **Real-Time Feedback**: Intelligent answer evaluation and scoring
- **STAR Method Guidance**: Behavioral question preparation
- **Performance Tracking**: Interview practice session analytics

### 🏗️ ATS Resume Builder
- **Multiple Templates**: Modern, Classic, Tech-Focused, Creative designs
- **ATS Optimization**: Keyword optimization and formatting guidelines
- **Real-Time Preview**: Live resume preview with completeness scoring
- **PDF Generation**: Professional resume export with custom templates

### 📊 Advanced Analytics
- **Performance Metrics**: Detailed analysis tracking and insights
- **Skill Trends**: Popular skills and market demand analysis
- **Progress Tracking**: Historical performance and improvement metrics
- **Export Capabilities**: JSON/CSV data export for external analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Internet connection for AI models

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KunjShah95/JOB-SNIPPER.git
   cd JOB-SNIPPER
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download AI models (optional but recommended)**
   ```bash
   # For enhanced NLP capabilities
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create .env file for API keys
   echo "OPENAI_API_KEY=your_openai_key_here" > .env
   ```

5. **Run the enhanced application**
   ```bash
   streamlit run app_enhanced.py
   ```

## 📖 How to Use

### 1. Resume Analysis
1. Navigate to **📄 Resume Analysis**
2. Upload your resume (PDF, DOC, DOCX, TXT)
3. Wait for AI analysis to complete
4. Review detailed results including:
   - Overall score and confidence
   - Extracted skills by category
   - Structure analysis
   - Personalized recommendations

### 2. Job Matching
1. Complete resume analysis first
2. Go to **🎯 Job Matching**
3. Paste a job description
4. Get compatibility score and skill gap analysis
5. Review improvement recommendations

### 3. Job Search
1. Navigate to **🔍 Job Search**
2. Enter job title/keywords and location
3. Set number of jobs to search
4. Review matched jobs with compatibility scores
5. Get application recommendations

### 4. Interview Preparation
1. Go to **🎤 Interview Prep**
2. Generate personalized questions based on your skills
3. Practice answering questions
4. Receive real-time feedback and scoring
5. Review detailed performance analysis

### 5. Resume Building
1. Navigate to **🏗️ ATS Resume Builder**
2. Fill in personal information, experience, education
3. Add skills by category
4. Include projects and achievements
5. Generate ATS-optimized PDF resume

## 🛠️ Technical Architecture

### Core Components
- **Enhanced AI Engine**: Multi-model approach with fallbacks
- **File Processor**: Secure file handling and text extraction
- **Job Scraper**: Multi-platform job search capabilities
- **Interview Prep**: AI-powered question generation and evaluation
- **Analytics Tracker**: Comprehensive usage and performance analytics

### AI Models Used
- **spaCy**: Named Entity Recognition and text processing
- **Transformers**: Advanced skill extraction and classification
- **Sentence Transformers**: Semantic similarity for job matching
- **OpenAI GPT**: Enhanced analysis and recommendations (optional)

### Security Features
- Input validation and sanitization
- File type and size restrictions
- Malware pattern detection
- Secure temporary file handling
- Error handling and logging

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| Resume Analysis | AI-powered resume scoring and analysis | ✅ Enhanced |
| Job Matching | Compatibility scoring with job descriptions | ✅ Enhanced |
| Job Search | Multi-platform job scraping and matching | ✅ New |
| Interview Prep | AI-generated questions and feedback | ✅ New |
| Resume Builder | ATS-optimized resume creation | ✅ Enhanced |
| Analytics | Comprehensive usage and performance tracking | ✅ Enhanced |
| Security | Multi-layer file validation and processing | ✅ Enhanced |

## 🔧 Configuration

### Environment Variables
```bash
# Optional: For enhanced AI capabilities
OPENAI_API_KEY=your_openai_api_key

# Optional: For job scraping rate limiting
SCRAPING_DELAY=2

# Optional: For analytics storage
ANALYTICS_PATH=analytics_data.json
```

### Customization
- Modify skill databases in `core/enhanced_ai_engine.py`
- Add new job platforms in `features/job_scraper.py`
- Customize interview questions in `features/interview_prep.py`
- Adjust resume templates in `core/resume_builder.py`

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

2. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **File Upload Issues**
   - Check file size (max 10MB)
   - Ensure supported format (PDF, DOC, DOCX, TXT)
   - Verify file is not corrupted

4. **AI Analysis Fails**
   - Check internet connection
   - Verify API keys if using OpenAI
   - Review logs for specific errors

## 📈 Performance Tips

1. **For Better Analysis**:
   - Use well-formatted resumes
   - Include clear section headers
   - Add quantified achievements
   - Use standard fonts and formatting

2. **For Job Matching**:
   - Analyze resume first for better results
   - Use complete job descriptions
   - Include all relevant skills in resume

3. **For Interview Prep**:
   - Complete resume analysis for personalized questions
   - Set appropriate experience level
   - Practice regularly for improvement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **spaCy** for NLP capabilities
- **Transformers** for advanced AI models
- **Streamlit** for the web interface
- **OpenAI** for enhanced AI features
- **Community** for feedback and contributions

---

## 🎯 Getting Started with Resume Analysis

### Step-by-Step Guide:

1. **Launch the Application**
   ```bash
   streamlit run app_enhanced.py
   ```

2. **Upload Your Resume**
   - Click on "📄 Resume Analysis"
   - Upload your resume file
   - Wait for processing

3. **Review Results**
   - Check your overall score
   - Review extracted skills
   - Read personalized recommendations

4. **Explore Additional Features**
   - Try job matching with real job descriptions
   - Practice interview questions
   - Build an ATS-optimized resume

**Built with ❤️ for better career outcomes**

---

*For support, please open an issue on GitHub or contact the development team.*