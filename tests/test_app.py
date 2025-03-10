"""
Tests for the Flask application.
"""

import json
import pytest
from app import create_app
from src.data.database import db, User, Question, TestResult, Answer


def test_index_page(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI-Driven Sales Aptitude Test' in response.data
    assert b'Start the Test' in response.data


def test_test_page(client):
    """Test the test page."""
    response = client.get('/test')
    assert response.status_code == 200
    assert b'Ready to Begin?' in response.data
    assert b'Start the Test' in response.data


def test_get_questions_api(client):
    """Test the API endpoint for retrieving questions."""
    response = client.get('/api/questions')
    assert response.status_code == 200
    
    # Parse the JSON response
    data = json.loads(response.data)
    
    # Check that we got a list of questions
    assert isinstance(data, list)
    
    # Check that each question has the required fields
    if data:  # If there are questions
        question = data[0]
        assert 'id' in question
        assert 'text' in question
        assert 'category' in question
        assert 'type' in question


def test_submit_test_api(client, app):
    """Test the API endpoint for submitting test answers."""
    # Create a sample test submission
    sample_answers = {
        "1": "Agree",
        "2": "Neutral",
        "3": "Ask more questions to understand their budget constraints"
    }
    
    # Submit the test
    response = client.post(
        '/api/submit',
        json={"user_id": 1, "answers": sample_answers},
        content_type='application/json'
    )
    
    # Check the response
    assert response.status_code == 200
    
    # Parse the JSON response
    data = json.loads(response.data)
    
    # Check that the response contains the expected fields
    assert 'scores' in data
    assert 'analysis' in data
    assert 'recommendations' in data
    assert 'feedback' in data
    
    # Check that the test result was saved to the database
    with app.app_context():
        # Get the most recent test result for user 1
        test_result = TestResult.query.filter_by(user_id=1).order_by(TestResult.id.desc()).first()
        assert test_result is not None
        
        # Check that the answers were saved
        answers = Answer.query.filter_by(test_result_id=test_result.id).all()
        assert len(answers) == len(sample_answers)


def test_results_page_with_no_result(client):
    """Test the results page when no test result is in the session."""
    # Clear the session
    with client.session_transaction() as session:
        if 'test_result_id' in session:
            del session['test_result_id']
    
    # Access the results page
    response = client.get('/results')
    assert response.status_code == 200
    assert b'No Test Results Found' in response.data


def test_results_page_with_result(client, app):
    """Test the results page with a test result in the session."""
    # Create a test result
    with app.app_context():
        # Check if user 1 exists, create if not
        user = User.query.get(1)
        if not user:
            user = User(
                id=1,
                username='testuser',
                email='test@example.com',
                password_hash='pbkdf2:sha256:150000$abc123',
                first_name='Test',
                last_name='User'
            )
            db.session.add(user)
            db.session.commit()
        
        # Create a test result
        import json
        test_result = TestResult(
            user_id=1,
            overall_score=4.2,
            scores_json=json.dumps({
                "relationship_building": 4.5,
                "resilience": 4.0,
                "negotiation": 3.8,
                "overall": 4.2
            }),
            analysis_json=json.dumps({
                "strengths": ["relationship_building", "resilience"],
                "areas_for_improvement": [],
                "overall_assessment": "Strong sales aptitude with well-developed core skills."
            }),
            recommendations_json=json.dumps([
                "Your profile indicates strong potential for consultative sales roles."
            ])
        )
        db.session.add(test_result)
        db.session.commit()
        
        # Set the test result ID in the session
        with client.session_transaction() as session:
            session['test_result_id'] = test_result.id
    
    # Access the results page
    response = client.get('/results')
    assert response.status_code == 200
    assert b'Your Sales Aptitude Results' in response.data
    assert b'Overall Assessment' in response.data
    assert b'Strong sales aptitude' in response.data


def test_404_page(client):
    """Test the 404 error page."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data


def test_database_models(app):
    """Test the database models."""
    with app.app_context():
        # Test User model
        user = User(
            username='testuser2',
            email='test2@example.com',
            password_hash='pbkdf2:sha256:150000$abc123',
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()
        
        # Test retrieving the user
        retrieved_user = User.query.filter_by(username='testuser2').first()
        assert retrieved_user is not None
        assert retrieved_user.email == 'test2@example.com'
        assert retrieved_user.full_name == 'Test User'
        
        # Test Question model
        question = Question(
            text='Test question',
            category='test_category',
            type='likert',
            options_json=json.dumps(["Option 1", "Option 2", "Option 3"]),
            weight=1.0
        )
        db.session.add(question)
        db.session.commit()
        
        # Test retrieving the question
        retrieved_question = Question.query.filter_by(text='Test question').first()
        assert retrieved_question is not None
        assert retrieved_question.category == 'test_category'
        assert retrieved_question.type == 'likert'
        
        # Clean up
        db.session.delete(user)
        db.session.delete(question)
        db.session.commit() 