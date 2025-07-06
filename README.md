# 🎓 BCS MCQ Practice System

A comprehensive, mobile-responsive MCQ (Multiple Choice Question) generation and practice system designed specifically for Special BCS (Bangladesh Civil Service) exam preparation. This system allows users to upload study materials and automatically generates high-quality, BCS-style practice questions using Google's Gemini AI.

## 🎯 Features

- **📱 Mobile-Responsive Design**: Optimized for all devices with touch gestures and mobile-friendly interface
- **📄 Multi-Format Support**: Upload PDF, DOCX, and TXT files or paste text directly
- **🤖 AI-Powered Generation**: Uses Google Gemini AI for intelligent, high-quality question creation
- **🎯 BCS-Style Questions**: Questions specifically designed for BCS examination patterns and difficulty levels
- **📊 Interactive Quiz Interface**: User-friendly quiz taking experience with keyboard shortcuts
- **📈 Progress Tracking**: Real-time progress monitoring with visual indicators
- **📋 Comprehensive Results**: Detailed performance analysis with explanations and downloadable reports
- **🎚️ Multiple Difficulty Levels**: Easy, Medium, and Hard question options
- **⚙️ Customizable Settings**: Adjust number of questions and difficulty levels
- **🔄 Touch Gestures**: Swipe navigation for mobile devices
- **🎨 Modern UI/UX**: Beautiful, intuitive interface with smooth animations
- **💾 Result Export**: Download detailed results as JSON
- **🔒 Privacy-Focused**: No data storage, files processed locally

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection (for AI question generation)
- Google account (for free Gemini API key)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Mcq
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp config.env.example .env
   ```
   
   For best results, add your free Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   See `GEMINI_SETUP.md` for detailed setup instructions.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 How to Use

### Step 1: Add Study Material
**Option A: Upload File**
- Click "Choose File" or drag and drop your study material
- Supported formats: PDF, DOCX, DOC, TXT
- Maximum file size: 16MB

**Option B: Enter Text Directly**
- Paste your study material text in the text area
- Minimum 50 characters for better question generation
- Perfect for quick practice with notes or copied content

### Step 2: Configure Quiz Settings
- Select number of questions (5, 10, 15, or 20)
- Choose difficulty level (Easy, Medium, Hard)
- Click "Generate MCQ Questions"

### Step 3: Practice
- Answer questions by clicking on options
- Use keyboard shortcuts (A, B, C, D or 1, 2, 3, 4)
- Navigate with arrow keys or buttons
- Track your progress in real-time

### Step 4: Review Results
- View your final score and performance
- Restart the quiz or upload new material

## 🎮 Keyboard Shortcuts & Mobile Controls

### Desktop Controls
During the quiz, you can use these keyboard shortcuts:
- **A, B, C, D** or **1, 2, 3, 4**: Select answer options
- **Left Arrow**: Previous question
- **Right Arrow** or **Enter**: Next question

### Mobile Controls
- **Tap options**: Select answers
- **Swipe left**: Next question
- **Swipe right**: Previous question
- **Touch feedback**: Visual feedback on option selection

## 🔧 Configuration

### AI Setup

The system uses Google Gemini AI for high-quality question generation:

- **Service**: Google Gemini (free tier)
- **Processing**: Cloud-based AI processing
- **Cost**: Completely free - no API costs or usage limits
- **Quality**: High-quality, relevant BCS-style questions

**Note**: Requires internet connection for AI question generation. See `GEMINI_SETUP.md` for API key setup.

### Customization

You can customize various aspects:

- **Question Count**: Modify the options in the HTML template
- **Difficulty Levels**: Adjust in the MCQ generator
- **File Size Limits**: Change in `app.py`
- **UI Colors**: Modify `static/css/style.css`

## 📁 Project Structure

```
Mcq/
├── app.py                    # Main Flask application
├── file_handler.py           # File processing and text extraction
├── text_processor.py         # Text cleaning and processing
├── mcq_generator.py          # Main MCQ generation logic
├── gemini_mcq_generator.py   # Google Gemini AI integration
├── requirements.txt          # Python dependencies
├── config.env.example        # Environment variables template
├── GEMINI_SETUP.md          # Gemini API setup instructions
├── README.md                # This file
├── templates/
│   └── index.html           # Main web interface
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── app.js           # Frontend functionality
└── uploads/                 # Temporary file storage
```

## 🛠️ Technical Details

### Backend Technologies
- **Flask**: Web framework
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **Google Gemini AI**: AI question generation
- **Werkzeug**: File handling

### Frontend Technologies
- **HTML5**: Structure
- **CSS3**: Styling with modern design
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Typography

### AI Integration
The system uses Google's Gemini AI to generate contextually relevant questions based on the uploaded content. The AI creates high-quality BCS-style questions that test understanding rather than just memorization. The free tier provides 15,000 requests per day, which is more than sufficient for exam preparation.

## 🔒 Security & Privacy

- Files are processed locally and not stored permanently
- Session data is temporary and cleaned up automatically
- No personal data is collected or stored
- File uploads are validated for type and size

## 🐛 Troubleshooting

### Common Issues

1. **"Upload failed" error**
   - Check file format (PDF, DOCX, DOC, TXT only)
   - Ensure file size is under 16MB
   - Verify file is not corrupted

2. **"Failed to generate questions" error**
   - Check internet connection (for AI generation)
   - Verify Gemini API key is set correctly
   - Try with a different file

3. **Questions seem generic**
   - This happens when Gemini API key is not set
   - The system uses enhanced fallback generation
   - Add your free Gemini API key for better questions

### Performance Tips

- Use smaller files for faster processing
- Ensure stable internet connection for AI generation
- Questions generate quickly with Gemini AI
- Fallback generation works offline if needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Special thanks to Google for providing free Gemini AI
- Built with love for BCS aspirants
- Inspired by the need for better exam preparation tools

---

**Made with ❤️ for Special BCS preparation**

For support or questions, please open an issue in the repository. 