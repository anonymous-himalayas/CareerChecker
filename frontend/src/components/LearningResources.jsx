import React from 'react';
import './LearningResources.css';

const LearningResources = ({ resources = { courses: [], additional_resources: [] } }) => {
  // Add debug log
  console.log('Resources received in LearningResources:', resources);

  // Ensure we have the expected structure
  const courses = resources?.courses || [];
  const additionalResources = resources?.additional_resources || [];

  // Only render if we have content to show
  if (courses.length === 0 && additionalResources.length === 0) {
    return null;
  }

  return (
    <div className="learning-resources-container">
      <h3 className="resources-title">Recommended Learning Resources</h3>
      
      {courses.length > 0 && (
        <div className="resources-section">
          <h4 className="section-title">Online Courses</h4>
          <div className="courses-grid">
            {courses.map((course, index) => (
              <a
                key={index}
                href={course.link}
                target="_blank"
                rel="noopener noreferrer"
                className="course-card"
              >
                <div className="course-header">
                  <span className="platform-badge">{course.platform}</span>
                  <span className="course-rating">★ {course.rating}</span>
                </div>
                <h5 className="course-title">{course.title}</h5>
                <div className="course-info">
                  <span className="course-skill">Skill: {course.skill}</span>
                  <span className="course-price">{course.price}</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {additionalResources.length > 0 && (
        <div className="resources-section">
          <h4 className="section-title">Additional Resources</h4>
          <div className="resources-grid">
            {additionalResources.map((resource, index) => (
              <a
                key={index}
                href={resource.link}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-card"
              >
                <div className="resource-type-badge">{resource.type}</div>
                <h5 className="resource-title">{resource.title}</h5>
                <p className="resource-description">{resource.description}</p>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default LearningResources; 