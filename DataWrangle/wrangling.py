import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os


def convert_to_csv(file_path, output_path):
    """Convert Excel file to CSV file"""
    # Load Excel file
    df = pd.read_excel(file_path)
    
    # Save as CSV
    df.to_csv(output_path, index=False)

convert_to_csv('Datasets/Career Dataset.xlsx', 'Datasets/data.csv')
convert_to_csv('Datasets/Job opportunities.xlsx', 'Datasets/job_data.csv')

# class JobSkillsAnalyzer:
#     def __init__(self, data_folder):
#         """Initialize the analyzer with path to datasets folder"""
#         self.data_folder = data_folder
#         self.model = None
#         self.mlb = MultiLabelBinarizer()
#         self.le = LabelEncoder()
        
#     def load_and_preprocess_data(self):
#         """Load and preprocess multiple datasets from the folder"""
#         # Initialize empty lists to store combined data
#         all_skills = []
#         all_job_titles = []
        
#         # Get all CSV files from the data folder
#         csv_files = [f for f in os.listdir(self.data_folder) if f.endswith('.csv')]
        
#         for file in csv_files:
#             file_path = os.path.join(self.data_folder, file)
#             df = pd.read_csv(file_path)
            
#             # Assuming all datasets have 'skills' and 'job_title' columns
#             # Convert skills string to list if it's stored as string
            
        
#         # Convert skills to binary format
#         skills_encoded = self.mlb.fit_transform(all_skills)
        
#         # Encode job titles
#         job_titles_encoded = self.le.fit_transform(all_job_titles)
        
#         return skills_encoded, job_titles_encoded
    
#     def train_model(self):
#         """Train the Random Forest model"""
#         X, y = self.load_and_preprocess_data()
        
#         # Split the data
#         X_train, X_test, y_train, y_test = train_test_split(
#             X, y, test_size=0.2, random_state=42
#         )
        
#         # Train model
#         self.model = RandomForestClassifier(n_estimators=100, random_state=42)
#         self.model.fit(X_train, y_train)
        
#         # Evaluate model
#         y_pred = self.model.predict(X_test)
#         print(classification_report(y_test, y_pred))
        
#         return self.model
    
#     def predict_job(self, skills_list):
#         """Predict job based on input skills"""
#         if self.model is None:
#             raise ValueError("Model needs to be trained first!")
            
#         # Transform input skills
#         skills_encoded = self.mlb.transform([skills_list])
        
#         # Make prediction
#         job_encoded = self.model.predict(skills_encoded)
        
#         # Return predicted job title
#         return self.le.inverse_transform(job_encoded)[0]

# def main():
#     # Example usage
#     analyzer = JobSkillsAnalyzer('Datasets')  # Point to the Datasets folder
#     analyzer.train_model()
    
#     # Example prediction
#     skills = ['python', 'machine learning', 'data analysis']
#     predicted_job = analyzer.predict_job(skills)
#     print(f"Recommended job based on skills: {predicted_job}")

# if __name__ == "__main__":
#     main()
