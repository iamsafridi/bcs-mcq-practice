# Setting Up Google Gemini API (Free)

## 🎯 Why Gemini?

Google Gemini provides much better, more relevant questions compared to the previous implementations. It's completely free and generates high-quality BCS-style questions.

## 📋 Steps to Get Free Gemini API Key

### Step 1: Go to Google AI Studio
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account

### Step 2: Create API Key
1. Click "Create API Key"
2. Give it a name (e.g., "BCS MCQ Generator")
3. Copy the generated API key

### Step 3: Add to Environment
1. Create or edit `.env` file in your project:
   ```bash
   nano .env
   ```

2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. Save the file (Ctrl+X, then Y, then Enter)

## 🚀 Benefits of Gemini

- ✅ **Completely Free**: No usage limits or costs
- ✅ **High Quality**: Generates relevant, BCS-style questions
- ✅ **Fast**: Quick response times
- ✅ **Reliable**: Google's infrastructure
- ✅ **Smart**: Understands context and generates appropriate questions

## 🔧 Testing

After setting up the API key, restart the application:

```bash
./start.sh
```

The system will now use Gemini AI to generate high-quality questions!

## 📊 Free Tier Limits

- **Queries per minute**: 60
- **Daily quota**: 15,000 requests
- **Cost**: $0 (completely free)

This is more than enough for BCS exam preparation! 