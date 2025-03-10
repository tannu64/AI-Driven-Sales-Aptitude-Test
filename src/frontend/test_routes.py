"""
Controller for the test interface.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from src.data.question_bank import CATEGORIES
from src.data.database import get_questions_from_db, save_test_result, get_test_result
from src.models.result_model import TestResult
from src.utils.ai_analyzer import ResponseAnalyzer

# Create blueprint
test_bp = Blueprint('test', __name__)

# Initialize response analyzer
analyzer = ResponseAnalyzer()


@test_bp.route('/test')
def test_page():
    """Render the test interface."""
    return render_template('test.html', categories=CATEGORIES)


@test_bp.route('/api/questions', methods=['GET'])
def get_questions():
    """API endpoint to retrieve test questions."""
    # Get query parameters
    num_questions = request.args.get('num_questions', type=int)
    categories = request.args.getlist('categories')
    
    # Get questions from database
    questions = get_questions_from_db()
    
    # Filter by category if specified
    if categories:
        questions = [q for q in questions if q.category in categories]
    
    # Limit number of questions if specified
    if num_questions and num_questions < len(questions):
        questions = questions[:num_questions]
    
    # Convert to dictionary format for JSON
    questions_dict = [q.to_dict() for q in questions]
    
    return jsonify(questions_dict)


@test_bp.route('/api/submit', methods=['POST'])
def submit_test():
    """API endpoint to submit test answers and get results."""
    # Get the submitted answers
    data = request.json
    user_id = data.get('user_id', session.get('user_id', 1))  # Default to user ID 1 if not logged in
    answers = data.get('answers', {})
    
    print(f"DEBUG: Received submission - user_id: {user_id}, answers: {answers}")
    
    if not answers:
        print("DEBUG: No answers provided")
        return jsonify({"error": "No answers provided"}), 400
    
    # Get the questions used in the test
    question_ids = [int(qid) for qid in answers.keys()]
    questions = get_questions_from_db()
    test_questions = [q for q in questions if q.id in question_ids]
    
    print(f"DEBUG: Found {len(test_questions)} questions for the test")
    
    # Create a test result object for processing
    result = TestResult(user_id, answers)
    
    # Calculate scores
    scores = result.calculate_scores(test_questions)
    print(f"DEBUG: Calculated scores: {scores}")
    
    # Generate analysis
    result.generate_analysis()
    print(f"DEBUG: Generated analysis: {result.analysis}")
    
    # Add AI-based analysis
    pattern_analysis = analyzer.analyze_response_patterns(answers)
    
    # Generate personalized feedback
    feedback = analyzer.generate_personalized_feedback(scores, result.analysis)
    
    # Save result to database
    db_result = save_test_result(
        user_id=user_id,
        answers=answers,
        scores=scores,
        analysis=result.analysis,
        recommendations=result.recommendations
    )
    
    print(f"DEBUG: Saved test result to database, ID: {db_result.id}")
    
    # Store result ID in session for results page
    session['test_result_id'] = db_result.id
    print(f"DEBUG: Stored test_result_id in session: {session['test_result_id']}")
    
    # Return the results
    response = {
        "scores": scores,
        "analysis": result.analysis,
        "recommendations": result.recommendations,
        "feedback": feedback,
        "pattern_analysis": pattern_analysis
    }
    
    return jsonify(response)


@test_bp.route('/results')
def results_page():
    """Render the results page."""
    # Get result ID from session
    result_id = session.get('test_result_id')
    
    if not result_id:
        # No result in session, redirect to no results page
        return render_template('no_results.html')
    
    # Get result from database
    result = get_test_result(result_id)
    
    if not result:
        # Result not found, redirect to no results page
        return render_template('no_results.html')
    
    # Convert to dictionary
    result_dict = result.to_dict()
    
    # Ensure scores and analysis exist
    if 'scores' not in result_dict or not result_dict['scores']:
        result_dict['scores'] = {'overall': 0}
    
    if 'analysis' not in result_dict or not result_dict['analysis']:
        result_dict['analysis'] = {'overall_assessment': 'Assessment not available'}
    
    # Generate feedback
    feedback = analyzer.generate_personalized_feedback(
        result_dict['scores'], 
        result_dict['analysis']
    )
    
    # Ensure feedback is a dictionary
    if not isinstance(feedback, dict):
        feedback = {
            'strengths': [],
            'areas_for_improvement': [],
            'recommendations': ['Focus on developing your core sales skills through structured training programs and mentorship.']
        }
    
    # Add a default recommendation if none exist
    if 'recommendations' not in feedback or not feedback['recommendations']:
        feedback['recommendations'] = ['Focus on developing your core sales skills through structured training programs and mentorship.']
    
    return render_template(
        'results.html',
        result=result_dict,
        feedback=feedback,
        categories=CATEGORIES
    ) 