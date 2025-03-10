"""
Tests for the CLI commands.
"""

import pytest
from app import create_app
from src.data.database import db, User, get_user_by_username


def test_create_user_command(runner, app):
    """Test the create user command."""
    # Make sure the test user doesn't exist
    with app.app_context():
        user = get_user_by_username('testcli')
        if user:
            db.session.delete(user)
            db.session.commit()
    
    # Run the command
    result = runner.invoke(app.cli, [
        'user-cli', 'create', 'testcli', 'testcli@example.com', 'password',
        '--first-name', 'Test', '--last-name', 'CLI'
    ])
    
    # Check the output
    assert 'User created: testcli' in result.output
    
    # Verify the user was created in the database
    with app.app_context():
        user = get_user_by_username('testcli')
        assert user is not None
        assert user.email == 'testcli@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'CLI'
        assert user.full_name == 'Test CLI'
        
        # Clean up
        db.session.delete(user)
        db.session.commit()


def test_list_users_command(runner, app):
    """Test the list users command."""
    # Create a test user
    with app.app_context():
        user = get_user_by_username('testcli')
        if not user:
            user = User(
                username='testcli',
                email='testcli@example.com',
                password_hash='pbkdf2:sha256:150000$abc123',
                first_name='Test',
                last_name='CLI'
            )
            db.session.add(user)
            db.session.commit()
    
    # Run the command
    result = runner.invoke(app.cli, ['user-cli', 'list'])
    
    # Check the output
    assert 'testcli' in result.output
    assert 'testcli@example.com' in result.output
    
    # Clean up
    with app.app_context():
        user = get_user_by_username('testcli')
        if user:
            db.session.delete(user)
            db.session.commit()


def test_reset_password_command(runner, app):
    """Test the reset password command."""
    # Create a test user
    with app.app_context():
        user = get_user_by_username('testcli')
        if not user:
            user = User(
                username='testcli',
                email='testcli@example.com',
                password_hash='pbkdf2:sha256:150000$abc123',
                first_name='Test',
                last_name='CLI'
            )
            db.session.add(user)
            db.session.commit()
        
        # Store the original password hash
        original_hash = user.password_hash
    
    # Run the command
    result = runner.invoke(app.cli, ['user-cli', 'reset-password', 'testcli', 'newpassword'])
    
    # Check the output
    assert 'Password reset for user' in result.output
    
    # Verify the password was changed
    with app.app_context():
        user = get_user_by_username('testcli')
        assert user is not None
        assert user.password_hash != original_hash
        
        # Clean up
        db.session.delete(user)
        db.session.commit()


def test_delete_user_command(runner, app):
    """Test the delete user command."""
    # Create a test user
    with app.app_context():
        user = get_user_by_username('testcli')
        if not user:
            user = User(
                username='testcli',
                email='testcli@example.com',
                password_hash='pbkdf2:sha256:150000$abc123',
                first_name='Test',
                last_name='CLI'
            )
            db.session.add(user)
            db.session.commit()
    
    # Run the command with confirmation
    result = runner.invoke(app.cli, ['user-cli', 'delete', 'testcli'], input='y\n')
    
    # Check the output
    assert "User 'testcli' deleted" in result.output
    
    # Verify the user was deleted
    with app.app_context():
        user = get_user_by_username('testcli')
        assert user is None 