# 🚀 JobSniper AI - Deployment Guide

This guide covers all deployment options for JobSniper AI.

## 🎯 Quick Deploy Options

### 1. Streamlit Cloud (Recommended)
**Easiest deployment option - Free and fast!**

1. Fork this repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Select your forked repository
5. Set branch to `complete-revamp`
6. Set main file to `app.py`
7. Click "Deploy"

**Your app will be live at:** `https://your-app-name.streamlit.app`

### 2. Local Development
```bash
# Clone and setup
git clone https://github.com/KunjShah95/JOB-SNIPPER.git
cd JOB-SNIPPER
git checkout complete-revamp

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 3. Docker Deployment
```bash
# Build the image
docker build -t jobsniper-ai .

# Run the container
docker run -p 8501:8501 jobsniper-ai

# Access at http://localhost:8501
```

### 4. Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku complete-revamp:main

# Open app
heroku open
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for enhanced features:

```env
# Optional: AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
```

### Platform-Specific Setup

#### Streamlit Cloud
- No additional setup required
- Add secrets in the Streamlit Cloud dashboard if using API keys
- Automatic SSL and custom domain support

#### Docker
- Exposed on port 8501
- Health check included
- Volume mounting for persistent data:
  ```bash
  docker run -p 8501:8501 -v $(pwd)/data:/app/data jobsniper-ai
  ```

#### Heroku
- Add `Procfile`:
  ```
  web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  ```
- Set config vars in Heroku dashboard for API keys

## 🌐 Production Considerations

### Performance
- The app is optimized for fast loading
- Demo mode requires no external API calls
- Caching implemented for better performance

### Security
- No sensitive data stored by default
- API keys handled securely through environment variables
- Input validation for file uploads

### Monitoring
- Built-in health checks
- Error logging and handling
- Usage analytics in the dashboard

## 🔍 Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Port Already in Use:**
```bash
streamlit run app.py --server.port 8502
```

**Docker Build Fails:**
```bash
docker system prune
docker build --no-cache -t jobsniper-ai .
```

### Logs and Debugging

**Streamlit Logs:**
```bash
streamlit run app.py --logger.level debug
```

**Docker Logs:**
```bash
docker logs container-name
```

## 📊 Scaling

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use container orchestration (Kubernetes, Docker Swarm)

### Vertical Scaling
- Increase memory allocation for large file processing
- Use faster storage for better performance

## 🔄 Updates and Maintenance

### Updating the Application
```bash
git pull origin complete-revamp
pip install -r requirements.txt
streamlit run app.py
```

### Database Backup
The app uses session state by default. For persistent data:
- Implement database integration
- Use cloud storage for file uploads
- Regular backup procedures

## 🆘 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/KunjShah95/JOB-SNIPPER/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/KunjShah95/JOB-SNIPPER/discussions)
- 📖 **Documentation**: [README.md](README.md)

## ✅ Deployment Checklist

- [ ] Repository forked/cloned
- [ ] Dependencies installed
- [ ] App runs locally
- [ ] Tests pass (`python test_app.py`)
- [ ] Environment variables configured (if needed)
- [ ] Deployment platform chosen
- [ ] App deployed and accessible
- [ ] Basic functionality tested

**🎉 Congratulations! Your JobSniper AI is now live!**