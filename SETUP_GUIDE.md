# 🚀 Job Snipper AI - Complete Setup Guide

This guide will help you set up and run the enhanced Job Snipper AI platform for resume analysis, job matching, and career development.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended for AI models)
- **Storage**: 2GB free space
- **Internet**: Required for AI model downloads and job scraping

### Required Software
- Python 3.8+
- pip (Python package manager)
- Git (for cloning repository)

## 🔧 Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/KunjShah95/JOB-SNIPPER.git
cd JOB-SNIPPER
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv job_snipper_env

# Activate virtual environment
# On Windows:
job_snipper_env\Scripts\activate
# On macOS/Linux:
source job_snipper_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# If you encounter issues, try:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Step 4: Download AI Models (Optional but Recommended)
```bash
# Download spaCy English model for enhanced NLP
python -m spacy download en_core_web_sm

# If the above fails, try:
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz
```

### Step 5: Set Up Environment Variables (Optional)
```bash
# Create .env file for API keys
touch .env

# Add your API keys (optional for enhanced features)
echo "OPENAI_API_KEY=your_openai_key_here" >> .env
echo "SCRAPING_DELAY=2" >> .env
```

### Step 6: Test Installation
```bash
# Test basic functionality
python -c "import streamlit; print('Streamlit installed successfully')"
python -c "import pandas; print('Pandas installed successfully')"
python -c "import PyPDF2; print('PDF processing ready')"
```

## 🚀 Running the Application

### Option 1: Enhanced Version (Recommended)
```bash
streamlit run app_enhanced.py
```

### Option 2: Basic Version
```bash
streamlit run app.py
```

### Access the Application
- Open your browser and go to: `http://localhost:8501`
- The application should load with the Job Snipper AI interface

## 🎯 First-Time Usage Guide

### 1. Resume Analysis
1. **Navigate to Resume Analysis**
   - Click on "📄 Resume Analysis" in the sidebar

2. **Upload Your Resume**
   - Click "Choose your resume file"
   - Select a PDF, DOC, DOCX, or TXT file
   - Maximum file size: 10MB

3. **Wait for Analysis**
   - File validation (security check)
   - Text extraction
   - AI analysis and scoring

4. **Review Results**
   - Overall score and confidence
   - Extracted skills by category
   - Structure analysis
   - Personalized recommendations

### 2. Job Matching
1. **Complete Resume Analysis First**
   - Your resume data is needed for matching

2. **Enter Job Description**
   - Paste a complete job description
   - Include requirements and responsibilities

3. **Get Compatibility Score**
   - AI-powered matching analysis
   - Skill gap identification
   - Application recommendations

### 3. Job Search (New Feature)
1. **Set Search Parameters**
   - Enter job title/keywords
   - Specify location (optional)
   - Choose number of results

2. **Review Matched Jobs**
   - Compatibility scores
   - Missing skills analysis
   - Application recommendations

### 4. Interview Preparation (New Feature)
1. **Generate Questions**
   - Based on your skills and experience level
   - Mix of technical and behavioral questions

2. **Practice Session**
   - Answer questions one by one
   - Get real-time feedback
   - Receive performance scoring

### 5. Resume Builder
1. **Fill Information**
   - Personal details
   - Work experience
   - Education and skills

2. **Generate ATS Resume**
   - Choose from multiple templates
   - Download as PDF

## 🛠️ Troubleshooting

### Common Installation Issues

#### Issue 1: Python Version Error
```bash
# Check Python version
python --version

# If version is < 3.8, install newer Python
# Visit: https://www.python.org/downloads/
```

#### Issue 2: pip Installation Fails
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try installing with verbose output
pip install -r requirements.txt -v
```

#### Issue 3: spaCy Model Download Fails
```bash
# Alternative installation methods
pip install spacy[lookups]
python -m spacy download en_core_web_sm

# Manual download if needed
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz
```

#### Issue 4: Memory Issues
```bash
# For systems with limited RAM, install lighter versions
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers[torch]
```

### Runtime Issues

#### Issue 1: File Upload Fails
- **Check file size**: Maximum 10MB
- **Verify format**: PDF, DOC, DOCX, TXT only
- **File corruption**: Try a different file

#### Issue 2: AI Analysis Fails
- **Check internet connection**: Required for some models
- **Verify dependencies**: Ensure all packages installed
- **Check logs**: Look for specific error messages

#### Issue 3: Job Search Not Working
- **Internet connection**: Required for job scraping
- **Rate limiting**: Wait between searches
- **Platform availability**: Some job sites may block requests

## ⚙️ Configuration Options

### Environment Variables
Create a `.env` file in the project root:

```bash
# OpenAI API Key (optional, for enhanced AI features)
OPENAI_API_KEY=your_openai_key_here

# Job scraping settings
SCRAPING_DELAY=2
MAX_JOBS_PER_SEARCH=50

# Analytics settings
ANALYTICS_PATH=analytics_data.json
CLEANUP_DAYS=90

# Security settings
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf,doc,docx,txt
```

### Customization Options

#### 1. Skill Database
Edit `core/enhanced_ai_engine.py` to add custom skills:
```python
'custom_category': [
    'your_skill_1', 'your_skill_2', 'your_skill_3'
]
```

#### 2. Interview Questions
Add questions in `features/interview_prep.py`:
```python
{
    'question': 'Your custom question?',
    'difficulty': 'medium',
    'expected_points': ['Point 1', 'Point 2'],
    'follow_ups': ['Follow-up question?'],
    'skills': ['relevant_skill']
}
```

#### 3. Resume Templates
Customize templates in `core/resume_builder.py`

## 📊 Performance Optimization

### For Better Performance
1. **Use SSD storage** for faster file processing
2. **Increase RAM** for better AI model performance
3. **Stable internet** for job scraping and AI features
4. **Close other applications** when running analysis

### For Better Results
1. **Well-formatted resumes** with clear sections
2. **Complete job descriptions** for accurate matching
3. **Relevant skills** in your resume
4. **Regular practice** with interview preparation

## 🔒 Security Considerations

### File Security
- All uploaded files are validated
- Temporary files are automatically cleaned
- No files are permanently stored
- MIME type verification prevents malicious uploads

### Data Privacy
- No personal data is sent to external services (unless using OpenAI)
- Analytics data is stored locally
- Session data is cleared on browser close

### API Key Security
- Store API keys in `.env` file
- Never commit API keys to version control
- Use environment variables in production

## 📈 Advanced Features

### Using OpenAI Integration
1. **Get API Key**: Visit https://platform.openai.com/
2. **Add to Environment**: Set `OPENAI_API_KEY` in `.env`
3. **Enhanced Analysis**: Better recommendations and insights

### Custom Job Sources
1. **Add new platforms** in `features/job_scraper.py`
2. **Implement scraping logic** following existing patterns
3. **Test thoroughly** to avoid blocking

### Analytics Export
1. **Navigate to Settings**
2. **Click Export Analytics Data**
3. **Download JSON/CSV** for external analysis

## 🆘 Getting Help

### Documentation
- **README.md**: Overview and basic setup
- **SETUP_GUIDE.md**: This detailed guide
- **Code comments**: Inline documentation

### Support Channels
1. **GitHub Issues**: Report bugs and request features
2. **Discussions**: Ask questions and share ideas
3. **Wiki**: Additional documentation and examples

### Common Questions

**Q: Can I use this without internet?**
A: Basic functionality works offline, but AI features and job search require internet.

**Q: Is my resume data secure?**
A: Yes, all processing is local. No data is stored permanently unless you choose to export analytics.

**Q: Can I add custom skills?**
A: Yes, modify the skill database in the AI engine configuration.

**Q: How accurate is the job matching?**
A: Accuracy depends on resume quality and job description completeness. AI models provide good baseline matching.

---

## 🎉 You're Ready!

Your Job Snipper AI platform is now set up and ready to use. Start by uploading a resume and exploring the various features. Remember to check the analytics dashboard to track your progress over time.

**Happy job hunting! 🚀**