"""
Command-line interface utilities for the sales aptitude test.
"""

import click
from flask.cli import with_appcontext
from src.data.database import create_user, get_user_by_username, get_user_by_email, User, db


@click.group()
def user_cli():
    """User management commands."""
    pass


@user_cli.command('create')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@click.option('--first-name', '-f', help='User\'s first name')
@click.option('--last-name', '-l', help='User\'s last name')
@with_appcontext
def create_user_command(username, email, password, first_name=None, last_name=None):
    """Create a new user."""
    # Check if username already exists
    if get_user_by_username(username):
        click.echo(f"Error: Username '{username}' already exists.")
        return
    
    # Check if email already exists
    if get_user_by_email(email):
        click.echo(f"Error: Email '{email}' already exists.")
        return
    
    # Create user
    user = create_user(username, email, password, first_name, last_name)
    click.echo(f"User created: {user.username} (ID: {user.id})")


@user_cli.command('list')
@with_appcontext
def list_users_command():
    """List all users."""
    users = User.query.all()
    
    if not users:
        click.echo("No users found.")
        return
    
    click.echo("ID | Username | Email | Full Name")
    click.echo("-" * 50)
    
    for user in users:
        click.echo(f"{user.id} | {user.username} | {user.email} | {user.full_name}")


@user_cli.command('delete')
@click.argument('username')
@with_appcontext
def delete_user_command(username):
    """Delete a user by username."""
    user = get_user_by_username(username)
    
    if not user:
        click.echo(f"Error: User '{username}' not found.")
        return
    
    # Confirm deletion
    if not click.confirm(f"Are you sure you want to delete user '{username}'?"):
        click.echo("Operation cancelled.")
        return
    
    # Delete user
    db.session.delete(user)
    db.session.commit()
    
    click.echo(f"User '{username}' deleted.")


@user_cli.command('reset-password')
@click.argument('username')
@click.argument('new_password')
@with_appcontext
def reset_password_command(username, new_password):
    """Reset a user's password."""
    from werkzeug.security import generate_password_hash
    
    user = get_user_by_username(username)
    
    if not user:
        click.echo(f"Error: User '{username}' not found.")
        return
    
    # Reset password
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    click.echo(f"Password reset for user '{username}'.")


def register_cli(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(user_cli) 