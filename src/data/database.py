"""
Database module for the sales aptitude test.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define models
class User(db.Model):
    """User model for database storage."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with test results
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @property
    def full_name(self):
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username or "Anonymous User"


class TestResult(db.Model):
    """Test result model for database storage."""
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    overall_score = db.Column(db.Float)
    
    # Store JSON data for scores, analysis, and recommendations
    scores_json = db.Column(db.Text)  # JSON string of category scores
    analysis_json = db.Column(db.Text)  # JSON string of analysis results
    recommendations_json = db.Column(db.Text)  # JSON string of recommendations
    
    # Relationship with answers
    answers = db.relationship('Answer', backref='test_result', lazy=True)
    
    def to_dict(self):
        """Convert test result to dictionary for JSON serialization."""
        import json
        return {
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "overall_score": self.overall_score,
            "scores": json.loads(self.scores_json) if self.scores_json else {},
            "analysis": json.loads(self.analysis_json) if self.analysis_json else {},
            "recommendations": json.loads(self.recommendations_json) if self.recommendations_json else []
        }


class Answer(db.Model):
    """Individual answer model for database storage."""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_results.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    def to_dict(self):
        """Convert answer to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "test_result_id": self.test_result_id,
            "question_id": self.question_id,
            "answer_text": self.answer_text
        }


class Question(db.Model):
    """Question model for database storage."""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'likert', 'scenario', 'open_ended'
    options_json = db.Column(db.Text)  # JSON string of options
    correct_index = db.Column(db.Integer)  # For scenario questions
    weight = db.Column(db.Float, default=1.0)
    min_words = db.Column(db.Integer)  # For open-ended questions
    max_words = db.Column(db.Integer)  # For open-ended questions
    
    def to_dict(self):
        """Convert question to dictionary for JSON serialization."""
        import json
        result = {
            "id": self.id,
            "text": self.text,
            "category": self.category,
            "type": self.type,
            "weight": self.weight
        }
        
        if self.options_json:
            result["options"] = json.loads(self.options_json)
        
        if self.correct_index is not None:
            result["correct_index"] = self.correct_index
            
        if self.min_words:
            result["min_words"] = self.min_words
            
        if self.max_words:
            result["max_words"] = self.max_words
            
        return result


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()


def seed_questions(app):
    """Seed the database with initial questions."""
    from src.data.question_bank import get_questions
    import json
    
    with app.app_context():
        # Check if questions already exist
        if Question.query.count() > 0:
            return
        
        # Get questions from question bank
        questions = get_questions()
        
        # Add questions to database
        for q in questions:
            db_question = Question(
                id=q.id,
                text=q.text,
                category=q.category,
                type=q.type,
                weight=q.weight
            )
            
            if hasattr(q, 'options'):
                db_question.options_json = json.dumps(q.options)
                
            if hasattr(q, 'correct_index') and q.correct_index is not None:
                db_question.correct_index = q.correct_index
                
            if hasattr(q, 'min_words') and q.min_words is not None:
                db_question.min_words = q.min_words
                
            if hasattr(q, 'max_words') and q.max_words is not None:
                db_question.max_words = q.max_words
            
            db.session.add(db_question)
        
        db.session.commit()


def create_user(username, email, password, first_name=None, last_name=None):
    """
    Create a new user in the database.
    
    Args:
        username (str): Username for login
        email (str): Email address
        password (str): Password (will be hashed)
        first_name (str): User's first name
        last_name (str): User's last name
        
    Returns:
        User: The created user object
    """
    from werkzeug.security import generate_password_hash
    
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user


def get_user_by_username(username):
    """
    Get a user by username.
    
    Args:
        username (str): Username to look up
        
    Returns:
        User: The user object, or None if not found
    """
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """
    Get a user by email.
    
    Args:
        email (str): Email to look up
        
    Returns:
        User: The user object, or None if not found
    """
    return User.query.filter_by(email=email).first()


def save_test_result(user_id, answers, scores, analysis, recommendations):
    """
    Save a test result to the database.
    
    Args:
        user_id (int): ID of the user who took the test
        answers (dict): Dictionary mapping question IDs to responses
        scores (dict): Dictionary of category scores
        analysis (dict): Analysis results
        recommendations (list): List of recommendations
        
    Returns:
        TestResult: The created test result object
    """
    import json
    
    print(f"DEBUG: Saving test result - user_id: {user_id}")
    print(f"DEBUG: Scores: {scores}")
    print(f"DEBUG: Analysis: {analysis}")
    
    # Ensure scores and analysis are properly formatted
    if not isinstance(scores, dict):
        print("DEBUG: Scores is not a dictionary, setting default")
        scores = {'overall': 0}
    
    if not isinstance(analysis, dict):
        print("DEBUG: Analysis is not a dictionary, setting default")
        analysis = {'overall_assessment': 'Assessment not available'}
    
    # Convert to JSON strings
    scores_json = json.dumps(scores)
    analysis_json = json.dumps(analysis)
    recommendations_json = json.dumps(recommendations)
    
    print(f"DEBUG: JSON strings - scores: {scores_json}, analysis: {analysis_json}")
    
    # Create test result
    test_result = TestResult(
        user_id=user_id,
        overall_score=scores.get('overall', 0),
        scores_json=scores_json,
        analysis_json=analysis_json,
        recommendations_json=recommendations_json
    )
    
    db.session.add(test_result)
    db.session.flush()  # Get the ID without committing
    
    print(f"DEBUG: Created test result with ID: {test_result.id}")
    
    # Create answers
    for question_id, answer_text in answers.items():
        answer = Answer(
            test_result_id=test_result.id,
            question_id=int(question_id),
            answer_text=answer_text
        )
        db.session.add(answer)
    
    # Commit the transaction to save everything to the database
    try:
        db.session.commit()
        print(f"DEBUG: Successfully committed test result to database")
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error committing test result to database: {e}")
        raise
    
    # Verify the test result was saved
    saved_result = TestResult.query.get(test_result.id)
    if saved_result:
        print(f"DEBUG: Verified test result was saved, ID: {saved_result.id}")
    else:
        print(f"DEBUG: Failed to verify test result was saved, ID: {test_result.id}")
    
    return test_result


def get_test_results_for_user(user_id):
    """
    Get all test results for a user.
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        list: List of TestResult objects
    """
    return TestResult.query.filter_by(user_id=user_id).order_by(TestResult.timestamp.desc()).all()


def get_test_result(result_id):
    """
    Get a test result by ID.
    
    Args:
        result_id (int): ID of the test result
        
    Returns:
        TestResult: The test result object, or None if not found
    """
    print(f"DEBUG: Getting test result with ID: {result_id}")
    
    result = TestResult.query.get(result_id)
    
    if result:
        print(f"DEBUG: Found test result with ID: {result_id}")
        print(f"DEBUG: Scores JSON: {result.scores_json}")
        print(f"DEBUG: Analysis JSON: {result.analysis_json}")
    else:
        print(f"DEBUG: Test result with ID {result_id} not found")
    
    return result


def get_questions_from_db():
    """
    Get all questions from the database.
    
    Returns:
        list: List of Question objects
    """
    return Question.query.all() 