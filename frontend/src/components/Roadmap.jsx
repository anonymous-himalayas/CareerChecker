import React from 'react';
import './Roadmap.css';

const Roadmap = ({ recommendations, onBack }) => {
  if (!recommendations) {
    return <div className="loading">Loading recommendations...</div>;
  }

  const { job_title, confidence_score, required_skills, learning_roadmap } = recommendations;

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

      <div className="next-steps">
        <h3>Next Steps</h3>
        <p>Start your learning journey by focusing on the immediate skills listed above. 
           Consider using resources like:</p>
        <ul>
          <li>Online learning platforms (Coursera, Udemy, etc.)</li>
          <li>Practice projects</li>
          <li>Technical documentation</li>
          <li>Community forums and meetups</li>
        </ul>
      </div>
    </div>
  );
};

export default Roadmap; 