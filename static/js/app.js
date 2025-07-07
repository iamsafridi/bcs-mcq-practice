// Global variables
let currentSessionId = null;
let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};
let quizScore = 0;
let quizHistory = JSON.parse(localStorage.getItem('quizHistory') || '[]');
let performanceStats = JSON.parse(localStorage.getItem('performanceStats') || '{}');

// DOM elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileInfo = document.getElementById('file-info');
const fileName = document.getElementById('file-name');
const fileSize = document.getElementById('file-size');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Only trigger file input on click if no file is selected
    uploadArea.addEventListener('click', (e) => {
        // Prevent triggering if clicking on file info or remove button
        if (!e.target.closest('.file-info') && !e.target.closest('.btn')) {
            // Only open file dialog if no file is currently uploaded
            if (!window.uploadedFile) {
                fileInput.click();
            }
        }
    });
}

// File handling functions
let isProcessingFile = false;

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && !isProcessingFile) {
        isProcessingFile = true;
        processFile(file);
        // Reset flag after a short delay
        setTimeout(() => {
            isProcessingFile = false;
        }, 1000);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    // Prevent double processing
    if (window.uploadedFile && window.uploadedFile.name === file.name) {
        isProcessingFile = false;
        return;
    }
    
    // Validate file type
    const allowedTypes = ['.pdf', '.docx', '.doc', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showToast('Please select a valid file type (PDF, DOCX, DOC, or TXT)', 'error');
        isProcessingFile = false;
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showToast('File size must be less than 16MB', 'error');
        isProcessingFile = false;
        return;
    }
    
    // Store file for later use
    window.uploadedFile = file;
    window.contentType = 'file';
    
    // Display file info
    displayFileInfo(file);
    
    // Show settings section
    showSection('settings-section');
    showToast('File uploaded successfully! Configure your quiz settings.', 'success');
}

function displayFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    
    // Update upload area to show it's not clickable
    const uploadArea = document.getElementById('upload-area');
    uploadArea.classList.add('file-uploaded');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile() {
    fileInput.value = '';
    fileInfo.style.display = 'none';
    window.uploadedFile = null;
    window.contentType = null;
    hideSection('settings-section');
    
    // Reset upload area to show it's clickable again
    const uploadArea = document.getElementById('upload-area');
    uploadArea.classList.remove('file-uploaded');
    
    showToast('File removed successfully!', 'info');
}

// MCQ Generation function
async function generateMCQ() {
    const numQuestions = document.getElementById('num-questions').value;
    const difficulty = document.getElementById('difficulty').value;
    
    if (!window.uploadedContent && !window.uploadedFile) {
        showToast('Please upload a file or enter text first!', 'error');
        return;
    }
    
    try {
        showSection('loading-section');
        hideSection('settings-section');
        
        const formData = new FormData();
        formData.append('num_questions', numQuestions);
        formData.append('difficulty', difficulty);
        
        // Add content based on type
        if (window.contentType === 'text') {
            formData.append('text_content', window.uploadedContent);
        } else {
            formData.append('file', window.uploadedFile);
        }
        
        const response = await fetch('/generate-mcq', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentQuestions = data.questions;
            currentQuestionIndex = 0;
            userAnswers = {};
            quizScore = 0;
            
            showToast(`Generated ${data.total_questions} questions!`, 'success');
            startQuiz();
        } else {
            showToast(data.error || 'Failed to generate questions', 'error');
            showSection('settings-section');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showToast('Failed to generate questions. Please try again.', 'error');
        showSection('settings-section');
    }
    
    hideSection('loading-section');
}

// --- BATCHED QUIZ LOGIC ---
const QUESTIONS_PER_BATCH = 5;
let currentBatchIndex = 0; // 0-based

function startQuiz() {
    showSection('quiz-section');
    currentBatchIndex = 0;
    renderBatch();
    updateProgress();
}

function renderBatch() {
    const start = currentBatchIndex * QUESTIONS_PER_BATCH;
    const end = Math.min(start + QUESTIONS_PER_BATCH, currentQuestions.length);
    const container = document.getElementById('multi-question-container');
    container.innerHTML = '';
    for (let i = start; i < end; i++) {
        const q = currentQuestions[i];
        const qDiv = document.createElement('div');
        qDiv.className = 'multi-question-block';
        // Question text
        const qText = document.createElement('div');
        qText.className = 'question';
        qText.textContent = `${i + 1}. ${q.question}`;
        qDiv.appendChild(qText);
        // Options
        const optsDiv = document.createElement('div');
        optsDiv.className = 'options-container';
        q.options.forEach((opt, optIdx) => {
            const optId = `q${i}-opt${optIdx}`;
            const label = document.createElement('label');
            label.className = 'option-radio-label';
            // Radio input
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question-${i}`;
            radio.id = optId;
            radio.value = optIdx;
            radio.className = 'option-radio';
            if (userAnswers[i] !== undefined) {
                radio.checked = userAnswers[i] === optIdx;
                radio.disabled = true;
            }
            radio.addEventListener('change', function(e) {
                if (userAnswers[i] === undefined) {
                    userAnswers[i] = optIdx;
                    // Lock all radios for this question
                    const radios = document.getElementsByName(`question-${i}`);
                    radios.forEach(r => r.disabled = true);
                    // Update navigation state immediately
                    updateBatchNavigation();
                }
            });
            // Round A/B/C/D
            const round = document.createElement('span');
            round.className = 'option-round';
            round.textContent = String.fromCharCode(65 + optIdx);
            // Only clicking the round triggers the radio
            round.addEventListener('click', function(e) {
                if (!radio.disabled) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
            label.appendChild(radio);
            label.appendChild(round);
            // Option text (no click event)
            const optText = document.createElement('span');
            optText.className = 'option-text';
            optText.textContent = opt.replace(/^\w\)\s*/, '');
            optText.style.pointerEvents = 'none';
            optText.style.userSelect = 'none';
            label.appendChild(optText);
            // On mobile, also prevent label text from being clickable
            label.addEventListener('touchstart', function(e) {
                if (e.target === optText) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            }, {passive: false});
            optsDiv.appendChild(label);
        });
        qDiv.appendChild(optsDiv);
        container.appendChild(qDiv);
    }
    updateBatchNavigation();
    updateBatchCounter();
}

function nextBatch() {
    const maxBatch = Math.floor((currentQuestions.length - 1) / QUESTIONS_PER_BATCH);
    if (currentBatchIndex < maxBatch) {
        currentBatchIndex++;
        renderBatch();
        updateProgress();
    } else {
        showResults();
    }
}

function previousBatch() {
    if (currentBatchIndex > 0) {
        currentBatchIndex--;
        renderBatch();
        updateProgress();
    }
}

function updateBatchNavigation() {
    const prevBtn = document.getElementById('prev-batch-btn');
    const nextBtn = document.getElementById('next-batch-btn');
    prevBtn.disabled = currentBatchIndex === 0;
    const maxBatch = Math.floor((currentQuestions.length - 1) / QUESTIONS_PER_BATCH);
    // Next is disabled only if all batches are done and all questions in last batch are answered
    const start = currentBatchIndex * QUESTIONS_PER_BATCH;
    const end = Math.min(start + QUESTIONS_PER_BATCH, currentQuestions.length);
    let allAnswered = true;
    for (let i = start; i < end; i++) {
        if (userAnswers[i] === undefined) {
            allAnswered = false;
            break;
        }
    }
    nextBtn.disabled = !allAnswered;
    if (currentBatchIndex === maxBatch) {
        nextBtn.innerHTML = 'Finish <i class="fas fa-check"></i>';
    } else {
        nextBtn.innerHTML = 'Next 5 <i class="fas fa-arrow-right"></i>';
    }
}

function updateBatchCounter() {
    const start = currentBatchIndex * QUESTIONS_PER_BATCH + 1;
    const end = Math.min(start + QUESTIONS_PER_BATCH - 1, currentQuestions.length);
    document.getElementById('question-counter').textContent = `Questions ${start}-${end} of ${currentQuestions.length}`;
}

// Results functions
function showResults() {
    calculateScore();
    displayResults();
    displayDetailedResults();
    showSection('results-section');
    hideSection('quiz-section');
}

function calculateScore() {
    quizScore = 0;
    let negativeMarks = 0;
    currentQuestions.forEach((question, index) => {
        if (userAnswers[index] !== undefined) {
            const selectedAnswer = String.fromCharCode(65 + userAnswers[index]); // Convert to A, B, C, D
            if (selectedAnswer === question.correct_answer) {
                quizScore++;
            } else {
                negativeMarks += 0.25;
            }
        }
    });
    quizScore = quizScore - negativeMarks;
    if (quizScore < 0) quizScore = 0;
    window.negativeMarks = negativeMarks;
}

function displayResults() {
    const totalQuestions = currentQuestions.length;
    const correctCount = currentQuestions.reduce((acc, question, index) => {
        const selectedAnswer = userAnswers[index] !== undefined ? String.fromCharCode(65 + userAnswers[index]) : null;
        return acc + (selectedAnswer === question.correct_answer ? 1 : 0);
    }, 0);
    const incorrectCount = totalQuestions - correctCount - (totalQuestions - Object.keys(userAnswers).length);
    const unansweredCount = totalQuestions - Object.keys(userAnswers).length;
    const percentage = Math.round((quizScore / totalQuestions) * 100);
    // Show total score achieved (including negative marking)
    const totalScoreElem = document.getElementById('total-score-achieved');
    if (totalScoreElem) {
        totalScoreElem.textContent = `Total Score: ${quizScore} / ${totalQuestions}`;
    }
    // Update main score display
    document.getElementById('final-score').textContent = percentage + '%';
    document.getElementById('correct-count').textContent = correctCount;
    document.getElementById('total-count').textContent = totalQuestions;
    document.getElementById('accuracy-rate').textContent = percentage + '%';
    // Update performance summary
    document.getElementById('correct-summary').textContent = correctCount;
    document.getElementById('incorrect-summary').textContent = incorrectCount;
    document.getElementById('unanswered-summary').textContent = unansweredCount;
    // Update score display
    document.getElementById('score-display').textContent = `Score: ${quizScore}/${totalQuestions}`;
    // Show negative marking info
    let negMarkElem = document.getElementById('negative-mark-info');
    if (!negMarkElem) {
        negMarkElem = document.createElement('div');
        negMarkElem.id = 'negative-mark-info';
        negMarkElem.style.marginTop = '10px';
        negMarkElem.style.color = '#dc3545';
        document.querySelector('.score-details').appendChild(negMarkElem);
    }
    negMarkElem.textContent = `Negative marks: -${window.negativeMarks || 0}`;
}

function displayDetailedResults() {
    const analysisContainer = document.getElementById('question-analysis');
    analysisContainer.innerHTML = '';
    
    currentQuestions.forEach((question, index) => {
        const userAnswer = userAnswers[index];
        const isCorrect = userAnswer !== undefined && 
                         String.fromCharCode(65 + userAnswer) === question.correct_answer;
        const isAnswered = userAnswer !== undefined;
        
        const questionItem = document.createElement('div');
        questionItem.className = `question-item ${isAnswered ? (isCorrect ? 'correct' : 'incorrect') : 'unanswered'}`;
        
        const status = isAnswered ? (isCorrect ? 'Correct' : 'Incorrect') : 'Unanswered';
        const statusClass = isAnswered ? (isCorrect ? 'correct' : 'incorrect') : 'unanswered';
        
        questionItem.innerHTML = `
            <div class="question-header">
                <span class="question-number">Question ${index + 1}</span>
                <span class="question-status ${statusClass}">${status}</span>
            </div>
            <div class="question-text">${question.question}</div>
            <div class="options-review">
                ${question.options.map((option, optionIndex) => {
                    const optionLetter = String.fromCharCode(65 + optionIndex);
                    const isSelected = userAnswer === optionIndex;
                    const isCorrectOption = optionLetter === question.correct_answer;
                    
                    let optionClass = 'option-review';
                    if (isSelected && isCorrectOption) {
                        optionClass += ' selected correct';
                    } else if (isSelected && !isCorrectOption) {
                        optionClass += ' selected incorrect';
                    } else if (isCorrectOption) {
                        optionClass += ' correct';
                    }
                    
                    return `<div class="${optionClass}">${option}</div>`;
                }).join('')}
            </div>
            <div class="explanation">
                <strong>Explanation:</strong> ${question.explanation}
            </div>
        `;
        
        analysisContainer.appendChild(questionItem);
    });
}

function downloadResults() {
    const results = {
        score: quizScore,
        total: currentQuestions.length,
        percentage: Math.round((quizScore / currentQuestions.length) * 100),
        date: new Date().toLocaleString(),
        questions: currentQuestions.map((question, index) => {
            const userAnswer = userAnswers[index];
            const isCorrect = userAnswer !== undefined && 
                             String.fromCharCode(65 + userAnswer) === question.correct_answer;
            
            return {
                questionNumber: index + 1,
                question: question.question,
                userAnswer: userAnswer !== undefined ? String.fromCharCode(65 + userAnswer) : 'Not answered',
                correctAnswer: question.correct_answer,
                isCorrect: isCorrect,
                explanation: question.explanation,
                options: question.options
            };
        })
    };
    
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `bcs-quiz-results-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showToast('Results downloaded successfully!', 'success');
}

function restartQuiz() {
    currentQuestionIndex = 0;
    userAnswers = {};
    quizScore = 0;
    startQuiz();
    hideSection('results-section');
}

function uploadNewFile() {
    hideSection('results-section');
    showSection('upload-section');
    
    // Reset all inputs
    fileInput.value = '';
    fileInfo.style.display = 'none';
    document.getElementById('text-input').value = '';
    window.uploadedFile = null;
    window.uploadedContent = null;
    window.contentType = null;
}

// Utility functions
function hideSection(sectionId) {
    document.getElementById(sectionId).style.display = 'none';
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    if (document.getElementById('quiz-section').style.display !== 'none') {
        switch(event.key) {
            case '1':
            case 'a':
            case 'A':
                selectOption(0);
                break;
            case '2':
            case 'b':
            case 'B':
                selectOption(1);
                break;
            case '3':
            case 'c':
            case 'C':
                selectOption(2);
                break;
            case '4':
            case 'd':
            case 'D':
                selectOption(3);
                break;
            case 'ArrowLeft':
                if (!document.getElementById('prev-btn').disabled) {
                    previousQuestion();
                }
                break;
            case 'ArrowRight':
            case 'Enter':
                if (!document.getElementById('next-btn').disabled) {
                    nextQuestion();
                }
                break;
        }
    }
});

// Mobile touch gestures
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', function(event) {
    touchStartX = event.changedTouches[0].screenX;
});

document.addEventListener('touchend', function(event) {
    touchEndX = event.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (document.getElementById('quiz-section').style.display !== 'none') {
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next question
                if (!document.getElementById('next-btn').disabled) {
                    nextQuestion();
                }
            } else {
                // Swipe right - previous question
                if (!document.getElementById('prev-btn').disabled) {
                    previousQuestion();
                }
            }
        }
    }
}

// Add mobile-specific enhancements
function addMobileEnhancements() {
    // Add touch feedback to options
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        option.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        option.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Call mobile enhancements when quiz starts
function startQuiz() {
    showSection('quiz-section');
    currentBatchIndex = 0;
    renderBatch();
    updateProgress();
    addMobileEnhancements();
}

// Text input functions
function useTextInput() {
    const textInput = document.getElementById('text-input');
    const text = textInput.value.trim();
    
    if (!text) {
        showToast('Please enter some text first!', 'error');
        return;
    }
    
    if (text.length < 50) {
        showToast('Please enter at least 50 characters for better question generation!', 'error');
        return;
    }
    
    // Store the text content
    window.uploadedContent = text;
    window.contentType = 'text';
    
    // Show settings section
    showSection('settings-section');
    showToast('Text content ready! Configure your quiz settings.', 'success');
}

function clearTextInput() {
    document.getElementById('text-input').value = '';
    window.uploadedContent = null;
    window.contentType = null;
    showToast('Text cleared!', 'success');
}

// Professional Features

// Navigation and Section Management
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Update navigation tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Find and activate corresponding tab
    const activeTab = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
    
    // Show dashboard tab if we have quiz history
    if (quizHistory.length > 0) {
        const dashboardTab = document.getElementById('dashboard-tab');
        if (dashboardTab) {
            dashboardTab.style.display = 'inline-flex';
        }
    }
}

// Dashboard Functions
function updateDashboard() {
    if (quizHistory.length === 0) return;
    
    // Update metrics
    const totalQuizzes = quizHistory.length;
    const totalQuestions = quizHistory.reduce((sum, quiz) => sum + quiz.totalQuestions, 0);
    const avgScore = Math.round(quizHistory.reduce((sum, quiz) => sum + quiz.score, 0) / totalQuizzes);
    
    document.getElementById('total-quizzes').textContent = totalQuizzes;
    document.getElementById('avg-score').textContent = avgScore + '%';
    document.getElementById('questions-answered').textContent = totalQuestions;
    
    // Update recent scores
    const recentScoresContainer = document.getElementById('recent-scores');
    recentScoresContainer.innerHTML = '';
    
    const recentQuizzes = quizHistory.slice(-5).reverse();
    recentQuizzes.forEach(quiz => {
        const scoreItem = document.createElement('div');
        scoreItem.className = 'score-item';
        scoreItem.innerHTML = `
            <span class="score">${quiz.score}%</span>
            <span class="date">${new Date(quiz.date).toLocaleDateString()}</span>
        `;
        recentScoresContainer.appendChild(scoreItem);
    });
}

// Enhanced Results with History
function saveQuizResults() {
    const quizResult = {
        date: new Date().toISOString(),
        score: Math.round((quizScore / currentQuestions.length) * 100),
        correctAnswers: quizScore,
        totalQuestions: currentQuestions.length,
        difficulty: document.getElementById('difficulty').value,
        questions: currentQuestions.length
    };
    
    quizHistory.push(quizResult);
    localStorage.setItem('quizHistory', JSON.stringify(quizHistory));
    
    // Update performance stats
    updatePerformanceStats(quizResult);
    
    // Update dashboard
    updateDashboard();
}

function updatePerformanceStats(quizResult) {
    const difficulty = quizResult.difficulty;
    if (!performanceStats[difficulty]) {
        performanceStats[difficulty] = {
            totalQuizzes: 0,
            totalScore: 0,
            bestScore: 0,
            averageScore: 0
        };
    }
    
    const stats = performanceStats[difficulty];
    stats.totalQuizzes++;
    stats.totalScore += quizResult.score;
    stats.averageScore = Math.round(stats.totalScore / stats.totalQuizzes);
    
    if (quizResult.score > stats.bestScore) {
        stats.bestScore = quizResult.score;
    }
    
    localStorage.setItem('performanceStats', JSON.stringify(performanceStats));
}

// Enhanced Settings
function resetSettings() {
    document.getElementById('num-questions').value = '10';
    document.getElementById('difficulty').value = 'medium';
    document.getElementById('time-limit').value = '0';
    
    // Reset checkboxes
    document.getElementById('factual-questions').checked = true;
    document.getElementById('conceptual-questions').checked = true;
    document.getElementById('analytical-questions').checked = true;
    
    showToast('Settings reset to default!', 'info');
}

// Enhanced MCQ Generation with Advanced Settings
async function generateMCQ() {
    const numQuestions = document.getElementById('num-questions').value;
    const difficulty = document.getElementById('difficulty').value;
    const timeLimit = document.getElementById('time-limit').value;
    
    // Get question types
    const questionTypes = [];
    if (document.getElementById('factual-questions').checked) questionTypes.push('factual');
    if (document.getElementById('conceptual-questions').checked) questionTypes.push('conceptual');
    if (document.getElementById('analytical-questions').checked) questionTypes.push('analytical');
    
    if (questionTypes.length === 0) {
        showToast('Please select at least one question type!', 'error');
        return;
    }
    
    if (!window.uploadedContent && !window.uploadedFile) {
        showToast('Please upload a file or enter text first!', 'error');
        return;
    }
    
    try {
        showSection('loading-section');
        hideSection('settings-section');
        
        const formData = new FormData();
        formData.append('num_questions', numQuestions);
        formData.append('difficulty', difficulty);
        formData.append('time_limit', timeLimit);
        formData.append('question_types', JSON.stringify(questionTypes));
        
        // Add content based on type
        if (window.contentType === 'text') {
            formData.append('text_content', window.uploadedContent);
        } else {
            formData.append('file', window.uploadedFile);
        }
        
        const response = await fetch('/generate-mcq', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentQuestions = data.questions;
            currentQuestionIndex = 0;
            userAnswers = {};
            quizScore = 0;
            
            // Start timer if time limit is set
            if (timeLimit > 0) {
                startTimer(parseInt(timeLimit));
            }
            
            showToast(`Generated ${data.total_questions} questions!`, 'success');
            startQuiz();
        } else {
            showToast(data.error || 'Failed to generate questions', 'error');
            showSection('settings-section');
        }
    } catch (error) {
        console.error('Generation error:', error);
        showToast('Failed to generate questions. Please try again.', 'error');
        showSection('settings-section');
    }
    
    hideSection('loading-section');
}

// Timer functionality
let timerInterval = null;
let timeRemaining = 0;

function startTimer(seconds) {
    timeRemaining = seconds;
    updateTimerDisplay();
    
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();
        
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            showToast('Time\'s up! Submitting quiz...', 'info');
            showResults();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    
    // Add timer to quiz header if it doesn't exist
    let timerElement = document.getElementById('timer');
    if (!timerElement) {
        timerElement = document.createElement('div');
        timerElement.id = 'timer';
        timerElement.className = 'timer';
        document.querySelector('.quiz-stats').appendChild(timerElement);
    }
    
    timerElement.textContent = `Time: ${timeString}`;
    timerElement.style.color = timeRemaining <= 30 ? '#dc3545' : '#495057';
}

// Enhanced Results Display
function showResults() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    calculateScore();
    saveQuizResults();
    displayResults();
    displayDetailedResults();
    showSection('results-section');
}

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateDashboard();
}); 

function updateProgress() {
    // Calculate progress based on answered questions
    let answered = 0;
    for (let i = 0; i < currentQuestions.length; i++) {
        if (userAnswers[i] !== undefined) answered++;
    }
    const percent = (answered / currentQuestions.length) * 100;
    const fill = document.getElementById('progress-fill');
    if (fill) fill.style.width = percent + '%';
} 