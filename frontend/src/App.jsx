import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
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
    <Router basename="/CareerChecker">
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
        <Route 
          path="/gamification" 
          element={<GamificationPanel />}
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
