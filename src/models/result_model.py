"""
Result model for the sales aptitude test.
"""

import datetime


class TestResult:
    """Class representing the results of a completed sales aptitude test."""
    
    def __init__(self, user_id, answers, timestamp=None):
        """
        Initialize a test result.
        
        Args:
            user_id (str): Identifier for the test taker
            answers (dict): Dictionary mapping question IDs to responses
            timestamp (datetime): When the test was completed (default: current time)
        """
        self.user_id = user_id
        self.answers = answers
        self.timestamp = timestamp or datetime.datetime.now()
        self.scores = {}
        self.analysis = {}
        self.recommendations = []
        
    def calculate_scores(self, questions):
        """
        Calculate category scores based on answers and question definitions.
        
        Args:
            questions (list): List of Question objects used in the test
        """
        # Initialize category scores
        category_scores = {}
        category_counts = {}
        
        # Process each answer
        for question_id_str, answer in self.answers.items():
            # Convert question_id to int
            try:
                question_id = int(question_id_str)
            except ValueError:
                continue
                
            # Find the corresponding question
            question = next((q for q in questions if q.id == question_id), None)
            if not question:
                continue
                
            # Initialize category if not already present
            if question.category not in category_scores:
                category_scores[question.category] = 0
                category_counts[question.category] = 0
            
            # Calculate score based on question type
            if question.type == "likert":
                # Convert Likert response to numeric value (1-5)
                likert_values = {
                    "Strongly Disagree": 1,
                    "Disagree": 2,
                    "Neutral": 3,
                    "Agree": 4,
                    "Strongly Agree": 5
                }
                
                if answer in likert_values:
                    value = likert_values[answer]
                    category_scores[question.category] += value * (question.weight or 1)
                    category_counts[question.category] += (question.weight or 1)
                    
            elif question.type == "scenario" and hasattr(question, 'correct_index') and question.correct_index is not None:
                # Score based on whether the correct option was selected
                try:
                    if hasattr(question, 'options') and question.options:
                        selected_index = question.options.index(answer)
                        if selected_index == question.correct_index:
                            category_scores[question.category] += 5 * (question.weight or 1)  # Max score for correct
                        else:
                            # Partial credit based on distance from correct answer
                            # (simplified scoring - could be more sophisticated)
                            distance = abs(selected_index - question.correct_index)
                            score = max(5 - distance, 1)  # Minimum score of 1
                            category_scores[question.category] += score * (question.weight or 1)
                        category_counts[question.category] += (question.weight or 1)
                except (ValueError, TypeError, AttributeError):
                    # Skip if answer is invalid
                    pass
            
            # For open-ended questions, assign a default score of 3 (neutral)
            elif question.type == "open_ended":
                category_scores[question.category] += 3 * (question.weight or 1)
                category_counts[question.category] += (question.weight or 1)
        
        # Calculate average scores for each category
        for category in category_scores:
            if category_counts[category] > 0:
                self.scores[category] = round(
                    category_scores[category] / category_counts[category], 2
                )
            else:
                self.scores[category] = 0
                
        # Calculate overall score (average of category scores)
        if self.scores:
            category_scores_sum = sum(score for category, score in self.scores.items())
            category_count = len(self.scores)
            if category_count > 0:
                self.scores["overall"] = round(category_scores_sum / category_count, 2)
            else:
                self.scores["overall"] = 0
        
        return self.scores
    
    def generate_analysis(self):
        """
        Generate analysis based on calculated scores.
        This is a simplified version - a real implementation would use more sophisticated algorithms.
        """
        if not self.scores:
            self.analysis = {
                "strengths": [],
                "areas_for_improvement": [],
                "overall_assessment": "No scores available for assessment."
            }
            return self.analysis
            
        # Identify strengths (categories with scores >= 4.0)
        strengths = [
            category for category, score in self.scores.items() 
            if score >= 4.0 and category != "overall"
        ]
        
        # Identify areas for improvement (categories with scores < 3.0)
        areas_for_improvement = [
            category for category, score in self.scores.items() 
            if score < 3.0 and category != "overall"
        ]
        
        # Generate recommendations based on scores
        self.recommendations = []
        
        overall_score = self.scores.get("overall", 0)
        
        if overall_score >= 4.0:
            self.recommendations.append(
                "Your profile indicates strong potential for sales roles that require relationship building."
            )
        elif overall_score >= 3.0:
            self.recommendations.append(
                "Consider roles that leverage your strengths while providing support in areas for development."
            )
        else:
            self.recommendations.append(
                "Focus on developing core sales skills through training and mentorship."
            )
            
        # Add specific recommendations based on strengths and areas for improvement
        if strengths:
            self.recommendations.append(
                f"Leverage your strengths in {', '.join(strengths)} to maximize your sales effectiveness."
            )
            
        if areas_for_improvement:
            self.recommendations.append(
                f"Focus on developing your skills in {', '.join(areas_for_improvement)} to become a more well-rounded sales professional."
            )
            
        # Store analysis
        self.analysis = {
            "strengths": strengths,
            "areas_for_improvement": areas_for_improvement,
            "overall_assessment": self._get_overall_assessment()
        }
        
        return self.analysis
    
    def _get_overall_assessment(self):
        """Generate an overall assessment based on the overall score."""
        overall_score = self.scores.get("overall", 0)
        
        if overall_score >= 4.5:
            return "Exceptional sales potential across multiple dimensions."
        elif overall_score >= 4.0:
            return "Strong sales aptitude with well-developed core skills."
        elif overall_score >= 3.5:
            return "Good sales potential with some notable strengths."
        elif overall_score >= 3.0:
            return "Moderate sales aptitude with potential for growth."
        elif overall_score >= 2.5:
            return "Some sales capabilities but significant development needed."
        else:
            return "Limited natural sales aptitude; consider roles that align with other strengths."
    
    def to_dict(self):
        """Convert test result to dictionary for JSON serialization."""
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "scores": self.scores,
            "analysis": self.analysis,
            "recommendations": self.recommendations
        } 