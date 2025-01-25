import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder

# GeoData
def wrangle_geodata(df):
    """Clean US geographical coordinates data"""
    # Handle missing coordinates
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].fillna(0)
    
    # Convert FIPS code to standardized string format
    df['FIPSCode'] = df['FIPSCode'].astype(str).str.zfill(5)
    
    # Clean ZipCode+4 format and deduplicate
    df['ZipCodePlus4'] = df['ZipCodePlus4'].str.replace(r'\D', '', regex=True)
    df = df.drop_duplicates(subset=['ZipCodePlus4'], keep='first')
    
    return df

#Skills
def wrangle_skill_data(df):
    """Clean skills mapping data from data.csv"""
    # Normalize skill names
    skill_clean = df['Skill'].str.replace(
        r'\b(ML|AI|Ml|A\.I)\b', 'Machine Learning', flags=re.I
    )
    df['Skill'] = skill_clean.str.replace(
        r'\b(DL|Deep\s?L)\b', 'Deep Learning', flags=re.I
    )
    
    # Convert comma-separated skills to lists
    df['Skill'] = df['Skill'].str.split(r',\s*')
    
    # Filter invalid career entries
    valid_careers = ['Data Science', 'Software Development', 'AI', 'Cybersecurity']
    df = df[df['Career'].isin(valid_careers)]
    
    return df


def change_salary_range_to_usd(df):
        # Step 1: Split the range into two separate columns
    df[['Lower Bound', 'Upper Bound']] = df['Salary Range'].str.replace(r'[$,]', '', regex=True).str.split(' - ', expand=True)

    # Step 2: Convert the columns to numeric
    df['Lower Bound'] = pd.to_numeric(df['Lower Bound'])
    df['Upper Bound'] = pd.to_numeric(df['Upper Bound'])

    # Step 3: Multiply the bounds by the factor
    factor = 1.5
    df['Lower Bound'] *= factor
    df['Upper Bound'] *= factor

    # Step 4: Optionally reformat back to the original format
    df['Salary Range'] = df['Lower Bound'].astype(int).map('${:,.0f}'.format) + ' - ' + df['Upper Bound'].astype(int).map('${:,.0f}'.format)

    return df

# Data Processing
def wrangle_job_data(df):
    """Clean job posting data from job_data.csv"""
    # Convert salary ranges from GBP to USD (using approximate conversion rate of 1 GBP = 1.27 USD)
    GBP_TO_USD = 1.27
    
    # Convert salary ranges to numeric values and convert to USD
    df['Salary Range'] = df['Salary Range'].str.replace(r'[£]', '$', regex=True)
    df = change_salary_range_to_usd(df)
    df['Salary_Min'] = df['Salary Range'].str.extract(r'£(\d+),\d+').astype(float) * GBP_TO_USD * 2
    df['Salary_Max'] = df['Salary Range'].str.extract(r'£\d+,\d+ - £(\d+),\d+').astype(float) * GBP_TO_USD * 2
    df['Salary_Avg'] = (df['Salary_Min'] + df['Salary_Max']) / 2
    
    
    
    # Standardize experience levels
    exp_map = {
        'Entry-Level': 0,
        'Junior': 1,
        'Mid-Level': 2,
        'Senior': 3
    }
    df['Experience_Level'] = df['Experience Level'].map(exp_map)
    
    # Convert date posted to datetime
    df['Date Posted'] = pd.to_datetime(df['Date Posted'])
    
    return df

#Transitions
def wrangle_transitions(df):
    """Clean career transitions data from Dashboard_transitions_dataset.csv"""
    # Clean SOC codes
    df['SOCCode'] = df['SOCCode'].astype(str)
    df['TransitionSOCCode'] = df['TransitionSOCCode'].astype(str)
    
    # Calculate wage change metrics
    df['WageChangePercent'] = (df['TransitionWageChange'] / 100)
    
    # Create transition direction flags
    df['TransitionDirection'] = np.select(
        [
            df['TransitionWageDirection'] == 1,
            df['TransitionWageDirection'] == 0,
            df['TransitionWageDirection'] == -1
        ],
        ['Up', 'Lateral', 'Down'],
        default='Unknown'
    )
    
    return df

#Trajectories
def wrangle_trajectories(df):
    """Clean career trajectory data from Trajectories-10-years-dataset.csv"""
    # Convert demographic flags to integers
    demo_cols = ['woman', 're_hispanic', 're_blackNH', 're_whiteNH', 're_otherNH']
    df[demo_cols] = df[demo_cols].fillna(0).astype(int)
    
    # Calculate wage changes
    df['wage_change'] = df['wage_119cap'] - df['wage_0cap']
    df['wage_change_pct'] = (df['wage_change'] / df['wage_0cap']) * 100
    
    # Create education transition flags
    df['education_improved'] = np.where(
        (df['educBA_119'] > df['educBA_0']) |
        (df['educAA_119'] > df['educAA_0']),
        1, 0
    )
    
    return df

#CPS-SIPP
def wrangle_cps_sipp(df):
    """Clean CPS-SIPP employment survey data"""
    # Convert wage columns to numeric
    wage_cols = ['wage_SRCE', 'wage_DEST', 'medhrlywage_SRCE', 'medhrlywage_DEST']
    df[wage_cols] = df[wage_cols].apply(pd.to_numeric, errors='coerce')
    
    # Handle demographic data
    demo_cols = ['raceeth_whiteNH', 'raceeth_blackNH', 'raceeth_Hispanic']
    df[demo_cols] = df[demo_cols].fillna(0).astype(int)
    
    # Create transition success metric
    df['TransitionSuccess'] = np.where(
        (df['wage_DEST'] > df['wage_SRCE']) & 
        (df['jobzone_DEST'] >= df['jobzone_SRCE']), 1, 0
    )
    
    return df

# Main Model
class JobSkillsAnalyzer:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.skills_encoder = MultiLabelBinarizer()
        self.job_encoder = LabelEncoder()
        
    def load_data(self):
        """Load and clean all datasets"""
        # Load skills data
        skills_df = pd.read_csv(f'{self.data_folder}/data.csv')
        self.skills_df = wrangle_skill_data(skills_df)
        print(self.skills_df.head())
        
        # Load job postings
        jobs_df = pd.read_csv(f'{self.data_folder}/job_data.csv')
        self.jobs_df = wrangle_job_data(jobs_df)
        print(self.jobs_df.head())
        
        # Load career transitions
        transitions_df = pd.read_csv(f'{self.data_folder}/Dashboard_transitions_dataset.csv')
        self.transitions_df = wrangle_transitions(transitions_df)
        print(self.transitions_df.head())
        
        # Load longitudinal data
        trajectories_df = pd.read_csv(f'{self.data_folder}/Trajectories-10-years-dataset.csv')
        self.trajectories_df = wrangle_trajectories(trajectories_df)
        print(self.trajectories_df.head())
        
        # Load employment survey data
        employment_df = pd.read_csv(f'{self.data_folder}/CPS-SIPP_dataset.csv')
        self.employment_df = wrangle_cps_sipp(employment_df)
        print(self.employment_df.head())
        
        return self
    
    def analyze_career_paths(self):
        """Analyze career transition patterns and success rates"""
        # Implement career path analysis using cleaned datasets
        pass
    
    def predict_next_job(self, current_job, skills):
        """Predict potential next career move based on current job and skills"""
        # Implement job prediction logic using cleaned datasets
        pass
    
    def get_skill_recommendations(self, target_job):
        """Get recommended skills for a target job"""
        # Implement skill recommendation logic using cleaned datasets
        pass

def main():
    """Main execution function"""
    analyzer = JobSkillsAnalyzer("Datasets/")
    analyzer.load_data()
    # Add main processing logic here
    
if __name__ == "__main__":
    main()