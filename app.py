from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
from werkzeug.utils import secure_filename
from text_processor import TextProcessor
from mcq_generator import MCQGenerator
from file_handler import FileHandler

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
text_processor = TextProcessor()
mcq_generator = MCQGenerator()
file_handler = FileHandler()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Extract text from file
            extracted_text = file_handler.extract_text(filepath)
            
            if not extracted_text:
                return jsonify({'error': 'Could not extract text from file'}), 400
            
            # Process and clean text
            processed_text = text_processor.process_text(extracted_text)
            
            # Store processed text temporarily (in production, use a database)
            session_id = str(uuid.uuid4())
            session_data = {
                'text': processed_text,
                'filename': filename,
                'filepath': filepath
            }
            
            # Save session data (in production, use Redis or database)
            with open(f'session_{session_id}.json', 'w') as f:
                json.dump(session_data, f)
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'filename': filename,
                'text_preview': processed_text[:500] + '...' if len(processed_text) > 500 else processed_text
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-mcq', methods=['POST'])
def generate_mcq():
    """Generate MCQ questions from uploaded content or text input"""
    try:
        # Check if it's a file upload or text input
        if 'file' in request.files:
            # Handle file upload
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            # Save file
            file.save(filepath)
            # Extract text from file
            extracted_text = file_handler.extract_text(filepath)
            if not extracted_text:
                return jsonify({'error': 'Could not extract text from file'}), 400
            # Process and clean text
            processed_text = text_processor.process_text(extracted_text)
        elif 'text_content' in request.form:
            # Handle text input
            text_content = request.form['text_content']
            if not text_content or len(text_content.strip()) < 50:
                return jsonify({'error': 'Please provide at least 50 characters of text'}), 400
            # Process and clean text
            processed_text = text_processor.process_text(text_content.strip())
        else:
            return jsonify({'error': 'No content provided'}), 400
        # Get quiz settings
        num_questions = int(request.form.get('num_questions', 10))
        difficulty = request.form.get('difficulty', 'medium')
        # Generate MCQ questions
        try:
            mcq_questions = mcq_generator.generate_questions(
                processed_text,
                num_questions=num_questions,
                difficulty=difficulty
            )
        except Exception as e:
            return jsonify({'success': False, 'error': f'MCQ generation failed: {str(e)}'}), 500
        return jsonify({
            'success': True,
            'questions': mcq_questions,
            'total_questions': len(mcq_questions)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'}), 500

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    """Handle answer submission and provide feedback"""
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        selected_answer = data.get('selected_answer')
        correct_answer = data.get('correct_answer')
        
        is_correct = selected_answer == correct_answer
        
        return jsonify({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'explanation': f"Your answer was {'correct' if is_correct else 'incorrect'}."
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 