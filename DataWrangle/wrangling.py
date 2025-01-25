import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder

# GeoData
def wrangle_geodata(df):
    """Clean US geographical coordinates data"""
    
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].fillna(0)
    
    # Figure out fips
    df['FIPSCode'] = df['FIPSCode'].astype(str).str.zfill(5)
    
    # 
    df['ZipCodePlus4'] = df['ZipCodePlus4'].str.replace(r'\D', '', regex=True)
    df = df.drop_duplicates(subset=['ZipCodePlus4'], keep='first')
    
    return df

#Skills
def wrangle_skill_data(df):
    """Clean skills mapping data from data.csv"""
    
    # make it ml
    skill_clean = df['Skill'].str.replace(
        r'\b(ML|AI|Ml|A\.I)\b', 'Machine Learning', flags=re.I
    )

    # deep learning/neural netorks
    df['Skill'] = skill_clean.str.replace(
        r'\b(DL|Deep\s?L)\b', 'Deep Learning', flags=re.I
    )
    
    # SKill
    df['Skill'] = df['Skill'].str.split(r',\s*')
    
    # Data
    valid_careers = ['Data Science', 'Software Development', 'AI', 'Cybersecurity']
    df = df[df['Career'].isin(valid_careers)]
    
    return df


def change_salary_range_to_usd(df):
    # pounds
    df[['Lower Bound', 'Upper Bound']] = df['Salary Range'].str.replace(r'[$,]', '', regex=True).str.split(' - ', expand=True)
    df['Lower Bound'] = pd.to_numeric(df['Lower Bound'])
    df['Upper Bound'] = pd.to_numeric(df['Upper Bound'])
    df['Lower Bound'] *= 1.5
    df['Upper Bound'] *= 1.5

    # Test
    df['Salary Range'] = df['Lower Bound'].astype(int).map('${:,.0f}'.format) + ' - ' + df['Upper Bound'].astype(int).map('${:,.0f}'.format)

    return df

# Data Processing
def wrangle_job_data(df):
    """job_data.csv"""
    
    GBP_TO_USD = 1.27
    
    # british
    df['Salary Range'] = df['Salary Range'].str.replace(r'[£]', '$', regex=True)
    df = change_salary_range_to_usd(df)
    df['Salary_Min'] = df['Salary Range'].str.extract(r'£(\d+),\d+').astype(float) * GBP_TO_USD * 2
    df['Salary_Max'] = df['Salary Range'].str.extract(r'£\d+,\d+ - £(\d+),\d+').astype(float) * GBP_TO_USD * 2
    df['Salary_Avg'] = (df['Salary_Min'] + df['Salary_Max']) / 2
    
    
    
    # Change Exp level
    exp_map = {
        'Entry-Level': 0,
        'Junior': 1,
        'Mid-Level': 2,
        'Senior': 3
    }
    df['Experience_Level'] = df['Experience Level'].map(exp_map)
    df['Date Posted'] = pd.to_datetime(df['Date Posted'])
    
    return df

#Transitions
def wrangle_transitions(df):
    """Dashboard_transitions_dataset.csv"""
    # The Standard Occupational Classification (SOC) System is a United States government system for classifying occupations. 
    # It is used by U.S. federal government agencies collecting occupational data, enabling comparison of occupations across data sets
    df['SOCCode'] = df['SOCCode'].astype(str)
    df['TransitionSOCCode'] = df['TransitionSOCCode'].astype(str)
    df['WageChangePercent'] = (df['TransitionWageChange'] / 100)
    
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
    """Trajectories-10-years-dataset.csv"""

    demo_cols = ['woman', 're_hispanic', 're_blackNH', 're_whiteNH', 're_otherNH']
    df[demo_cols] = df[demo_cols].fillna(0).astype(int)
    
    df['wage_change'] = df['wage_119cap'] - df['wage_0cap']
    df['wage_change_pct'] = (df['wage_change'] / df['wage_0cap']) * 100
    
    df['education_improved'] = np.where(
        (df['educBA_119'] > df['educBA_0']) |
        (df['educAA_119'] > df['educAA_0']),
        1, 0
    )
    
    return df

#CPS-SIPP
def wrangle_cps_sipp(df):
    """cps-sipp_dataset.csv"""

    wage_cols = ['wage_SRCE', 'wage_DEST', 'medhrlywage_SRCE', 'medhrlywage_DEST']
    df[wage_cols] = df[wage_cols].apply(pd.to_numeric, errors='coerce')

    demo_cols = ['raceeth_whiteNH', 'raceeth_blackNH', 'raceeth_Hispanic']
    df[demo_cols] = df[demo_cols].fillna(0).astype(int)
    
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
        """all datasets"""

        skills_df = pd.read_csv(f'{self.data_folder}/data.csv')
        self.skills_df = wrangle_skill_data(skills_df)
        # print(self.skills_df.head())
        
        jobs_df = pd.read_csv(f'{self.data_folder}/job_data.csv')
        self.jobs_df = wrangle_job_data(jobs_df)
        # print(self.jobs_df.head())
        
        transitions_df = pd.read_csv(f'{self.data_folder}/Dashboard_transitions_dataset.csv')
        self.transitions_df = wrangle_transitions(transitions_df)
        # print(self.transitions_df.head())
        
        trajectories_df = pd.read_csv(f'{self.data_folder}/Trajectories-10-years-dataset.csv')
        self.trajectories_df = wrangle_trajectories(trajectories_df)
        # print(self.trajectories_df.head())
        
        employment_df = pd.read_csv(f'{self.data_folder}/CPS-SIPP_dataset.csv')
        self.employment_df = wrangle_cps_sipp(employment_df)
        # print(self.employment_df.head())
        
        return self
    
    def analyze_career_paths(self):
        """Analyze career transition patterns and success rates"""
        
        transition_analysis = {
            'success_rate': self.transitions_df['TransitionWageDirection'].mean(),
            'avg_wage_change': self.transitions_df['TransitionWageChange'].mean(),
            'common_paths': self.transitions_df.groupby(['SOCTitle', 'TransitionSOCTitle']).size().nlargest(10),
            'upward_mobility': (
                self.transitions_df[self.transitions_df['TransitionWageDirection'] == 1]
                .groupby('SOCTitle')['TransitionSOCTitle']
                .agg(list)
            )
        }
        
        # means of changes
        trajectory_analysis = {
            'avg_10yr_wage_growth': self.trajectories_df['wage_change_pct'].mean(),
            'education_impact': (
                self.trajectories_df.groupby('education_improved')['wage_change_pct'].mean()
            )
        }
        
        return {
            'transitions': transition_analysis,
            'trajectories': trajectory_analysis
        }
    
    def predict_next_job(self, current_job, skills):
        """Predict potential next career move based on current job and skills"""

        # set or list
        current_skills = set(skills)
        
        self.jobs_df['skills_set'] = self.jobs_df['Required Skills'].str.split(',').apply(set)

        # lambda now works
        self.jobs_df['skill_match'] = self.jobs_df['skills_set'].apply(
            lambda x: len(current_skills.intersection(x)) / len(current_skills.union(x))
        )
        
        similar_transitions = self.transitions_df[
            self.transitions_df['SOCTitle'].str.contains(current_job, case=False)
        ]
        
        potential_jobs = similar_transitions.merge(
            self.jobs_df[['Job Title', 'skill_match', 'Salary_Avg']],
            left_on='TransitionSOCTitle',
            right_on='Job Title',
            how='inner'
        )
        
        recommendations = potential_jobs.sort_values(
            by=['TransitionWageChange', 'skill_match'],
            ascending=[False, False]
        ).head(5)
        
        return {
            'recommended_jobs': recommendations[['Job Title', 'TransitionWageChange', 'skill_match']],
            'avg_wage_increase': recommendations['TransitionWageChange'].mean()
        }
    
    def get_skill_recommendations(self, target_job):
        """Get recommended skills for a target job"""

        target_jobs = self.jobs_df[
            self.jobs_df['Job Title'].str.contains(target_job, case=False)
        ]
        
        if target_jobs.empty:
            return {'error': 'Target job not found'}
        
        # set or list
        target_skills = set()
        for skills in target_jobs['Required Skills'].str.split(','):
            target_skills.update(skills)
        
        successful_transitions = self.transitions_df[
            (self.transitions_df['TransitionSOCTitle'].str.contains(target_job, case=False)) &
            (self.transitions_df['TransitionWageDirection'] == 1)
        ]
        
        similar_roles = self.skills_df[
            self.skills_df['Career'].str.contains(target_job, case=False)
        ]
        
        role_skills = set()
        for skills in similar_roles['Skill']:
            role_skills.update(skills)
            
        # Combine
        all_skills = target_skills.union(role_skills)
        
        # Everytyhing
        skill_scores = {}
        for skill in all_skills:
            jobs_with_skill = self.jobs_df[
                self.jobs_df['Required Skills'].str.contains(skill, case=False)
            ]
            skill_scores[skill] = {
                'frequency': len(jobs_with_skill) / len(self.jobs_df),
                'avg_salary': jobs_with_skill['Salary_Avg'].mean(),
                'in_target_requirements': skill in target_skills
            }
        
        ranked_skills = sorted(
            skill_scores.items(),
            key=lambda x: (
                x[1]['in_target_requirements'],
                x[1]['frequency'],
                x[1]['avg_salary']
            ),
            reverse=True
        )
        
        return {
            'essential_skills': [skill for skill, _ in ranked_skills[:5]],
            'recommended_skills': [skill for skill, _ in ranked_skills[5:10]],
            'skill_details': skill_scores
        }

def main():
    """Main execution function"""

    analyzer = JobSkillsAnalyzer("Datasets/")
    print("Loading and cleaning datasets...")
    analyzer.load_data()
    
    # Test career path analysis
    # print("\n1. Analyzing career transition patterns...")
    # career_analysis = analyzer.analyze_career_paths()
    # print(f"Overall transition success rate: {career_analysis['transitions']['success_rate']:.2%}")
    # print(f"Average wage change: {career_analysis['transitions']['avg_wage_change']:.2f}%")
    # print("\nTop 3 most common career transitions:")
    # print(career_analysis['transitions']['common_paths'].head(3))
    
    # # Test job prediction
    # print("\n2. Testing job prediction...")
    # current_job = "Software Engineer"
    # current_skills = ["Python", "Java", "SQL", "Machine Learning"]
    # predictions = analyzer.predict_next_job(current_job, current_skills)
    # print(f"\nTop recommended next roles for {current_job}:")
    # print(predictions['recommended_jobs'])
    # print(f"Expected average wage increase: {predictions['avg_wage_increase']:.2f}%")
    
    # # Test skill recommendations
    # print("\n3. Testing skill recommendations...")
    # target_job = "Data Scientist"
    # skill_recs = analyzer.get_skill_recommendations(target_job)
    # print(f"\nEssential skills for {target_job}:")
    # print(skill_recs['essential_skills'])
    # print(f"\nRecommended additional skills:")
    # print(skill_recs['recommended_skills'])
    

if __name__ == "__main__":
    main()