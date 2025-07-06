#!/bin/bash

echo "🚀 Starting BCS MCQ Practice System..."
echo "=================================================="

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import flask, PyPDF2, docx, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some required packages are missing."
    echo "Please run: python3 -m pip install --break-system-packages -r requirements.txt"
    exit 1
fi

echo "✅ All dependencies are installed"

# Create necessary directories
mkdir -p uploads templates static/css static/js

echo "🎯 Starting the application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo "=================================================="

# Start the application
python3 app.py 