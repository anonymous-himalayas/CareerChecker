from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import uvicorn
import os
from datetime import datetime
import PyPDF2
from groq import Groq
import json
from read_resume import read_resume_with_groq, extract_skills
from dotenv import main


main.load_dotenv()


app = FastAPI()


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# COOOOOOOOOOOOOOOORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Hell
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


init_db()

# I think this is pydantic stuff
class UserBase(BaseModel):
    email: str
    id: Optional[int] = None

class UserProfile(BaseModel):
    skills: List[str]
    location: str

class CareerRecommendation(BaseModel):
    job_title: str
    confidence_score: float
    required_skills: List[str]
    learning_roadmap: dict


class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect('career_advisor.db')
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

def get_career_advice_from_groq(skills: List[str], location: str) -> dict:
    """Get career recommendations using Groq"""
    prompt = f"""
    Given these skills: {', '.join(skills)}
    And location: {location}
    
    Please provide career recommendations in tech. Include:
    1. Best matching job title
    2. Required skills for this role
    3. A learning roadmap of skills to acquire in the immediate, short-term, and long-term (make sure it is in the span of 2 months)
    
    Format the response STRICTLY as a JSON object with these keys and lists of strings as values:
    {{
        "job_title": "string",
        "confidence_score": float between 0 and 1,
        "required_skills": ["skill1", "skill2"],
        "learning_roadmap": {{
            "immediate": ["skill1", "skill2"],
            "short_term": ["skill3", "skill4"],
            "long_term": ["skill5", "skill6"]
        }}
    }}
    """
    
    try:
        completion = groq_client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": """You are a career advisor specializing in tech careers with 
                multiple years of experience. Always return valid JSON."""
            }, {
                "role": "user",
                "content": prompt
            }],
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=2000
        )
        
        return json.loads(completion.choices[0].message.content.strip())
    except Exception as e:
        print(f"Groq API error: {str(e)}")
        return None

# User has been created
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
            
            # Get the created user's ID
            c.execute("SELECT id FROM users WHERE email = ?", (user.email,))
            user_id = c.fetchone()['id']
            
            return {
                "email": user.email,
                "id": user_id
            }
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )

# User has been updated
@app.post("/profile/{user_id}")
async def update_profile(
    user_id: int,
    profile: str = Form(...),
    resume: Optional[UploadFile] = File(None)
):
    try:
        profile_data = UserProfile(**json.loads(profile))
        
        with DBConnection() as conn:
            c = conn.cursor()
            
            resume_path = None
            resume_skills = []
            if resume:
                file_path = f"uploads/{user_id}_{resume.filename}"
                os.makedirs("uploads", exist_ok=True)
                with open(file_path, "wb") as buffer:
                    content = await resume.read()
                    buffer.write(content)
                resume_path = file_path
                
                # WORK YOU STUPID THING
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                
                resume_analysis = read_resume_with_groq(text)
                if resume_analysis:
                    resume_skills = extract_skills(resume_analysis)
                    profile_data.skills.extend(resume_skills)
            
            # profile_data.skills = list(set(profile_data.skills))
            c.execute("""
                INSERT OR REPLACE INTO user_profiles 
                (user_id, skills, location, resume_path, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                ",".join(set(profile_data.skills)),
                profile_data.location,
                resume_path,
                datetime.now()
            ))
            conn.commit()
            
            return {
                "message": "Profile updated successfully",
                "skills_extracted": len(resume_skills)
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Recommendations from model and groqq
@app.get("/recommendations/{user_id}", response_model=CareerRecommendation)
async def get_career_recommendations(user_id: int):
    try:
        with DBConnection() as conn:
            c = conn.cursor()
            c.execute("""SELECT skills, location 
                      FROM user_profiles 
                      WHERE user_id = ?""", (user_id,))
            profile = c.fetchone()
            
            if not profile:
                raise HTTPException(status_code=404, detail="Profile not found")
            
            skills = profile['skills'].split(',')
            
            recommendations = get_career_advice_from_groq(skills, profile['location'])
            
            if not recommendations:
                raise HTTPException(
                    status_code=500,
                    detail="Could not generate recommendations"
                )
            
            # Do I really need to add it to the db
            c.execute("""
                INSERT INTO career_recommendations 
                (user_id, recommended_job, confidence_score, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                recommendations['job_title'],
                recommendations['confidence_score'],
                datetime.now()
            ))
            conn.commit()
            
            return CareerRecommendation(**recommendations)
            
    # pls work
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

# unicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
