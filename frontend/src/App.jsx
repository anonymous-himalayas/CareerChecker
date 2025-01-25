import React, { useState } from 'react';
import CareerForm from './components/CareerForm';
import Roadmap from './components/Roadmap';
import './App.css'

function App() {
  const [recommendations, setRecommendations] = useState(null);

  const handleRecommendations = (data) => {
    setRecommendations(data);
  };

  const handleBack = () => {
    setRecommendations(null);
  };

  return (
    <div className="App">
      {!recommendations ? (
        <CareerForm onRecommendations={handleRecommendations} />
      ) : (
        <Roadmap 
          recommendations={recommendations} 
          onBack={handleBack}
        />
      )}
    </div>
  );
}

export default App;
