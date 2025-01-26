import React, { useEffect } from 'react';
import './Roadmap.css';

const Roadmap = ({ recommendations, onBack }) => {
  useEffect(() => {
    console.log('Full recommendations:', recommendations);
  }, [recommendations]);

  if (!recommendations) {
    return <div className="loading">Loading recommendations...</div>;
  }

  const { 
    job_title, 
    confidence_score, 
    required_skills, 
    learning_roadmap,
    relevant_jobs = [] 
  } = recommendations;

  return (
    <div className="roadmap-container">
      <button className="back-button" onClick={onBack}>
        ← Back to Form
      </button>
      
      <div className="recommendation-header">
        <h2>Recommended Role: {job_title}</h2>
        <div className="confidence-score">
          Match Score: {Math.round(confidence_score * 100)}%
        </div>
      </div>

      <div className="required-skills">
        <h3>Required Skills</h3>
        <div className="skills-grid">
          {required_skills.map((skill, index) => (
            <div key={index} className="skill-card">
              {skill}
            </div>
          ))}
        </div>
      </div>

      <div className="learning-path">
        <h3>Learning Path</h3>
        <div className="timeline">
          <div className="timeline-section">
            <h4>Immediate (0-2 weeks)</h4>
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

      {relevant_jobs.length > 0 && (
        <div className="jobs-section">
          <h3>Featured Job Openings</h3>
          <div className="jobs-grid">
            {relevant_jobs.slice(0, 2).map((job, index) => (
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
      )}
    </div>
  );
};

export default Roadmap; 