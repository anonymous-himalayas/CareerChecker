import React, { useState } from 'react';
import CareerForm from './components/CareerForm';
import Roadmap from './components/Roadmap';
import GamificationPanel from './components/GamificationPanel';
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('form'); // 'form', 'roadmap', or 'gamification'
  const [recommendations, setRecommendations] = useState(null);

  const handleRecommendations = (data) => {
    setRecommendations(data);
    setCurrentPage('roadmap');
  };

  const handleBack = () => {
    setCurrentPage('form');
  };

  const navigateToGamification = () => {
    setCurrentPage('gamification');
  };

  return (
    <div className="App">
      <nav className="navigation">
        <button 
          className={`nav-button ${currentPage === 'form' ? 'active' : ''}`}
          onClick={() => setCurrentPage('form')}
        >
          Career Form
        </button>
        {recommendations && (
          <button 
            className={`nav-button ${currentPage === 'roadmap' ? 'active' : ''}`}
            onClick={() => setCurrentPage('roadmap')}
          >
            Roadmap
          </button>
        )}
        <button 
          className={`nav-button ${currentPage === 'gamification' ? 'active' : ''}`}
          onClick={navigateToGamification}
        >
          Progress & Quests
        </button>
      </nav>

      {currentPage === 'form' && (
        <CareerForm onRecommendations={handleRecommendations} />
      )}
      {currentPage === 'roadmap' && recommendations && (
        <Roadmap 
          recommendations={recommendations} 
          onBack={handleBack}
        />
      )}
      {currentPage === 'gamification' && (
        <GamificationPanel />
      )}
    </div>
  );
}

export default App;
