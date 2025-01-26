import React, { useState } from 'react';
import './CareerForm.css';

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
      // Create user first
      const userResponse = await fetch('https://341e-169-234-117-150.ngrok-free.app/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: formData.email })
      });

      if (!userResponse.ok) {
        const errorData = await userResponse.json();
        throw new Error(errorData.detail || 'Failed to create user');
      }

      const userData = await userResponse.json();
      const userId = userData.id; // Get the actual user ID from response

      // Convert skills string to array and remove whitespace
      const skillsArray = formData.skills.split(',').map(skill => skill.trim());
      
      // Create profile object
      const profileData = {
        skills: skillsArray,
        location: formData.location
      };

      // Create FormData for profile update
      const formDataToSend = new FormData();
      formDataToSend.append('profile', JSON.stringify(profileData));
      if (resume) {
        formDataToSend.append('resume', resume);
      }

      // Update profile
      const profileResponse = await fetch(`https://341e-169-234-117-150.ngrok-free.app/profile/${userId}`, {
        method: 'POST',
        body: formDataToSend,
      });

      if (!profileResponse.ok) {
        throw new Error('Failed to update profile');
      }

      // Get recommendations
      const recommendationsResponse = await fetch(`https://341e-169-234-117-150.ngrok-free.app/recommendations/${userId}`);
      
      if (!recommendationsResponse.ok) {
        throw new Error('Failed to get recommendations');
      }

      const recommendations = await recommendationsResponse.json();
      setSuccess(true);
      onRecommendations(recommendations);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="career-form-container">
      <h1>Career Path Advisor</h1>
      <form onSubmit={handleSubmit} className="career-form">
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
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
          <label htmlFor="skills">Skills (comma-separated)</label>
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
          <label htmlFor="location">Location</label>
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
          <label htmlFor="resume">Resume (Optional)</label>
          <input
            type="file"
            id="resume"
            accept=".pdf"
            onChange={handleFileChange}
          />
          <small>Upload PDF file only</small>
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