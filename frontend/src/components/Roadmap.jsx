import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Roadmap.css';

const Roadmap = ({ recommendations }) => {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/career-form');
  };

  useEffect(() => {
    console.log('Full recommendations:', recommendations);
  }, [recommendations]);

  if (!recommendations) {
    return <div className="loading">Loading recommendations...</div>;
  }

  const { 
    job_title = '', 
    confidence_score = 0,
    required_skills = [],
    learning_roadmap = {
      immediate: [],
      short_term: [],
      long_term: []
    }
  } = recommendations;

  // Need to fix this
  const displayResources = defaultCourses[job_title] || {
    courses: [],
    additional_resources: []
  };


  const careerJobs = jobListings[job_title] || [];


  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'beginner':
        return 'difficulty-beginner';
      case 'intermediate':
        return 'difficulty-intermediate';
      case 'advanced':
        return 'difficulty-advanced';
      default:
        return '';
    }
  };

  const getFormatIcon = (format) => {
    switch(format?.toLowerCase()) {
      case 'video':
        return '🎥';
      case 'text':
        return '📚';
      case 'interactive':
        return '💻';
      default:
        return '📌';
    }
  };

  return (
    <div className="roadmap-container">
      <button className="back-button" onClick={handleBack}>
        ← Back to Form
      </button>
      
      <div className="recommendation-header">
        <div className="role-container">
          <h4 className="recommended-label">Recommended Role</h4>
          <h1 className="role-title">{job_title}</h1>
          <div className="confidence-score">
            Match Score: {Math.round(confidence_score * 100)}%
          </div>
        </div>
      </div>

      <div className="gamification-panel">
        <div className="level-info">
          <h3>Career Progress</h3>
          <div className="level-container">
            <div className="level-circle">1</div>
            <div className="level-details">
              <span className="level-label">Level 1</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '45%' }}></div>
              </div>
              <span className="xp-text">450/1000 XP</span>
            </div>
          </div>
        </div>

        <div className="active-quests">
          <h3>Active Quests</h3>
          <div className="quest-list">
            <div className="quest-item">
              <div className="quest-info">
                <h4>Complete First Course</h4>
                <p>Finish your first recommended course</p>
              </div>
              <div className="quest-progress">
                <span className="xp-reward">+100 XP</span>
                <div className="progress-bar">
                  <div className="progress" style={{ width: '60%' }}></div>
                </div>
              </div>
            </div>
            <div className="quest-item">
              <div className="quest-info">
                <h4>Skill Master</h4>
                <p>Learn 3 new required skills</p>
              </div>
              <div className="quest-progress">
                <span className="xp-reward">+150 XP</span>
                <div className="progress-bar">
                  <div className="progress" style={{ width: '30%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="section-container">
        <h3 className="section-title">Required Skills</h3>
        <div className="skills-grid">
          {required_skills.map((skill, index) => (
            <div key={index} className="skill-card">
              {skill}
            </div>
          ))}
        </div>
      </div>

      <div className="section-container">
        <h3 className="section-title">Learning Path</h3>
        <div className="timeline">
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Immediate</h4>
              <span className="timeline-duration">0-2 weeks</span>
            </div>
            <ul>
              {learning_roadmap.immediate.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Short Term</h4>
              <span className="timeline-duration">2-4 weeks</span>
            </div>
            <ul>
              {learning_roadmap.short_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Long Term</h4>
              <span className="timeline-duration">1-2 months</span>
            </div>
            <ul>
              {learning_roadmap.long_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="section-container resources-container">
        
        <div className="courses-section">
          <h1 className="subsection-title">Recommended Courses</h1>
          <div className="courses-grid">
            {displayResources.courses.map((course, index) => (
              <a
                key={index}
                href={course.link}
                target="_blank"
                rel="noopener noreferrer"
                className="course-card"
              >
                <div className="course-content">
                  <div className="course-header">
                    <div className="course-platform">{course.platform}</div>
                    <div className={`difficulty ${getDifficultyColor(course.difficulty)}`}>
                      {course.difficulty}
                    </div>
                  </div>
                  <h5>{course.title}</h5>
                </div>
                <div className="course-footer">
                  <div className="course-details">
                    <span className="course-rating">★ {course.rating}</span>
                    <span className="course-price">{course.price}</span>
                  </div>
                  <div className="course-skill">
                    <span>{course.skill}</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>

        <div className="additional-resources">
          <h1>Additional Learning Resources</h1>
          <div className="resources-grid">
            {displayResources.additional_resources.map((resource, index) => (
              <a
                key={index}
                href={resource.link}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-card"
              >
                <div className="resource-header">
                  <div className="resource-type">{resource.type}</div>
                  <div className="resource-format">
                    {getFormatIcon(resource.format)} {resource.format}
                  </div>
                </div>
                <h5>{resource.title}</h5>
                <p className="resource-description">{resource.description}</p>
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="job-listings-section">
        <h1>Featured Job Opportunities</h1>
        <div className="jobs-grid">
          {careerJobs.map((job, index) => (
            <a
              key={index}
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="job-card"
            >
              <div className="job-header">
                <h4>{job.title}</h4>
                <div className="company-name">{job.company}</div>
              </div>
              <div className="job-details">
                <div className="detail-item">
                  <span className="icon">📍</span>
                  {job.location}
                </div>
                <div className="detail-item">
                  <span className="icon">💰</span>
                  {job.salary}
                </div>
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