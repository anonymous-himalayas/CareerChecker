import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

class JobSkillsAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with path to dataset"""
        self.data_path = data_path
        self.model = None
        self.mlb = MultiLabelBinarizer()
        self.le = LabelEncoder()
        self.careerData = pd.read_excel("Datasets\Career Dataset.xlsx")
        
    def load_and_preprocess_data(self):
        """Load and preprocess the dataset"""
        # Load your dataset
        df = pd.read_csv(self.data_path)
        
        # Assuming your dataset has columns: 'skills' and 'job_title'
        # Convert skills string to list if it's stored as string
        if isinstance(df['skills'].iloc[0], str):
            df['skills'] = df['skills'].apply(lambda x: x.split(','))
            
        # Convert skills to binary format
        skills_encoded = self.mlb.fit_transform(df['skills'])
        
        # Encode job titles
        job_titles_encoded = self.le.fit_transform(df['job_title'])
        
        return skills_encoded, job_titles_encoded
    
    def train_model(self):
        """Train the Random Forest model"""
        X, y = self.load_and_preprocess_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        
        return self.model
    
    def predict_job(self, skills_list):
        """Predict job based on input skills"""
        if self.model is None:
            raise ValueError("Model needs to be trained first!")
            
        # Transform input skills
        skills_encoded = self.mlb.transform([skills_list])
        
        # Make prediction
        job_encoded = self.model.predict(skills_encoded)
        
        # Return predicted job title
        return self.le.inverse_transform(job_encoded)[0]

def main():
    # Example usage
    analyzer = JobSkillsAnalyzer('path_to_your_dataset.csv')
    analyzer.train_model()
    
    # Example prediction
    skills = ['python', 'machine learning', 'data analysis']
    predicted_job = analyzer.predict_job(skills)
    print(f"Recommended job based on skills: {predicted_job}")

if __name__ == "__main__":
    main()
