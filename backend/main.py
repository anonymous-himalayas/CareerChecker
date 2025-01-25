from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import uvicorn
import os
from datetime import datetime
import PyPDF2
import spacy
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataWrangle.wrangling import JobSkillsAnalyzer
from groq import Groq
import json
from read_resume import read_resume_with_groq, extract_skills
from dotenv import main
main.load_dotenv()


# Initialize FastAPI app
app = FastAPI()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML model
model = JobSkillsAnalyzer("Datasets/")
model.load_data()

# Load NLP model for resume parsing
nlp = spacy.load("en_core_web_sm")

# Database initialization
def init_db():
    conn = sqlite3.connect('career_advisor.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            created_at TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER,
            skills TEXT,
            location TEXT,
            resume_path TEXT,
            last_updated TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS career_recommendations (
            user_id INTEGER,
            recommended_job TEXT,
            confidence_score FLOAT,
            created_at TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Pydantic models for request/response validation
class UserBase(BaseModel):
    email: str

class UserProfile(BaseModel):
    skills: List[str]
    location: str

class CareerRecommendation(BaseModel):
    job_title: str
    confidence_score: float
    required_skills: List[str]
    learning_roadmap: dict

# Database connection context manager
class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect('career_advisor.db')
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# Update the parse_resume function
async def parse_resume(file_path: str) -> List[str]:
    """Extract skills from resume using Groq"""
    try:
        # Read PDF content
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Analyze resume with Groq
        resume_analysis = read_resume_with_groq(text)
        
        # Extract skills from the analysis
        if resume_analysis:
            skills = extract_skills(resume_analysis)
            return skills
        
        # Fallback to spaCy if Groq fails
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "PRODUCT", "ORG"]]
        
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        return []

# API Endpoints
@app.post("/users/", response_model=UserBase)
async def create_user(user: UserBase):
    with DBConnection() as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (email, created_at) VALUES (?, ?)",
                (user.email, datetime.now())
            )
            conn.commit()
            return user
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already registered")

@app.post("/profile/{user_id}")
async def update_profile(
    user_id: int,
    profile: UserProfile,
    resume: Optional[UploadFile] = File(None)
):
    with DBConnection() as conn:
        c = conn.cursor()
        
        # Handle resume upload if provided
        resume_path = None
        resume_analysis = None
        if resume:
            file_path = f"uploads/{user_id}_{resume.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as buffer:
                content = await resume.read()
                buffer.write(content)
            resume_path = file_path
            
            # Extract additional skills from resume using Groq
            resume_skills = await parse_resume(file_path)
            profile.skills.extend(resume_skills)
        
        # Update profile in database
        c.execute("""
            INSERT OR REPLACE INTO user_profiles 
            (user_id, skills, location, resume_path, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            ",".join(set(profile.skills)),  # Remove duplicates
            profile.location,
            resume_path,
            datetime.now()
        ))
        conn.commit()
        
        return {
            "message": "Profile updated successfully",
            "skills_extracted": len(resume_skills) if resume else 0
        }

async def analyze_with_groq(skills: List[str], job_data: dict) -> dict:
    """Use Groq to enhance job and skill analysis"""
    prompt = f"""
    Given these skills: {', '.join(skills)}
    And this job market data: {json.dumps(job_data)}
    
    Please analyze and provide:
    1. The most suitable job roles
    2. Skills gap analysis
    3. Learning roadmap with timeline
    4. Career growth potential
    
    Format the response as a JSON object with these keys:
    - recommended_roles
    - skills_gap
    - learning_roadmap
    - growth_potential
    """
    
    try:
        completion = await groq_client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": """You are a career advisor AI specializing in tech careers and skill development and you want to give career advice 
                to someone who knows that they want to do a job in tech but they don't know which field to go in tech for."""
            }, {
                "role": "user",
                "content": prompt
            }],
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=2000
        )
        
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Groq API error: {str(e)}")
        return None

@app.get("/recommendations/{user_id}", response_model=CareerRecommendation)
async def get_career_recommendations(user_id: int):
    with DBConnection() as conn:
        c = conn.cursor()
        c.execute("SELECT skills, location FROM user_profiles WHERE user_id = ?", (user_id,))
        profile = c.fetchone()
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Get initial recommendations from your ML model
        skills = profile['skills'].split(',')
        predictions = model.predict_next_job("", skills)
        skill_recs = model.get_skill_recommendations(predictions['recommended_jobs'].iloc[0]['Job Title'])
        
        # Enhance recommendations with Groq
        job_data = {
            "initial_prediction": predictions['recommended_jobs'].iloc[0]['Job Title'],
            "skill_match_score": predictions['recommended_jobs'].iloc[0]['skill_match'],
            "market_demand": "high",  # You could get this from your job_data.csv
            "location": profile['location']
        }
        
        groq_analysis = await analyze_with_groq(skills, job_data)
        
        if groq_analysis:
            # Combine ML model predictions with Groq's analysis
            recommendation = CareerRecommendation(
                job_title=predictions['recommended_jobs'].iloc[0]['Job Title'],
                confidence_score=predictions['recommended_jobs'].iloc[0]['skill_match'],
                required_skills=groq_analysis['skills_gap'],
                learning_roadmap={
                    "immediate": groq_analysis['learning_roadmap'].get('immediate', []),
                    "short_term": groq_analysis['learning_roadmap'].get('short_term', []),
                    "long_term": groq_analysis['learning_roadmap'].get('long_term', [])
                }
            )
        else:
            # Fallback to original ML model recommendations
            recommendation = CareerRecommendation(
                job_title=predictions['recommended_jobs'].iloc[0]['Job Title'],
                confidence_score=predictions['recommended_jobs'].iloc[0]['skill_match'],
                required_skills=skill_recs['essential_skills'],
                learning_roadmap={
                    "immediate": skill_recs['essential_skills'][:3],
                    "short_term": skill_recs['recommended_skills'][:3],
                    "long_term": skill_recs['recommended_skills'][3:]
                }
            )
        
        # Store recommendation
        c.execute("""
            INSERT INTO career_recommendations 
            (user_id, recommended_job, confidence_score, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            recommendation.job_title,
            recommendation.confidence_score,
            datetime.now()
        ))
        conn.commit()
        
        return recommendation

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
