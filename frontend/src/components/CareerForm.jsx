import React, { useState } from 'react';
import './CareerForm.css';

const CareerForm = () => {
  const [formData, setFormData] = useState({
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
      // Create form data for multipart/form-data
      const formDataToSend = new FormData();
      
      // Convert skills string to array and remove whitespace
      const skillsArray = formData.skills.split(',').map(skill => skill.trim());
      
      // Create profile object
      const profileData = {
        skills: skillsArray,
        location: formData.location
      };

      // Append profile data and resume if exists
      formDataToSend.append('profile', JSON.stringify(profileData));
      if (resume) {
        formDataToSend.append('resume', resume);
      }

      // First create a user
      const userResponse = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: 'user@example.com' }) // You might want to add email input
      });

      if (!userResponse.ok) {
        throw new Error('Failed to create user');
      }

      const userData = await userResponse.json();
      const userId = 1; // For testing, you might want to get this from the response

      // Update profile with skills and resume
      const profileResponse = await fetch(`http://localhost:8000/profile/${userId}`, {
        method: 'POST',
        body: formDataToSend,
      });

      if (!profileResponse.ok) {
        throw new Error('Failed to update profile');
      }

      // Get career recommendations
      const recommendationsResponse = await fetch(`http://localhost:8000/recommendations/${userId}`);
      
      if (!recommendationsResponse.ok) {
        throw new Error('Failed to get recommendations');
      }

      const recommendations = await recommendationsResponse.json();
      setSuccess(true);
      // Handle recommendations display (you might want to pass this to a parent component)
      console.log(recommendations);

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