from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from typing import List, Dict
import numpy as np

class RestaurantIntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self._train_model()
    
    def _train_model(self):
        """Train a basic restaurant intent classifier with sample data"""
        training_data = {
            'location_query': [
                "Find places to eat in New York",
                "Any good spots around Austin?",
                "Where should I eat in LA?",
                "Restaurants near me",
                "Dinner places in San Francisco"
            ],
            'cuisine_query': [
                "I want Thai food",
                "Show me Italian restaurants",
                "Where can I get sushi?",
                "Any good Indian food?",
                "Mexican cuisine near downtown"
            ],
            'diet_query': [
                "I'm vegetarian",
                "Gluten-free options please",
                "Looking for halal food",
                "I need vegan choices",
                "Dairy-free meals"
            ],
            'budget_query': [
                "Cheap eats in Chicago",
                "Fancy dining options",
                "Budget-friendly restaurants",
                "Under $20 per person",
                "Not too expensive"
            ],
            'mood_query': [
                "I want something cozy",
                "Looking for a romantic spot",
                "Trendy places to eat",
                "Chill vibe for dinner",
                "Fun ambiance"
            ]
        }

        X, y = [], []
        for intent, phrases in training_data.items():
            X.extend(phrases)
            y.extend([intent] * len(phrases))

        X_transformed = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_transformed, y)
    
    def predict(self, text: str) -> str:
        """Predict the user's restaurant-related intent"""
        try:
            X = self.vectorizer.transform([text])
            intent = self.classifier.predict(X)[0]
            return intent
        except Exception as e:
            print(f"Error predicting intent: {e}")
            return "general_query"

if __name__ == "__main__":
    classifier = RestaurantIntentClassifier()
    test_queries = [
        "Find vegan restaurants in Brooklyn",
        "Where can I get Korean BBQ?",
        "Any romantic dinner spots near me?",
        "I'm on a tight budget",
        "Show me Mexican food in Dallas"
    ]
    
    for query in test_queries:
        intent = classifier.predict(query)
        print(f"Query: {query}")
        print(f"Predicted Intent: {intent}\n")