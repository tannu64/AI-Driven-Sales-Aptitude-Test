"""
Question bank for the sales aptitude test.
"""

from src.models.question_model import LikertQuestion, ScenarioQuestion, OpenEndedQuestion

# Define categories/traits being measured
CATEGORIES = {
    "relationship_building": "Relationship Building",
    "resilience": "Resilience",
    "persuasion": "Persuasion",
    "listening": "Active Listening",
    "problem_solving": "Problem Solving",
    "goal_orientation": "Goal Orientation",
    "adaptability": "Adaptability",
    "product_knowledge": "Product Knowledge",
    "negotiation": "Negotiation Skills",
    "time_management": "Time Management"
}

def get_questions():
    """
    Return a list of questions for the sales aptitude test.
    
    Returns:
        list: List of Question objects
    """
    questions = []
    
    # Likert scale questions
    likert_questions = [
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
        LikertQuestion(
            id=3,
            text="I find it easy to persuade others to see my point of view.",
            category="persuasion"
        ),
        LikertQuestion(
            id=4,
            text="I listen carefully to understand others' needs before offering solutions.",
            category="listening"
        ),
        LikertQuestion(
            id=5,
            text="I enjoy solving complex problems for customers.",
            category="problem_solving"
        ),
        LikertQuestion(
            id=6,
            text="I set ambitious goals for myself and consistently work to achieve them.",
            category="goal_orientation"
        ),
        LikertQuestion(
            id=7,
            text="I can quickly adapt my approach based on a customer's response.",
            category="adaptability"
        ),
        LikertQuestion(
            id=8,
            text="I enjoy learning detailed information about products and services.",
            category="product_knowledge"
        ),
        LikertQuestion(
            id=9,
            text="I am comfortable discussing pricing and negotiating terms.",
            category="negotiation"
        ),
        LikertQuestion(
            id=10,
            text="I manage my time effectively to maximize productivity.",
            category="time_management"
        ),
    ]
    questions.extend(likert_questions)
    
    # Scenario questions
    scenario_questions = [
        ScenarioQuestion(
            id=11,
            text="A potential client is hesitant about your product's price. How would you respond?",
            category="negotiation",
            options=[
                "Immediately offer a discount to close the deal",
                "Emphasize the value and ROI of your product",
                "Ask more questions to understand their budget constraints",
                "Suggest a smaller package or alternative solution"
            ],
            correct_index=2  # Asking more questions is the best approach
        ),
        ScenarioQuestion(
            id=12,
            text="You've been trying to reach a prospect for weeks with no response. What would you do?",
            category="resilience",
            options=[
                "Give up and focus on other prospects",
                "Continue with the same approach, hoping for a response",
                "Try a new communication channel or approach",
                "Escalate to the prospect's manager"
            ],
            correct_index=2  # Trying a new approach shows adaptability
        ),
        ScenarioQuestion(
            id=13,
            text="A customer has a complex problem that your product can only partially solve. How do you proceed?",
            category="problem_solving",
            options=[
                "Focus only on the aspects your product can solve",
                "Oversell your product's capabilities",
                "Acknowledge limitations and suggest complementary solutions",
                "Refer them to a competitor with a more suitable product"
            ],
            correct_index=2  # Honest problem-solving approach
        ),
        ScenarioQuestion(
            id=14,
            text="You have multiple high-priority tasks due today. How do you manage this situation?",
            category="time_management",
            options=[
                "Work on the easiest tasks first to build momentum",
                "Prioritize based on deadline and importance",
                "Ask for deadline extensions on all tasks",
                "Focus on one task and let the others slip"
            ],
            correct_index=1  # Prioritization is key to time management
        ),
        ScenarioQuestion(
            id=15,
            text="During a sales presentation, you realize the client is not engaged. What do you do?",
            category="adaptability",
            options=[
                "Continue with your planned presentation",
                "End the meeting early to respect their time",
                "Pause and ask questions to understand their needs better",
                "Switch to a more entertaining, high-energy presentation style"
            ],
            correct_index=2  # Adapting based on feedback
        ),
    ]
    questions.extend(scenario_questions)
    
    # Open-ended questions
    open_ended_questions = [
        OpenEndedQuestion(
            id=16,
            text="Describe a situation where you successfully persuaded someone to change their mind.",
            category="persuasion",
            min_words=50
        ),
        OpenEndedQuestion(
            id=17,
            text="How do you typically build rapport with new people you meet?",
            category="relationship_building",
            min_words=50
        ),
        OpenEndedQuestion(
            id=18,
            text="Describe your approach to learning about a new product you need to sell.",
            category="product_knowledge",
            min_words=50
        ),
    ]
    questions.extend(open_ended_questions)
    
    return questions


def get_question_by_id(question_id):
    """
    Get a specific question by ID.
    
    Args:
        question_id (int): The ID of the question to retrieve
        
    Returns:
        Question: The question object, or None if not found
    """
    questions = get_questions()
    return next((q for q in questions if q.id == question_id), None)


def get_questions_by_category(category):
    """
    Get all questions for a specific category.
    
    Args:
        category (str): The category to filter by
        
    Returns:
        list: List of Question objects in the specified category
    """
    questions = get_questions()
    return [q for q in questions if q.category == category]


def get_questions_for_test(num_questions=None, categories=None):
    """
    Get a subset of questions for a test, optionally filtered by category.
    
    Args:
        num_questions (int): Maximum number of questions to include
        categories (list): List of categories to include
        
    Returns:
        list: List of Question objects for the test
    """
    questions = get_questions()
    
    # Filter by category if specified
    if categories:
        questions = [q for q in questions if q.category in categories]
    
    # Limit number of questions if specified
    if num_questions and num_questions < len(questions):
        # This is a simple approach - a more sophisticated implementation
        # might balance questions across categories
        return questions[:num_questions]
    
    return questions 