# JobSniper AI - UI Deployment Guide

## 🚀 Quick Start

### Option 1: Advanced UI (Recommended)
```bash
# Install dependencies
pip install -r requirements_ui.txt

# Launch advanced UI
streamlit run ui/advanced_app.py
```

### Option 2: Auto-Detection Launcher
```bash
# Launch main app (auto-detects available components)
streamlit run app.py
```

### Option 3: Legacy UI (Fallback)
```bash
# Launch legacy UI
streamlit run ui/app.py
```

## 🔧 System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 1GB free disk space
- Internet connection (for AI APIs)

### Recommended Requirements
- Python 3.10+
- 8GB RAM
- 2GB free disk space
- High-speed internet

## 📦 Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/KunjShah95/JOB-SNIPPER.git
cd JOB-SNIPPER
```

### 2. Switch to Advanced Branch
```bash
git checkout advanced-agents-rebuild
```

### 3. Install Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# UI-specific dependencies
pip install -r requirements_ui.txt

# Optional: Development dependencies
pip install -r requirements_dev.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

### 5. Launch Application
```bash
# Option A: Advanced UI
streamlit run ui/advanced_app.py

# Option B: Auto-launcher
streamlit run app.py

# Option C: Legacy UI
streamlit run ui/app.py
```

## 🌐 Deployment Options

### Local Development
```bash
streamlit run ui/advanced_app.py --server.port 8501
```

### Production Deployment

#### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy with one click

#### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements_ui.txt

EXPOSE 8501

CMD ["streamlit", "run", "ui/advanced_app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t jobsniper-ai .
docker run -p 8501:8501 jobsniper-ai
```

#### Heroku Deployment
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run ui/advanced_app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## ⚙️ Configuration

### Environment Variables
```bash
# .env file
GEMINI_API_KEY=your_gemini_key
MISTRAL_API_KEY=your_mistral_key
OPENAI_API_KEY=your_openai_key

# Email configuration (optional)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Database configuration
DATABASE_URL=sqlite:///jobsniper.db

# Feature flags
ENABLE_ADVANCED_AGENTS=true
ENABLE_WEB_SCRAPING=false
ENABLE_EMAIL_EXPORT=true
```

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
maxUploadSize = 200

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Install missing dependencies
pip install -r requirements_ui.txt

# Error: Advanced agents not found
# Solution: Switch to correct branch
git checkout advanced-agents-rebuild
```

#### 2. API Key Issues
```bash
# Error: API key not found
# Solution: Check .env file
cat .env | grep API_KEY

# Error: Invalid API key
# Solution: Verify keys in respective platforms
```

#### 3. Port Conflicts
```bash
# Error: Port 8501 already in use
# Solution: Use different port
streamlit run ui/advanced_app.py --server.port 8502
```

#### 4. Memory Issues
```bash
# Error: Out of memory
# Solution: Increase system memory or use lighter models
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=50
```

### Debug Mode
```bash
# Enable debug logging
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run ui/advanced_app.py
```

### Performance Optimization
```bash
# Enable caching
export STREAMLIT_CACHE_ENABLED=true

# Optimize for production
streamlit run ui/advanced_app.py --server.runOnSave false
```

## 📊 Monitoring and Analytics

### Health Check Endpoint
The application includes a built-in system status page accessible at:
- Advanced UI: `/⚙️ System Status`
- Legacy UI: Check sidebar for system information

### Performance Metrics
- Response time tracking
- Agent performance monitoring
- Error rate analysis
- User session analytics

### Logging
Logs are available in:
- Console output (development)
- `logs/` directory (production)
- Streamlit Cloud logs (cloud deployment)

## 🔒 Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly
- Monitor API usage

### Data Privacy
- Resume data is processed locally
- No data stored permanently without user consent
- GDPR compliance considerations
- Secure data transmission

### Access Control
- Consider implementing authentication for production
- Use HTTPS in production environments
- Implement rate limiting if needed

## 🚀 Advanced Features

### Custom Themes
Modify `.streamlit/config.toml` for custom branding:
```toml
[theme]
primaryColor = "#your_brand_color"
backgroundColor = "#your_bg_color"
```

### Custom Components
Add custom Streamlit components:
```python
# In ui/components/
import streamlit.components.v1 as components

def custom_component():
    components.html("""
    <div>Your custom HTML/JS here</div>
    """)
```

### Analytics Integration
```python
# Add Google Analytics
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

## 📱 Mobile Optimization

The UI is responsive and works on mobile devices. For optimal mobile experience:

1. Use the advanced UI (better mobile support)
2. Enable touch-friendly controls
3. Optimize image sizes
4. Test on various screen sizes

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull origin advanced-agents-rebuild

# Update dependencies
pip install -r requirements_ui.txt --upgrade

# Restart application
streamlit run ui/advanced_app.py
```

### Database Maintenance
```bash
# Backup database
cp jobsniper.db jobsniper_backup_$(date +%Y%m%d).db

# Clean old sessions
python -c "from utils.sqlite_logger import cleanup_old_sessions; cleanup_old_sessions()"
```

## 📞 Support

### Getting Help
1. Check this deployment guide
2. Review error logs
3. Check GitHub issues
4. Contact support team

### Reporting Issues
When reporting issues, include:
- Error messages
- System information
- Steps to reproduce
- Expected vs actual behavior

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Start advanced UI
streamlit run ui/advanced_app.py

# Start with custom port
streamlit run ui/advanced_app.py --server.port 8502

# Start in debug mode
STREAMLIT_LOGGER_LEVEL=debug streamlit run ui/advanced_app.py

# Check system status
python -c "from ui.advanced_app import run_system_test; print(run_system_test())"
```

### File Structure
```
JobSniper AI/
├── app.py                 # Main launcher
├── ui/
│   ├── advanced_app.py    # Advanced UI
│   └── app.py            # Legacy UI
├── agents/               # AI agents
├── utils/               # Utilities
├── requirements_ui.txt  # UI dependencies
└── .streamlit/         # Streamlit config
```

---

**🚀 Ready to launch your advanced career intelligence platform!**