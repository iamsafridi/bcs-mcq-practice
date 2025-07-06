#!/bin/bash

echo "🚀 BCS MCQ Practice System - Deployment Helper"
echo "================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."

required_files=("app.py" "requirements.txt" "Procfile" "runtime.txt" "render.yaml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

echo "✅ All required files found!"

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY environment variable not set"
    echo "   You'll need to set this in your hosting platform's dashboard"
fi

echo ""
echo "🎯 Deployment Options:"
echo "======================"
echo "1. Render (Recommended - Free)"
echo "   - Go to: https://render.com"
echo "   - Sign up and connect GitHub"
echo "   - Create new Web Service"
echo "   - Select this repository"
echo "   - Set environment variable: GEMINI_API_KEY"
echo ""
echo "2. Railway (Alternative)"
echo "   - Go to: https://railway.app"
echo "   - Sign up and connect GitHub"
echo "   - Create new project"
echo "   - Deploy from GitHub"
echo ""
echo "3. Heroku (Alternative)"
echo "   - Go to: https://heroku.com"
echo "   - Install Heroku CLI"
echo "   - Run: heroku create your-app-name"
echo "   - Run: heroku config:set GEMINI_API_KEY=your_key"
echo "   - Run: git push heroku main"
echo ""
echo "📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 Your app is ready for deployment!" 