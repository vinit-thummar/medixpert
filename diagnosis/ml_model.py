import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.symptom_encoder = LabelEncoder()
        self.disease_encoder = LabelEncoder()
        self.symptoms_list = []
        
    def create_sample_data(self):
        """Create sample training data for demonstration"""
        # Sample symptoms and diseases data
        symptoms_data = [
            # Common Cold
            ['fever', 'cough', 'runny_nose', 'sore_throat', 'headache'],
            ['cough', 'runny_nose', 'sneezing', 'fatigue'],
            ['fever', 'sore_throat', 'headache', 'body_ache'],
            
            # Flu
            ['high_fever', 'severe_headache', 'body_ache', 'fatigue', 'cough'],
            ['fever', 'chills', 'body_ache', 'headache', 'weakness'],
            ['high_fever', 'severe_body_ache', 'headache', 'dry_cough'],
            
            # Diabetes
            ['excessive_thirst', 'frequent_urination', 'fatigue', 'blurred_vision'],
            ['increased_hunger', 'weight_loss', 'fatigue', 'frequent_urination'],
            ['excessive_thirst', 'slow_healing', 'fatigue', 'blurred_vision'],
            
            # Hypertension
            ['headache', 'dizziness', 'chest_pain', 'shortness_of_breath'],
            ['severe_headache', 'nosebleed', 'fatigue', 'vision_problems'],
            ['headache', 'dizziness', 'irregular_heartbeat'],
            
            # Migraine
            ['severe_headache', 'nausea', 'sensitivity_to_light', 'vomiting'],
            ['throbbing_headache', 'nausea', 'sensitivity_to_sound'],
            ['severe_headache', 'visual_disturbances', 'nausea'],
            
            # Gastritis
            ['stomach_pain', 'nausea', 'vomiting', 'loss_of_appetite'],
            ['burning_stomach_pain', 'bloating', 'nausea', 'heartburn'],
            ['stomach_pain', 'indigestion', 'nausea', 'vomiting'],
            
            # Asthma
            ['shortness_of_breath', 'wheezing', 'chest_tightness', 'cough'],
            ['difficulty_breathing', 'wheezing', 'chest_pain', 'fatigue'],
            ['shortness_of_breath', 'persistent_cough', 'chest_tightness'],
            
            # Pneumonia
            ['fever', 'cough_with_phlegm', 'chest_pain', 'shortness_of_breath'],
            ['high_fever', 'chills', 'cough', 'difficulty_breathing'],
            ['fever', 'productive_cough', 'chest_pain', 'fatigue'],
        ]
        
        diseases = [
            'Common Cold', 'Common Cold', 'Common Cold',
            'Influenza', 'Influenza', 'Influenza',
            'Diabetes', 'Diabetes', 'Diabetes',
            'Hypertension', 'Hypertension', 'Hypertension',
            'Migraine', 'Migraine', 'Migraine',
            'Gastritis', 'Gastritis', 'Gastritis',
            'Asthma', 'Asthma', 'Asthma',
            'Pneumonia', 'Pneumonia', 'Pneumonia',
        ]
        
        # Get all unique symptoms
        all_symptoms = set()
        for symptom_list in symptoms_data:
            all_symptoms.update(symptom_list)
        
        self.symptoms_list = sorted(list(all_symptoms))
        
        # Create feature matrix
        X = []
        for symptom_list in symptoms_data:
            features = [1 if symptom in symptom_list else 0 for symptom in self.symptoms_list]
            X.append(features)
        
        return np.array(X), np.array(diseases)
    
    def train_model(self):
        """Train the disease prediction model"""
        X, y = self.create_sample_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Test accuracy
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.2f}")
        
        return self.model
    
    def predict_disease(self, symptoms):
        """Predict disease based on symptoms"""
        if self.model is None:
            self.train_model()
        
        # Convert symptoms to feature vector
        features = [1 if symptom in symptoms else 0 for symptom in self.symptoms_list]
        features = np.array(features).reshape(1, -1)
        
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = max(probabilities)
        
        return {
            'predicted_disease': prediction,
            'confidence': confidence,
            'all_probabilities': dict(zip(self.model.classes_, probabilities))
        }
    
    def get_available_symptoms(self):
        """Get list of available symptoms"""
        if not self.symptoms_list:
            self.create_sample_data()
        return self.symptoms_list
    
    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'symptoms_list': self.symptoms_list
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Load a trained model"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.symptoms_list = model_data['symptoms_list']
            return True
        return False

# Global predictor instance
predictor = DiseasePredictor()

def get_predictor():
    """Get the global predictor instance"""
    return predictor

