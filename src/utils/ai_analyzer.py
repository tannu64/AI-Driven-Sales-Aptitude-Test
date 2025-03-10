"""
AI-based analysis utilities for the sales aptitude test.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResponseAnalyzer:
    """Class for analyzing test responses using AI techniques."""
    
    def __init__(self):
        """Initialize the response analyzer."""
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Sample positive responses for each category (would be expanded in a real implementation)
        self.reference_responses = {
            "relationship_building": [
                "I focus on finding common interests and asking thoughtful questions.",
                "I make sure to remember personal details and follow up on previous conversations.",
                "I try to be authentic and show genuine interest in the other person."
            ],
            "persuasion": [
                "I present clear benefits and address objections directly.",
                "I use stories and examples to illustrate my points.",
                "I focus on understanding their needs first, then align my proposal with those needs."
            ],
            "product_knowledge": [
                "I study all product documentation thoroughly and practice explaining features.",
                "I use the product myself to understand its strengths and limitations.",
                "I talk to existing customers about their experience with the product."
            ]
        }
        
        # Vectorize reference responses
        self.reference_vectors = {}
        for category, responses in self.reference_responses.items():
            self.reference_vectors[category] = self.vectorizer.fit_transform(responses)
    
    def analyze_open_ended_response(self, response, category):
        """
        Analyze an open-ended response using NLP techniques.
        
        Args:
            response (str): The user's response text
            category (str): The category being assessed
            
        Returns:
            float: A score between 1 and 5 representing the quality of the response
        """
        if not response or category not in self.reference_vectors:
            return 3.0  # Default neutral score
        
        # Vectorize the response
        response_vector = self.vectorizer.transform([response])
        
        # Calculate similarity to reference responses
        similarities = cosine_similarity(response_vector, self.reference_vectors[category])
        
        # Take the maximum similarity
        max_similarity = np.max(similarities)
        
        # Convert similarity to a score between 1 and 5
        # Similarity ranges from 0 to 1, so we scale to 1-5
        score = 1 + max_similarity * 4
        
        return round(score, 2)
    
    def analyze_response_patterns(self, answers):
        """
        Analyze patterns in responses to detect inconsistencies or response biases.
        
        Args:
            answers (dict): Dictionary of question IDs to responses
            
        Returns:
            dict: Analysis results including consistency score and detected patterns
        """
        # This is a placeholder for more sophisticated analysis
        # In a real implementation, this would look for patterns like:
        # - Extreme response bias (all 5s or all 1s)
        # - Inconsistent responses to similar questions
        # - Response patterns that suggest social desirability bias
        
        # Simple implementation: check for variety in responses
        likert_responses = [
            ans for ans in answers.values() 
            if isinstance(ans, str) and ans in ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        ]
        
        if likert_responses:
            unique_responses = len(set(likert_responses))
            variety_score = min(unique_responses / 3, 1.0)  # At least 3 different responses for full score
        else:
            variety_score = 1.0
            
        return {
            "consistency_score": round(variety_score * 5, 2),
            "patterns_detected": ["Limited response variety"] if variety_score < 0.7 else []
        }
    
    def generate_personalized_feedback(self, scores, analysis):
        """
        Generate personalized feedback based on test results.
        
        Args:
            scores (dict): Category scores
            analysis (dict): Analysis results
            
        Returns:
            dict: Personalized feedback including strengths, areas for improvement, and recommendations
        """
        feedback = {
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Generate feedback based on scores
        for category, score in scores.items():
            if category == "overall":
                continue
                
            if score >= 4.0:
                feedback["strengths"].append(self._get_strength_feedback(category))
            elif score < 3.0:
                feedback["areas_for_improvement"].append(self._get_improvement_feedback(category))
                
        # Add recommendations based on overall profile
        overall_score = scores.get("overall", 0)
        if overall_score >= 4.0:
            feedback["recommendations"].append(
                "Your profile indicates strong potential for consultative sales roles that require relationship building and problem-solving."
            )
        elif overall_score >= 3.0:
            feedback["recommendations"].append(
                "Consider roles that leverage your strengths while providing training in your development areas."
            )
        else:
            feedback["recommendations"].append(
                "Focus on developing your core sales skills through structured training programs and mentorship."
            )
            
        return feedback
    
    def _get_strength_feedback(self, category):
        """Generate feedback for a strength category."""
        feedback_templates = {
            "relationship_building": "You excel at building relationships, which is fundamental to sales success.",
            "resilience": "Your resilience will help you handle rejection and persist through sales challenges.",
            "persuasion": "You demonstrate strong persuasion skills, helping you influence customer decisions.",
            "listening": "Your active listening skills allow you to understand customer needs effectively.",
            "problem_solving": "You're skilled at problem-solving, which helps in creating value for customers.",
            "goal_orientation": "Your goal orientation will drive consistent sales performance.",
            "adaptability": "Your adaptability allows you to adjust your approach based on customer needs.",
            "product_knowledge": "You prioritize product knowledge, which builds credibility with customers.",
            "negotiation": "Your negotiation skills help you close deals while maintaining relationships.",
            "time_management": "Your time management skills enable you to maximize productivity."
        }
        
        return feedback_templates.get(category, f"You show strength in {category}.")
    
    def _get_improvement_feedback(self, category):
        """Generate feedback for an area needing improvement."""
        feedback_templates = {
            "relationship_building": "Work on developing your relationship-building skills by practicing active networking.",
            "resilience": "Develop resilience by reframing rejection as a learning opportunity rather than a personal failure.",
            "persuasion": "Enhance your persuasion skills by studying successful sales conversations and practicing your pitch.",
            "listening": "Improve active listening by focusing completely on the customer before formulating your response.",
            "problem_solving": "Strengthen your problem-solving by analyzing customer challenges more deeply before offering solutions.",
            "goal_orientation": "Develop your goal orientation by setting specific, measurable sales targets and tracking progress.",
            "adaptability": "Work on adaptability by preparing multiple approaches for different customer scenarios.",
            "product_knowledge": "Deepen your product knowledge through regular study and hands-on experience with your offerings.",
            "negotiation": "Improve negotiation skills by preparing thoroughly and focusing on value rather than price.",
            "time_management": "Enhance time management by prioritizing high-value activities and reducing distractions."
        }
        
        return feedback_templates.get(category, f"Focus on developing your skills in {category}.") 