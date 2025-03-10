import os
from flask import Flask, render_template, session
from flask_cors import CORS
from dotenv import load_dotenv
from src.frontend.test_routes import test_bp
from src.data.database import init_db, seed_questions
from src.utils.cli import register_cli

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Get the absolute path to the database file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'app.db')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', f'sqlite:///{db_path}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Initialize database
    init_db(app)
    
    # Seed questions
    seed_questions(app)
    
    # Register CLI commands
    register_cli(app)
    
    # Register blueprints
    app.register_blueprint(test_bp)
    
    # Main routes
    @app.route('/')
    def index():
        """Render the main landing page"""
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 