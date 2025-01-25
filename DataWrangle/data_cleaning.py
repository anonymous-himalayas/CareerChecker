import pandas as pd
import numpy as np
import re

def wrangle_geodata(df):
    """Clean and transform US geographical data"""
    # Handle missing coordinates
    df[['Latitude', 'Longitude']] = df[['Latitude', 'Longitude']].fillna(0)
    
    # Convert FIPS code to string with padding
    df['FIPSCode'] = df['FIPSCode'].astype(str).str.zfill(5)
    
    # Deduplicate based on ZipCode+4
    df = df.drop_duplicates(subset=['ZipCodePlus4'], keep='first')
    
    return df

def wrangle_skill_data(df):
    """Process skills and career mapping data"""
    # Normalize skill names
    df['Skill'] = df['Skill'].str.replace(r'\b(deepe?learning)\b', 'Deep Learning', flags=re.I)
    
    # Split comma-separated skills into lists
    df['Skill'] = df['Skill'].str.split(',\s*')
    
    # Filter out invalid career entries
    valid_careers = ['Development', 'Data Science', 'Artificial Intelligence', 
                    'Software Development and Engineering', 'Security']
    df = df[df['Career'].isin(valid_careers)]
    
    return df

def wrangle_job_data(df):
    """Clean job postings data"""
    # Convert salary ranges to numerical values
    df[['Salary_Low', 'Salary_High']] = df['Salary Range'].str.extract(r'£([\d,]+)\s*-\s*£([\d,]+)')
    df[['Salary_Low', 'Salary_High']] = df[['Salary_Low', 'Salary_High']].replace('[\£,]', '', regex=True).astype(float)
    
    # Standardize location format
    df['Location'] = df['Location'].str.title().str.replace(r'\s+', ' ', regex=True)
    
    # Handle missing experience levels
    df['Experience Level'] = df['Experience Level'].fillna('Not Specified')
    
    return df

def wrangle_transitions(df):
    """Process career transition dataset"""
    # Convert wage change to percentage
    df['Wage_Change_Pct'] = df['TransitionWageChange'] / df['TransitionWageChange'].abs().max()
    
    # Create transition type flag
    df['Transition_Type'] = np.where(df['TransitionWageDirection'] == 1, 'Upward', 
                                    np.where(df['TransitionWageDirection'] == -1, 'Downward', 'Lateral'))
    
    # Filter valid SOC codes
    df = df[df['SOCCode'].str.match(r'\d{2}-\d{4}')]
    
    return df

def wrangle_trajectories(df):
    """Process 10-year career trajectories"""
    # Convert wage columns to numeric
    wage_cols = ['wage_0cap', 'wage_119cap', 'abswagech10']
    df[wage_cols] = df[wage_cols].apply(pd.to_numeric, errors='coerce')
    
    # Create career stability metric
    df['Career_Stability'] = df['totjobcount'] / df['totmosUnemp10cap'].replace(0, 1)
    
    # Encode categorical features
    sector_dummies = pd.get_dummies(df['startingsector'], prefix='sector')
    df = pd.concat([df, sector_dummies], axis=1)
    
    return df

def wrangle_cps_sipp(df):
    """Clean CPS-SIPP employment data"""
    # Convert wage columns
    wage_cols = ['wage_SRCE', 'wage_DEST', 'medhrlywage_SRCE', 'medhrlywage_DEST']
    df[wage_cols] = df[wage_cols].apply(pd.to_numeric, errors='coerce')
    
    # Create transition flags
    df['sector_transition'] = np.where(df['sector_SRCE'] == df['sector_DEST'], 1, 0)
    df['zone_transition'] = (df['jobzone_DEST'] - df['jobzone_SRCE']).clip(-1, 1)
    
    # Handle missing demographic data
    demo_cols = ['raceeth_whiteNH', 'raceeth_blackNH', 'raceeth_Hispanic']
    df[demo_cols] = df[demo_cols].fillna(0)
    
    return df