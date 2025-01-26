import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import CareerForm from './components/CareerForm';
import Roadmap from './components/Roadmap';
import GamificationPanel from './components/GamificationPanel';
import './App.css'

function App() {
  const [recommendations, setRecommendations] = useState(null);

  const handleRecommendations = (data) => {
    setRecommendations(data);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route 
          path="/career-form" 
          element={
            <CareerForm 
              onRecommendations={handleRecommendations}
            />
          } 
        />
        <Route 
          path="/roadmap" 
          element={
            <Roadmap 
              recommendations={recommendations}
              onBack={() => window.history.back()}
            />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
