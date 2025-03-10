"""
Pytest configuration file with fixtures for testing.
"""

import os
import tempfile
import pytest
from app import create_app
from src.utils.cli import register_cli


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the app with test configuration
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost',  # Add server name for url_for to work in tests
    })

    # Register CLI commands
    register_cli(app)

    # Create the database and load test data
    with app.app_context():
        # Initialize database if needed
        pass

    yield app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def sample_questions():
    """Return a list of sample questions for testing."""
    from src.models.question_model import LikertQuestion, ScenarioQuestion
    
    questions = [
        LikertQuestion(
            id=1,
            text="I enjoy meeting new people and building relationships.",
            category="relationship_building"
        ),
        LikertQuestion(
            id=2,
            text="I am comfortable with rejection and see it as part of the process.",
            category="resilience"
        ),
        ScenarioQuestion(
            id=3,
            text="A potential client is hesitant about your product's price. How would you respond?",
            category="negotiation",
            options=[
                "Immediately offer a discount to close the deal",
                "Emphasize the value and ROI of your product",
                "Ask more questions to understand their budget constraints",
                "Suggest a smaller package or alternative solution"
            ],
            correct_index=2
        )
    ]
    
    return questions


@pytest.fixture
def sample_answers():
    """Return a dictionary of sample answers for testing."""
    return {
        "1": "Agree",
        "2": "Neutral",
        "3": "Ask more questions to understand their budget constraints"
    } 