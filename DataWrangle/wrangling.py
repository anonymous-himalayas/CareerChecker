import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os


# def convert_to_csv(file_path, output_path):
#     """Convert Excel file to CSV file"""
#     # Load Excel file
#     df = pd.read_excel(file_path)
    
#     # Save as CSV
#     df.to_csv(output_path, index=False)

# convert_to_csv('Datasets/Career Dataset.xlsx', 'Datasets/data.csv')
# convert_to_csv('Datasets/Job opportunities.xlsx', 'Datasets/job_data.csv')

class JobSkillsAnalyzer:
    def __init__(self, data_folder):
        """Initialize the analyzer with path to datasets folder"""
        self.data_folder = data_folder
        self.model = None
        self.mlb_skills = MultiLabelBinarizer()
        self.mlb_interests = MultiLabelBinarizer()
        self.le_location = LabelEncoder()
        self.le_job = LabelEncoder()
        
    def load_and_preprocess_data(self):
        """Load and preprocess multiple datasets from the folder"""
        # Initialize empty lists to store combined data
        all_skills = []
        all_interests = []
        all_locations = []
        all_job_titles = []
        
        # Get all CSV files from the data folder
        csv_files = [f for f in os.listdir(self.data_folder) if f.endswith('.csv')]
        
        for file in csv_files:
            file_path = os.path.join(self.data_folder, file)
            df = pd.read_csv(file_path)
            
            # Assuming datasets have 'skills', 'interests', 'location', and 'job_title' columns
            # Convert string representations to lists if needed
            skills = [eval(s) if isinstance(s, str) else s for s in df['skills']]
            interests = [eval(i) if isinstance(i, str) else i for i in df['interests']]
            
            all_skills.extend(skills)
            all_interests.extend(interests)
            all_locations.extend(df['location'])
            all_job_titles.extend(df['job_title'])
        
        # Transform features
        skills_encoded = self.mlb_skills.fit_transform(all_skills)
        interests_encoded = self.mlb_interests.fit_transform(all_interests)
        locations_encoded = self.le_location.fit_transform(all_locations)
        
        # Combine features
        X = np.hstack([
            skills_encoded,
            interests_encoded,
            locations_encoded.reshape(-1, 1)
        ])
        
        # Encode job titles
        y = self.le_job.fit_transform(all_job_titles)
        
        return X, y
    
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
    
    def predict_job(self, skills_list, interests_list, location):
        """Predict job based on input skills, interests, and location"""
        if self.model is None:
            raise ValueError("Model needs to be trained first!")
            
        # Transform input features
        skills_encoded = self.mlb_skills.transform([skills_list])
        interests_encoded = self.mlb_interests.transform([interests_list])
        location_encoded = self.le_location.transform([location]).reshape(1, -1)
        
        # Combine features
        X = np.hstack([skills_encoded, interests_encoded, location_encoded])
        
        # Make prediction
        job_encoded = self.model.predict(X)
        
        # Return predicted job title
        return self.le_job.inverse_transform(job_encoded)[0]

    def get_technology_roadmap(self, predicted_job):
        """Generate a technology roadmap based on the predicted job"""
        # Define technology roadmaps for different job roles
        roadmaps = {
            'Web Developer': {
                'Fundamentals': ['HTML', 'CSS', 'JavaScript'],
                'Frontend': ['React.js', 'Vue.js', 'TypeScript'],
                'Backend': ['Node.js', 'Express.js', 'MongoDB'],
                'Additional': ['Git', 'REST APIs', 'Web Security']
            },
            'Data Analyst': {
                'Fundamentals': ['Python', 'SQL', 'Statistics'],
                'Data Processing': ['Pandas', 'NumPy', 'Excel'],
                'Visualization': ['Tableau', 'Power BI', 'Matplotlib'],
                'Additional': ['Machine Learning Basics', 'Data Cleaning', 'Big Data Tools']
            },
            'Software Developer': {
                'Fundamentals': ['Python', 'Java', 'Data Structures'],
                'Development': ['OOP', 'Design Patterns', 'APIs'],
                'Tools': ['Git', 'Docker', 'CI/CD'],
                'Additional': ['System Design', 'Testing', 'Agile Methodologies']
            },
            'Data Scientist': {
                'Fundamentals': ['Python', 'SQL', 'Statistics'],
                'Machine Learning': ['Scikit-learn', 'TensorFlow', 'PyTorch'],
                'Data Visualization': ['Matplotlib', 'Seaborn', 'Plotly'],
                'Additional': ['Data Wrangling', 'Big Data', 'Cloud Computing']
            },
            'Cybersecurity Engineer': {
                'Fundamentals': ['Cybersecurity Basics', 'Network Security', 'Ethical Hacking'],
                'Tools': ['Wireshark', 'Nmap', 'Kali Linux'],
                'Additional': ['Penetration Testing', 'Security Audits', 'Compliance Standards']
            }
        }
        
        return roadmaps.get(predicted_job, "Roadmap not available for this job role")

def main():
    # Example usage
    analyzer = JobSkillsAnalyzer('Datasets')  # Point to the Datasets folder
    analyzer.train_model()
    
    # Example prediction
    skills = ['python', 'machine learning', 'data analysis']
    interests = ['data science', 'machine learning']
    location = 'New York'
    predicted_job = analyzer.predict_job(skills, interests, location)
    print(f"Recommended job based on skills, interests, and location: {predicted_job}")

    # Get technology roadmap
    roadmap = analyzer.get_technology_roadmap(predicted_job)
    print(f"Technology roadmap for {predicted_job}:")
    for category, technologies in roadmap.items():
        print(f"{category}:")
        for technology in technologies:
            print(f"  - {technology}")

if __name__ == "__main__":
    main()
