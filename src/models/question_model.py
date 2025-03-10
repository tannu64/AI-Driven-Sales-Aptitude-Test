"""
Question model for the sales aptitude test.
"""

class Question:
    """Base class for all question types."""
    
    def __init__(self, id, text, category, weight=1.0):
        """
        Initialize a question.
        
        Args:
            id (int): Unique identifier for the question
            text (str): The question text
            category (str): The category or trait this question measures
            weight (float): The weight of this question in scoring (default: 1.0)
        """
        self.id = id
        self.text = text
        self.category = category
        self.weight = weight
    
    def to_dict(self):
        """Convert question to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "text": self.text,
            "category": self.category,
            "weight": self.weight
        }


class LikertQuestion(Question):
    """Likert scale question (e.g., strongly disagree to strongly agree)."""
    
    def __init__(self, id, text, category, options=None, weight=1.0):
        """
        Initialize a Likert scale question.
        
        Args:
            id (int): Unique identifier for the question
            text (str): The question text
            category (str): The category or trait this question measures
            options (list): The response options (default: standard 5-point Likert scale)
            weight (float): The weight of this question in scoring (default: 1.0)
        """
        super().__init__(id, text, category, weight)
        self.type = "likert"
        self.options = options or [
            "Strongly Disagree", 
            "Disagree", 
            "Neutral", 
            "Agree", 
            "Strongly Agree"
        ]
    
    def to_dict(self):
        """Convert question to dictionary for JSON serialization."""
        question_dict = super().to_dict()
        question_dict.update({
            "type": self.type,
            "options": self.options
        })
        return question_dict


class ScenarioQuestion(Question):
    """Scenario-based question with multiple choice responses."""
    
    def __init__(self, id, text, category, options, correct_index=None, weight=1.0):
        """
        Initialize a scenario question.
        
        Args:
            id (int): Unique identifier for the question
            text (str): The scenario description
            category (str): The category or trait this question measures
            options (list): The response options
            correct_index (int): Index of the correct or best answer (if applicable)
            weight (float): The weight of this question in scoring (default: 1.0)
        """
        super().__init__(id, text, category, weight)
        self.type = "scenario"
        self.options = options
        self.correct_index = correct_index
    
    def to_dict(self):
        """Convert question to dictionary for JSON serialization."""
        question_dict = super().to_dict()
        question_dict.update({
            "type": self.type,
            "options": self.options
        })
        # Only include correct_index if it's specified
        if self.correct_index is not None:
            question_dict["correct_index"] = self.correct_index
        return question_dict


class OpenEndedQuestion(Question):
    """Open-ended question requiring a text response."""
    
    def __init__(self, id, text, category, weight=1.0, min_words=None, max_words=None):
        """
        Initialize an open-ended question.
        
        Args:
            id (int): Unique identifier for the question
            text (str): The question text
            category (str): The category or trait this question measures
            weight (float): The weight of this question in scoring (default: 1.0)
            min_words (int): Minimum word count for response (if applicable)
            max_words (int): Maximum word count for response (if applicable)
        """
        super().__init__(id, text, category, weight)
        self.type = "open_ended"
        self.min_words = min_words
        self.max_words = max_words
    
    def to_dict(self):
        """Convert question to dictionary for JSON serialization."""
        question_dict = super().to_dict()
        question_dict.update({
            "type": self.type
        })
        # Only include word limits if specified
        if self.min_words is not None:
            question_dict["min_words"] = self.min_words
        if self.max_words is not None:
            question_dict["max_words"] = self.max_words
        return question_dict 