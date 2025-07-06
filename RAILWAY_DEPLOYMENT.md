# 🚂 Railway Deployment Guide for BCS MCQ System

## ✅ Current Status
- ✅ Repository: https://github.com/iamsafridi/bcs-mcq-practice
- ✅ Deployed on Railway
- ⚠️ Gemini API needs environment variable setup

## 🔧 Fix Gemini API Issue

### Step 1: Add Environment Variable on Railway
1. **Go to Railway Dashboard**: https://railway.app/dashboard
2. **Click on your project** (`bcs-mcq-practice`)
3. **Go to "Variables" tab**
4. **Add new environment variable**:
   ```
   Key: GEMINI_API_KEY
   Value: [Your actual Gemini API key from Google AI Studio]
   ```
5. **Click "Add"**

### Step 2: Get Your Gemini API Key
If you don't have your API key:
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key
4. Add it to Railway Variables

### Step 3: Redeploy
- Railway will automatically redeploy when you add environment variables
- Or manually trigger redeploy from "Deployments" tab

## 🧪 Test Your Deployment

### Test 1: Check Environment Variables
Run this in Railway console or locally:
```bash
python test_railway_gemini.py
```

### Test 2: Test the Web App
1. Go to your Railway app URL
2. Upload a PDF/DOCX file or enter text
3. Try generating MCQs
4. Check if Gemini API is working

## 🔍 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Add the environment variable in Railway Variables tab

### Issue: "API key invalid"
**Solution**: 
1. Check your API key is correct
2. Ensure you have quota remaining
3. Verify the key is from Google AI Studio

### Issue: "Rate limit exceeded"
**Solution**: 
1. Check your Gemini API quota
2. Wait a few minutes and try again
3. Consider upgrading your plan

### Issue: App not loading
**Solution**:
1. Check Railway logs in "Deployments" tab
2. Ensure all dependencies are in requirements.txt
3. Verify the start command: `gunicorn app:app`

## 📱 Features Available on Railway
- ✅ File upload (PDF, DOCX, TXT)
- ✅ Direct text input
- ✅ AI-powered MCQ generation (after API key setup)
- ✅ Mobile responsive design
- ✅ Result sheet with explanations
- ✅ Download results feature

## 🌐 Your Railway App URL
Your app should be available at: `https://[your-app-name].railway.app`

## 📞 Support
- **Railway Logs**: Check "Deployments" tab for error logs
- **GitHub Issues**: https://github.com/iamsafridi/bcs-mcq-practice/issues
- **Local Testing**: Run `./start.sh` to test locally first

---
**🎯 After adding GEMINI_API_KEY, your BCS MCQ system will be fully functional on Railway!** 