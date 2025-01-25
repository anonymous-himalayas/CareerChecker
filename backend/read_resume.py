import os
from groq import Groq
import json
from typing import Dict, List

# Load the GROQ API key from the .env file
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def read_resume_with_groq(resume_text: str) -> Dict:
    """Analyze resume text using Groq API"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Please analyze this resume text and extract the following information in JSON format:
    
    Resume text:
    {resume_text}
    
    Please extract:
    1. All technical skills and technologies
    2. Soft skills
    3. Work experience summary
    4. Education background
    5. Project highlights
    
    Format the response as a JSON object with these keys:
    - technical_skills: [list of technical skills]
    - soft_skills: [list of soft skills]
    - experience: [list of work experiences]
    - education: [list of educational qualifications]
    - projects: [list of significant projects]
    
    Be specific and concise in the extraction.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are an expert at analyzing resumes and extracting relevant skills and experiences."
            }, {
                "role": "user",
                "content": prompt
            }],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=2000
        )
        
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error in Groq resume analysis: {str(e)}")
        return None

def extract_skills(resume_analysis: Dict) -> List[str]:
    """Extract all skills from the resume analysis"""
    if not resume_analysis:
        return []
    
    skills = set()
    
    # Add technical skills
    if 'technical_skills' in resume_analysis:
        skills.update(resume_analysis['technical_skills'])
    
    # Add relevant soft skills
    if 'soft_skills' in resume_analysis:
        skills.update(resume_analysis['soft_skills'])
    
    # Extract skills mentioned in projects
    if 'projects' in resume_analysis:
        for project in resume_analysis['projects']:
            if isinstance(project, str):
                # Extract any technical terms that might be skills
                technical_terms = [word for word in project.split() 
                                 if word[0].isupper() or 
                                 any(tech in word.lower() for tech in ['python', 'java', 'sql', 'aws', 'azure'])]
                skills.update(technical_terms)
    
    return list(skills)

# Example usage
resume_text = "Your resume text here"
groq_response = read_resume_with_groq(resume_text)
print(groq_response)