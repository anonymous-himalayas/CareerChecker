import React from 'react';
import './Roadmap.css';

const Roadmap = ({ recommendations, onBack }) => {
  // Mock data for courses and jobs based on skills
  const learningResources = {
    python: {
      udemy: [
        {
          title: "Complete Python Bootcamp: From Zero to Hero",
          link: "https://www.udemy.com/course/complete-python-bootcamp/",
          rating: 4.8,
          students: "1.2M+"
        },
        {
          title: "Python for Data Science and Machine Learning",
          link: "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/",
          rating: 4.7,
          students: "800K+"
        }
      ],
      other: [
        {
          platform: "Coursera",
          title: "Python for Everybody Specialization",
          link: "https://www.coursera.org/specializations/python"
        },
        {
          platform: "Real Python",
          title: "Python Learning Paths",
          link: "https://realpython.com/learning-paths/"
        }
      ]
    },
    javascript: {
      udemy: [
        {
          title: "The Complete JavaScript Course 2024",
          link: "https://www.udemy.com/course/the-complete-javascript-course/",
          rating: 4.9,
          students: "900K+"
        },
        {
          title: "Modern JavaScript From The Beginning",
          link: "https://www.udemy.com/course/modern-javascript-from-the-beginning/",
          rating: 4.8,
          students: "600K+"
        }
      ],
      other: [
        {
          platform: "freeCodeCamp",
          title: "JavaScript Algorithms and Data Structures",
          link: "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"
        },
        {
          platform: "JavaScript.info",
          title: "The Modern JavaScript Tutorial",
          link: "https://javascript.info/"
        }
      ]
    }
  };

  const jobOpenings = [
    {
      title: "Senior Software Engineer",
      company: "Microsoft",
      location: "Remote",
      salary: "$130,000 - $180,000",
      link: "https://careers.microsoft.com",
      skills: ["python", "javascript", "cloud"]
    },
    {
      title: "Full Stack Developer",
      company: "Amazon",
      location: "Seattle, WA",
      salary: "$120,000 - $160,000",
      link: "https://amazon.jobs",
      skills: ["javascript", "react", "node"]
    },
    {
      title: "Data Scientist",
      company: "Google",
      location: "Mountain View, CA",
      salary: "$140,000 - $200,000",
      link: "https://careers.google.com",
      skills: ["python", "machine learning", "sql"]
    }
  ];

  if (!recommendations) {
    return <div className="loading">Loading recommendations...</div>;
  }

  const { job_title, confidence_score, required_skills, learning_roadmap } = recommendations;

  // Filter jobs based on required skills
  const relevantJobs = jobOpenings.filter(job => 
    job.skills.some(skill => required_skills.includes(skill.toLowerCase()))
  );

  // Get relevant courses based on required skills
  const getRelevantCourses = () => {
    const courses = [];
    required_skills.forEach(skill => {
      if (learningResources[skill.toLowerCase()]) {
        courses.push(...learningResources[skill.toLowerCase()].udemy);
      }
    });
    return courses.slice(0, 3); // Return top 3 courses
  };

  return (
    <div className="roadmap-container">
      <button className="back-button" onClick={onBack}>
        ← Back to Form
      </button>
      
      <h1>Your Career Roadmap</h1>
      
      <div className="recommendation-header">
        <h2>Recommended Role: {job_title}</h2>
        <div className="confidence-score">
          Match Score: {Math.round(confidence_score * 100)}%
        </div>
      </div>

      <div className="skills-section">
        <h3>Required Skills</h3>
        <div className="skills-list">
          {required_skills.map((skill, index) => (
            <span key={index} className="skill-tag">{skill}</span>
          ))}
        </div>
      </div>

      <div className="timeline-container">
        <h3>Learning Timeline</h3>
        <div className="timeline">
          <div className="timeline-section">
            <h4>Immediate Focus (0-2 weeks)</h4>
            <ul>
              {learning_roadmap.immediate.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div className="timeline-section">
            <h4>Short Term (2-4 weeks)</h4>
            <ul>
              {learning_roadmap.short_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>

          <div className="timeline-section">
            <h4>Long Term (1-2 months)</h4>
            <ul>
              {learning_roadmap.long_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="resources-section">
        <h3>Recommended Courses</h3>
        <div className="courses-grid">
          {getRelevantCourses().map((course, index) => (
            <a 
              key={index} 
              href={course.link} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="course-card"
            >
              <h4>{course.title}</h4>
              <div className="course-stats">
                <span>⭐ {course.rating}</span>
                <span>👥 {course.students}</span>
              </div>
            </a>
          ))}
        </div>

        <h3>Additional Learning Resources</h3>
        <ul className="resource-list">
          {required_skills.map(skill => 
            learningResources[skill.toLowerCase()]?.other.map((resource, index) => (
              <li key={index}>
                <a href={resource.link} target="_blank" rel="noopener noreferrer">
                  {resource.platform}: {resource.title}
                </a>
              </li>
            ))
          )}
        </ul>
      </div>

      <div className="jobs-section">
        <h3>Current Job Openings</h3>
        <div className="jobs-grid">
          {relevantJobs.map((job, index) => (
            <a 
              key={index} 
              href={job.link} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="job-card"
            >
              <h4>{job.title}</h4>
              <div className="job-details">
                <span>🏢 {job.company}</span>
                <span>📍 {job.location}</span>
                <span>💰 {job.salary}</span>
              </div>
              <div className="job-skills">
                {job.skills.map((skill, i) => (
                  <span key={i} className="skill-tag">{skill}</span>
                ))}
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Roadmap; 