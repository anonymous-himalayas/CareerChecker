import os
from groq import Groq
import json
from typing import Dict, List
from dotenv import main
main.load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def read_resume_with_groq(resume_text: str) -> Dict:
    """Analyze resume text using Groq API"""
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Please analyze this resume text and extract the following information in JSON format:
    
    Resume text:
    {resume_text}
    
    Please extract:
    1. All technical skills and technologies (programming languages, frameworks, tools)
    2. Soft skills (communication, leadership, etc.)
    3. Work experience summary
    4. Education background
    5. Project highlights
    
    Format the response STRICTLY as a JSON object with these keys and lists of strings as values:
    {{
        "technical_skills": ["skill1", "skill2"],
        "soft_skills": ["skill1", "skill2"],
        "experience": ["exp1", "exp2"],
        "education": ["edu1", "edu2"],
        "projects": ["project1", "project2"]
    }}
    
    Make sure all skills are individual strings and not descriptions.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": """You are an expert at analyzing resumes and extracting relevant skills and experiences with many
                  years of experience under your belt. Always return valid JSON."""
            }, {
                "role": "user",
                "content": prompt
            }],
            model="mixtral-8x7b-32768",
            temperature=0.1,
            max_tokens=2000
        )
        
        # JSON
        response_text = completion.choices[0].message.content.strip()
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {response_text}")
            return None
            
    except Exception as e:
        print(f"Error in Groq resume analysis: {str(e)}")
        return None

def extract_skills(resume_analysis: Dict) -> List[str]:
    """Skills"""
    if not resume_analysis:
        return []
    
    skills = set()
    
    # Technical
    if 'technical_skills' in resume_analysis:
        skills.update(skill.strip() for skill in resume_analysis['technical_skills'])
    
    # Soft
    if 'soft_skills' in resume_analysis:
        skills.update(skill.strip() for skill in resume_analysis['soft_skills'])
    
    # Project
    if 'projects' in resume_analysis:
        for project in resume_analysis['projects']:
            if isinstance(project, str):
                # Issue
                technical_terms = [word.strip() for word in project.split() 
                                 if word[0].isupper() or 
                                 any(tech in word.lower() for tech in [
                                     'python', 'java', 'sql', 'aws', 'azure', 'javascript',
                                     'pandas', 'apis', 'react', 'node.js', 'express.js', 'docker', 'kubernetes',
                                        'html', 'css', 'git', 'github', 'linux', 'unix', 'bash',
                                        'api', 'rest', 'graphql', 'sqlalchemy', 'flask', 'django',
                                        'fastapi', 'numpy', 'pandas', 'scipy', 'scikit-learn',
                                        'tensorflow', 'keras', 'pytorch', 'opencv', 'nltk',
                                        'R', 'Rust', 'C++', 'C#', 'Java', 'Scala', 'Go', 'Ruby'
                                 ])]
                skills.update(technical_terms)
    
    skills.discard('')
    
    return list(skills)


# resume_text = "Your resume text here"
# groq_response = read_resume_with_groq(resume_text)
# print(groq_response)