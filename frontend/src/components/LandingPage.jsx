import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-container">
      <div className="hero-section">
        <div className="content">
          <h1 className="main-title">Career Compass</h1>
          <h2 className="subtitle">Navigate Your Tech Career Path</h2>
          <p className="description">
            Discover personalized career recommendations and learning paths tailored to your skills and interests.
          </p>
          <div className="features">
            <div className="feature">
              <span className="icon">🎯</span>
              <span>Personalized Career Matching</span>
            </div>
            <div className="feature">
              <span className="icon">📚</span>
              <span>Custom Learning Roadmap</span>
            </div>
            <div className="feature">
              <span className="icon">💼</span>
              <span>Job Market Insights</span>
            </div>
          </div>
          <Link to="/career-form" className="cta-button">
            Get Started
          </Link>
        </div>
        <div className="stats">
          <div className="stat-item">
            <h3>500+</h3>
            <p>Career Paths Analyzed</p>
          </div>
          <div className="stat-item">
            <h3>98%</h3>
            <p>User Satisfaction</p>
          </div>
          <div className="stat-item">
            <h3>24/7</h3>
            <p>AI-Powered Support</p>
          </div>
        </div>
      </div>
      
      <div className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Share Your Skills</h3>
            <p>Tell us about your technical skills and experience</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Get Matched</h3>
            <p>Our AI analyzes your profile to find the perfect tech career</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Start Learning</h3>
            <p>Follow your personalized roadmap to success</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage; 