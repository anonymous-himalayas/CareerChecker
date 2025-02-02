import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import './CareerForm.css';
import { useNavigate } from 'react-router-dom';

const CareerForm = ({ onRecommendations }) => {
  const [formData, setFormData] = useState({
    email: '',
    skills: '',
    location: '',
  });
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  // Tooltip content
  const tooltips = {
    skills: "List your technical skills",
    location: "Enter your preferred work location",
    resume: "Upload your resume in PDF format"
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResume(file);
      setError('');
    } else {
      setResume(null);
      setError('Please upload a PDF file');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      // Create FormData for the request
      const formDataToSend = new FormData();
      formDataToSend.append('email', formData.email);
      formDataToSend.append('skills', formData.skills);
      formDataToSend.append('location', formData.location);
      if (resume) {
        formDataToSend.append('resume', resume);
      }

      // Make the API request
      const response = await fetch('http://127.0.0.1:8000/recommendations/', {
        method: 'POST',
        // headers: {
        //   'ngrok-skip-browser-warning': 'true'
        // },
        body: formDataToSend
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const recommendations = await response.json();
      console.log('Received recommendations:', recommendations);
      
      setSuccess(true);
      onRecommendations(recommendations);
      navigate('/roadmap', { state: { recommendations } });

    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="career-form-container">
      <h1>Career Path Advisor</h1>
      <form onSubmit={handleSubmit} className="career-form">
        <div className="form-group">
          <label htmlFor="email">
            Email Address <span className="required">*</span>
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="your.email@example.com"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="skills">
            Skills <span className="required">*</span>
            <div className="tooltip-container">
              <FontAwesomeIcon icon={faCircleInfo} className="info-icon" />
              <span className="tooltip-text">{tooltips.skills}</span>
            </div>
          </label>
          <textarea
            id="skills"
            name="skills"
            value={formData.skills}
            onChange={handleInputChange}
            placeholder="e.g., Python, JavaScript, SQL"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">
            Location <span className="required">*</span>
            <div className="tooltip-container">
              <FontAwesomeIcon icon={faCircleInfo} className="info-icon" />
              <span className="tooltip-text">{tooltips.location}</span>
            </div>
          </label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="e.g., New York, NY"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="resume">
            Resume
            <div className="tooltip-container">
              <FontAwesomeIcon icon={faCircleInfo} className="info-icon" />
              <span className="tooltip-text">{tooltips.resume}</span>
            </div>
          </label>
          <input
            type="file"
            id="resume"
            accept=".pdf"
            onChange={handleFileChange}
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">Form submitted successfully!</div>}

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Get Career Recommendations'}
        </button>
      </form>
    </div>
  );
};

export default CareerForm; 