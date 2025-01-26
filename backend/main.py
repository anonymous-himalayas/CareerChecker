from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
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
import logging



main.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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

@app.post("/recommendations/")
async def get_recommendations(
    email: str = Form(...),
    skills: str = Form(...),
    location: str = Form(...),
    experience: str = Form(""),
    education: str = Form(""),
    interests: str = Form(""),
    resume: UploadFile = File(None)
):
    try:
        logger.info(f"Processing request for {email} with skills: {skills}")

        # Process resume if provided
        # ... (keep existing resume processing code)

        # Career analysis prompt
        career_prompt = """
        Based on these skills: {skills} and location: {location}, provide a career recommendation.
        
        Respond with ONLY a JSON object in this EXACT format, no additional text or explanation:
        {{
            "job_title": "Best matching job title",
            "confidence_score": 0.85,
            "required_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
            "learning_roadmap": {{
                "immediate": ["skill1", "skill2"],
                "short_term": ["skill3", "skill4"],
                "long_term": ["skill5", "skill6"]
            }},
            "learning_resources": {{
                "courses": [
                    {{
                        "title": "Complete Python Developer Course",
                        "platform": "Udemy",
                        "link": "https://www.udemy.com/course/complete-python-developer",
                        "price": "$12.99",
                        "rating": 4.8,
                        "skill": "Python"
                    }},
                    {{
                        "title": "React - The Complete Guide",
                        "platform": "Coursera",
                        "link": "https://www.coursera.org/learn/react-complete-guide",
                        "price": "$49.99",
                        "rating": 4.7,
                        "skill": "React"
                    }}
                ],
                "additional_resources": [
                    {{
                        "title": "MDN Web Docs",
                        "type": "Documentation",
                        "link": "https://developer.mozilla.org",
                        "description": "Comprehensive web development documentation"
                    }},
                    {{
                        "title": "freeCodeCamp",
                        "type": "Interactive Learning",
                        "link": "https://www.freecodecamp.org",
                        "description": "Free coding tutorials and certifications"
                    }}
                ]
            }},
            "relevant_jobs": [
                {{
                    "title": "Senior Software Engineer",
                    "company": "Example Corp",
                    "location": "Remote",
                    "salary": "$120,000 - $150,000",
                    "skills": ["Python", "JavaScript", "AWS"],
                    "link": "https://example.com/jobs/123"
                }},
                {{
                    "title": "Software Developer",
                    "company": "Tech Solutions Inc",
                    "location": "New York, NY",
                    "salary": "$90,000 - $120,000",
                    "skills": ["React", "Node.js", "SQL"],
                    "link": "https://example.com/jobs/456"
                }}
            ]
        }}
        """.format(skills=skills, location=location)

        # Get career recommendation
        career_response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a career advisor. Respond only with the requested JSON format, including job listings. No additional text."
                },
                {
                    "role": "user",
                    "content": career_prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1000
        )

        # Clean and parse career response
        career_text = career_response.choices[0].message.content.strip()
        logger.info(f"Raw career response: {career_text}")

        # Find the JSON object in the response
        try:
            start_idx = career_text.find('{')
            end_idx = career_text.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            
            career_json = career_text[start_idx:end_idx]
            career_data = json.loads(career_json)
            logger.info("Successfully parsed career data")
            
            # After parsing career_data, ensure learning resources exist
            if not career_data.get('learning_resources'):
                # Create learning resources based on the required skills
                skills_courses = []
                for skill in career_data.get('required_skills', [])[:2]:  # Get first two skills
                    if skill.lower() == 'python':
                        skills_courses.append({
                            "title": "Complete Python Bootcamp",
                            "platform": "Udemy",
                            "link": "https://www.udemy.com/course/complete-python-bootcamp/",
                            "price": "$12.99",
                            "rating": 4.8,
                            "skill": "Python"
                        })
                    elif 'javascript' in skill.lower():
                        skills_courses.append({
                            "title": "Modern JavaScript from the Beginning",
                            "platform": "Udemy",
                            "link": "https://www.udemy.com/course/modern-javascript/",
                            "price": "$14.99",
                            "rating": 4.7,
                            "skill": "JavaScript"
                        })
                    else:
                        skills_courses.append({
                            "title": f"Complete {skill} Course",
                            "platform": "Coursera",
                            "link": "https://www.coursera.org",
                            "price": "$49.99",
                            "rating": 4.6,
                            "skill": skill
                        })

                career_data['learning_resources'] = {
                    "courses": skills_courses,
                    "additional_resources": [
                        {
                            "title": "freeCodeCamp",
                            "type": "Interactive Learning",
                            "link": "https://www.freecodecamp.org",
                            "description": "Free coding tutorials and certifications for web development"
                        },
                        {
                            "title": "MDN Web Docs",
                            "type": "Documentation",
                            "link": "https://developer.mozilla.org",
                            "description": "Comprehensive web development documentation and tutorials"
                        },
                        {
                            "title": "GitHub Learning Lab",
                            "type": "Interactive Learning",
                            "link": "https://lab.github.com",
                            "description": "Learn essential developer tools and workflows"
                        }
                    ]
                }

            # Prepare final response with all necessary data
            response_data = {
                "job_title": career_data["job_title"],
                "confidence_score": career_data["confidence_score"],
                "required_skills": career_data["required_skills"],
                "learning_roadmap": career_data["learning_roadmap"],
                "learning_resources": career_data["learning_resources"],  # Ensure this is included
                "relevant_jobs": career_data.get("relevant_jobs", [])
            }

            logger.info("Response data structure:")
            logger.info(json.dumps(response_data, indent=2))

            # Generate specific course recommendations based on skills and career path
            learning_prompt = f"""
            As a career advisor, recommend specific online courses and learning resources for someone pursuing a career as a {career_data['job_title']} 
            with these skills: {skills}.
            Focus on their learning roadmap: {json.dumps(career_data['learning_roadmap'])}
            
            Return ONLY a JSON object in this EXACT format:
            {{
                "courses": [
                    {{
                        "title": "Exact course title from a real platform",
                        "platform": "Platform name (Udemy/Coursera/etc)",
                        "link": "Actual course URL",
                        "price": "Current price in USD",
                        "rating": "Course rating (1-5)",
                        "skill": "Primary skill taught",
                        "difficulty": "Beginner/Intermediate/Advanced"
                    }}
                ],
                "additional_resources": [
                    {{
                        "title": "Resource name",
                        "type": "Documentation/Tutorial/Practice/Community",
                        "link": "Resource URL",
                        "description": "Brief description focusing on career relevance",
                        "format": "Video/Text/Interactive"
                    }}
                ]
            }}
            
            Focus on:
            1. Real, currently available courses
            2. Mix of free and paid resources
            3. Resources matching their skill level
            4. Courses aligned with immediate and short-term skills
            5. Popular and highly-rated content
            """

            learning_response = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical education advisor with deep knowledge of programming courses and learning resources. Provide specific, real course recommendations from major platforms."
                    },
                    {
                        "role": "user",
                        "content": learning_prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1500
            )

            try:
                learning_text = learning_response.choices[0].message.content.strip()
                learning_resources = json.loads(learning_text)
                
                # Validate and clean the response
                if not isinstance(learning_resources.get('courses'), list):
                    raise ValueError("Invalid courses format")
                if not isinstance(learning_resources.get('additional_resources'), list):
                    raise ValueError("Invalid additional resources format")

                # Ensure we have at least some recommendations
                if len(learning_resources['courses']) == 0:
                    raise ValueError("No courses provided")

            except Exception as e:
                logger.error(f"Error parsing learning resources: {e}")
                # Provide fallback recommendations based on career path
                learning_resources = {
                    "courses": [
                        {
                            "title": f"Complete {career_data['job_title']} Bootcamp 2024",
                            "platform": "Udemy",
                            "link": "https://www.udemy.com",
                            "price": "$13.99",
                            "rating": 4.8,
                            "skill": career_data['required_skills'][0] if career_data['required_skills'] else "Programming",
                            "difficulty": "Beginner"
                        },
                        {
                            "title": f"Advanced {career_data['job_title']} Specialization",
                            "platform": "Coursera",
                            "link": "https://www.coursera.org",
                            "price": "$49.99",
                            "rating": 4.7,
                            "skill": career_data['required_skills'][1] if len(career_data['required_skills']) > 1 else "Development",
                            "difficulty": "Intermediate"
                        }
                    ],
                    "additional_resources": [
                        {
                            "title": "freeCodeCamp",
                            "type": "Interactive Learning",
                            "link": "https://www.freecodecamp.org",
                            "description": f"Free certification program covering essential {career_data['job_title']} skills",
                            "format": "Interactive"
                        },
                        {
                            "title": "MDN Web Docs",
                            "type": "Documentation",
                            "link": "https://developer.mozilla.org",
                            "description": "Comprehensive web development documentation and tutorials",
                            "format": "Text"
                        }
                    ]
                }

            # Update career_data with learning resources
            career_data['learning_resources'] = learning_resources

            # Prepare final response
            response_data = {
                "job_title": career_data["job_title"],
                "confidence_score": career_data["confidence_score"],
                "required_skills": career_data["required_skills"],
                "learning_roadmap": career_data["learning_roadmap"],
                "learning_resources": career_data["learning_resources"],
                "relevant_jobs": career_data.get("relevant_jobs", [])
            }

            logger.info("Successfully prepared final response with learning resources")
            return response_data

        except Exception as e:
            logger.error(f"Career parsing error: {e}")
            logger.error(f"Attempted to parse: {career_text}")
            raise HTTPException(status_code=500, detail="Failed to parse career response")

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job-openings")
async def get_job_openings(title: str = Query(...)):
    try:
        # Here you would implement the logic to fetch job openings based on the title
        # For demonstration, let's return some mock data
        job_openings = [
            {
                "title": f"Senior {title}",
                "company": "Tech Company A",
                "location": "Remote",
                "salary": "$120,000 - $150,000",
                "skills": ["Python", "Django", "REST APIs"],
                "link": "https://example.com/job-a"
            },
            {
                "title": f"Junior {title}",
                "company": "Tech Company B",
                "location": "New York, NY",
                "salary": "$80,000 - $100,000",
                "skills": ["JavaScript", "React"],
                "link": "https://example.com/job-b"
            }
        ]
        return job_openings
    except Exception as e:
        logger.error(f"Error fetching job openings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch job openings")

# unicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
