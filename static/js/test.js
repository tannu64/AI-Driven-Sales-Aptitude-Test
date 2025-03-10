/**
 * Test Interface JavaScript
 * Handles the interactive functionality of the sales aptitude test
 */

// Global variables
let questions = [];
let currentQuestionIndex = 0;
let answers = {};
let testStarted = false;

// DOM Elements
const startContainer = document.getElementById('start-container');
const testContainer = document.getElementById('test-container');
const resultContainer = document.getElementById('result-container');
const questionElement = document.getElementById('question');
const optionsElement = document.getElementById('options');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const submitButton = document.getElementById('submit-button');
const startButton = document.getElementById('start-button');
const loadingIndicator = document.getElementById('loading-indicator');

/**
 * Initialize the test interface
 */
function initTest() {
    // Add event listeners
    if (startButton) {
        startButton.addEventListener('click', startTest);
    }
    
    if (prevButton) {
        prevButton.addEventListener('click', showPreviousQuestion);
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', showNextQuestion);
    }
    
    if (submitButton) {
        submitButton.addEventListener('click', submitTest);
    }
    
    // Hide test and result containers initially
    if (testContainer) testContainer.style.display = 'none';
    if (resultContainer) resultContainer.style.display = 'none';
    if (loadingIndicator) loadingIndicator.style.display = 'none';
}

/**
 * Start the test
 */
async function startTest() {
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (startContainer) startContainer.style.display = 'none';
    
    try {
        // Fetch questions from API
        const response = await fetch('/api/questions');
        if (!response.ok) {
            throw new Error('Failed to fetch questions');
        }
        
        questions = await response.json();
        
        if (questions.length === 0) {
            throw new Error('No questions available');
        }
        
        // Initialize the test
        currentQuestionIndex = 0;
        answers = {};
        testStarted = true;
        
        // Show the first question
        showQuestion(currentQuestionIndex);
        
        // Show test container
        if (testContainer) testContainer.style.display = 'block';
    } catch (error) {
        console.error('Error starting test:', error);
        alert('There was an error starting the test. Please try again later.');
        
        // Show start container again
        if (startContainer) startContainer.style.display = 'block';
    } finally {
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * Display a question
 * @param {number} index - The index of the question to display
 */
function showQuestion(index) {
    if (!questions || index < 0 || index >= questions.length) {
        return;
    }
    
    const question = questions[index];
    
    // Update question text
    if (questionElement) {
        questionElement.textContent = question.text;
    }
    
    // Clear previous options
    if (optionsElement) {
        optionsElement.innerHTML = '';
        
        // Create options based on question type
        if (question.type === 'likert') {
            createLikertOptions(question);
        } else if (question.type === 'scenario') {
            createScenarioOptions(question);
        } else if (question.type === 'open_ended') {
            createOpenEndedInput(question);
        }
    }
    
    // Update progress
    updateProgress();
    
    // Update button states
    updateButtonStates();
}

/**
 * Create Likert scale options
 * @param {Object} question - The question object
 */
function createLikertOptions(question) {
    if (!optionsElement) return;
    
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option-item';
        if (answers[question.id] === option) {
            optionDiv.classList.add('selected');
        }
        
        optionDiv.textContent = option;
        optionDiv.addEventListener('click', () => {
            // Remove selected class from all options
            document.querySelectorAll('.option-item').forEach(item => {
                item.classList.remove('selected');
            });
            
            // Add selected class to clicked option
            optionDiv.classList.add('selected');
            
            // Save answer
            answers[question.id] = option;
            
            // Update button states
            updateButtonStates();
        });
        
        optionsElement.appendChild(optionDiv);
    });
}

/**
 * Create scenario question options
 * @param {Object} question - The question object
 */
function createScenarioOptions(question) {
    if (!optionsElement) return;
    
    question.options.forEach((option, index) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option-item';
        if (answers[question.id] === option) {
            optionDiv.classList.add('selected');
        }
        
        optionDiv.textContent = option;
        optionDiv.addEventListener('click', () => {
            // Remove selected class from all options
            document.querySelectorAll('.option-item').forEach(item => {
                item.classList.remove('selected');
            });
            
            // Add selected class to clicked option
            optionDiv.classList.add('selected');
            
            // Save answer
            answers[question.id] = option;
            
            // Update button states
            updateButtonStates();
        });
        
        optionsElement.appendChild(optionDiv);
    });
}

/**
 * Create open-ended question input
 * @param {Object} question - The question object
 */
function createOpenEndedInput(question) {
    if (!optionsElement) return;
    
    const inputContainer = document.createElement('div');
    inputContainer.className = 'mb-3';
    
    const textarea = document.createElement('textarea');
    textarea.className = 'form-control';
    textarea.rows = 5;
    textarea.placeholder = 'Type your answer here...';
    
    if (answers[question.id]) {
        textarea.value = answers[question.id];
    }
    
    // Add word count display if min/max words specified
    let wordCountDisplay = null;
    if (question.min_words || question.max_words) {
        wordCountDisplay = document.createElement('div');
        wordCountDisplay.className = 'text-muted mt-2';
        
        let countText = 'Word count: 0';
        if (question.min_words) {
            countText += ` (minimum: ${question.min_words})`;
        }
        if (question.max_words) {
            countText += ` (maximum: ${question.max_words})`;
        }
        
        wordCountDisplay.textContent = countText;
        
        // Update word count on input
        textarea.addEventListener('input', () => {
            const wordCount = textarea.value.trim().split(/\s+/).filter(Boolean).length;
            
            let countText = `Word count: ${wordCount}`;
            if (question.min_words) {
                countText += ` (minimum: ${question.min_words})`;
            }
            if (question.max_words) {
                countText += ` (maximum: ${question.max_words})`;
            }
            
            wordCountDisplay.textContent = countText;
            
            // Save answer
            answers[question.id] = textarea.value;
            
            // Update button states
            updateButtonStates();
        });
    } else {
        // Save answer on input
        textarea.addEventListener('input', () => {
            answers[question.id] = textarea.value;
            
            // Update button states
            updateButtonStates();
        });
    }
    
    inputContainer.appendChild(textarea);
    if (wordCountDisplay) {
        inputContainer.appendChild(wordCountDisplay);
    }
    
    optionsElement.appendChild(inputContainer);
}

/**
 * Show the previous question
 */
function showPreviousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showQuestion(currentQuestionIndex);
    }
}

/**
 * Show the next question
 */
function showNextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        showQuestion(currentQuestionIndex);
    }
}

/**
 * Update the progress bar and text
 */
function updateProgress() {
    if (!progressBar || !progressText || questions.length === 0) return;
    
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressBar.style.width = `${progress}%`;
    progressText.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
}

/**
 * Update button states based on current question and answers
 */
function updateButtonStates() {
    if (!prevButton || !nextButton || !submitButton) return;
    
    // Previous button is disabled on first question
    prevButton.disabled = currentQuestionIndex === 0;
    
    // Next button is enabled if there's a next question and current question is answered
    const currentQuestion = questions[currentQuestionIndex];
    const hasAnswer = answers[currentQuestion.id] !== undefined;
    
    nextButton.disabled = currentQuestionIndex >= questions.length - 1 || !hasAnswer;
    
    // Submit button is enabled on last question if all questions are answered
    const isLastQuestion = currentQuestionIndex === questions.length - 1;
    const allAnswered = questions.every(q => answers[q.id] !== undefined);
    
    submitButton.disabled = !isLastQuestion || !allAnswered;
}

/**
 * Submit the test
 */
async function submitTest() {
    if (!allQuestionsAnswered()) {
        alert('Please answer all questions before submitting.');
        return;
    }
    
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (submitButton) submitButton.disabled = true;
    
    try {
        // Submit answers to API
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: generateUserId(),
                answers: answers
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit test');
        }
        
        const result = await response.json();
        
        // Redirect to results page
        window.location.href = '/results';
    } catch (error) {
        console.error('Error submitting test:', error);
        alert('There was an error submitting your test. Please try again.');
        
        if (submitButton) submitButton.disabled = false;
    } finally {
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * Check if all questions have been answered
 * @returns {boolean} True if all questions are answered
 */
function allQuestionsAnswered() {
    return questions.every(q => answers[q.id] !== undefined);
}

/**
 * Generate a unique user ID
 * @returns {string} A unique user ID
 */
function generateUserId() {
    return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Initialize the test when the DOM is loaded
document.addEventListener('DOMContentLoaded', initTest); 