# 🚀 BCS MCQ Practice System - Deployment Guide

## 📍 Repository
Your code is now live at: **https://github.com/iamsafridi/bcs-mcq-practice**

## 🌐 Free Hosting Options

### Option 1: Render (Recommended - Easiest)
1. **Go to**: https://render.com
2. **Sign up** with your GitHub account
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository**: `iamsafridi/bcs-mcq-practice`
5. **Configure**:
   - **Name**: `bcs-mcq-practice`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Add Environment Variable**:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key
7. **Click "Create Web Service"**
8. **Wait 2-3 minutes** for deployment
9. **Your app will be live at**: `https://bcs-mcq-practice.onrender.com`

### Option 2: Railway
1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select**: `iamsafridi/bcs-mcq-practice`
5. **Add Environment Variable**:
   - `GEMINI_API_KEY` = Your API key
6. **Deploy automatically**

### Option 3: Heroku
1. **Go to**: https://heroku.com
2. **Create account** and install Heroku CLI
3. **Run commands**:
   ```bash
   heroku create bcs-mcq-practice
   heroku config:set GEMINI_API_KEY=your_api_key_here
   git push heroku main
   ```

## 🔑 Setting Up Gemini API Key

### For Render:
1. Go to your Render dashboard
2. Click on your web service
3. Go to "Environment" tab
4. Add variable: `GEMINI_API_KEY` = `your_actual_api_key`

### For Railway:
1. Go to your Railway project
2. Click "Variables" tab
3. Add: `GEMINI_API_KEY` = `your_actual_api_key`

### For Heroku:
```bash
heroku config:set GEMINI_API_KEY=your_actual_api_key_here
```

## 📱 Features Available Online
- ✅ File upload (PDF, DOCX, TXT)
- ✅ Direct text input
- ✅ AI-powered MCQ generation
- ✅ Mobile responsive design
- ✅ Result sheet with explanations
- ✅ Download results feature

## 🔧 Troubleshooting

### If deployment fails:
1. Check if `GEMINI_API_KEY` is set correctly
2. Ensure all files are committed to GitHub
3. Check Render/Railway logs for errors

### If app doesn't work:
1. Verify API key is valid
2. Check if Gemini API has quota remaining
3. Test locally first: `./start.sh`

## 🌟 Next Steps
1. **Deploy to your chosen platform**
2. **Add your Gemini API key**
3. **Test the live app**
4. **Share with your wife for BCS practice!**

## 📞 Support
- **GitHub Issues**: https://github.com/iamsafridi/bcs-mcq-practice/issues
- **Local Testing**: Run `./start.sh` to test locally

---
**🎯 Your BCS MCQ Practice System is ready for deployment!** 