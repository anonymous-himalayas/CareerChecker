import React from 'react';
import './GamificationPanel.css';

const GamificationPanel = () => {
  // Mock data for demo
  const userProgress = {
    level: 3,
    currentXp: 350,
    xpToNextLevel: 500,
    badges: [
      {
        id: 1,
        name: "Novice Explorer",
        description: "Started your career journey",
        imageUrl: "🎯"
      },
      {
        id: 2,
        name: "Skill Novice",
        description: "Added a skill to your profile",
        imageUrl: "⭐"
      },
      {
        id: 3,
        name: "Resume Master",
        description: "Uploaded and analyzed your resume",
        imageUrl: "📄"
      }
    ],
    activeQuests: [
      {
        id: 1,
        title: "Skill Master",
        description: "Add skills to your profile",
        xpReward: 200,
        status: "in_progress",
        progress: {
          current: 3,
          total: 5,
          type: "skills"
        }
      },
      {
        id: 2,
        title: "Resume Analysis",
        description: "Upload and analyze your resume to get personalized recommendations",
        xpReward: 150,
        status: "not_started",
        progress: {
          current: 0,
          total: 1,
          type: "upload"
        }
      },
      {
        id: 3,
        title: "Career Path Explorer",
        description: "Complete a recommended course to gain a new skill",
        xpReward: 250,
        status: "not_started",
        progress: {
          current: 0,
          total: 1,
          type: "recommendation"
        }
      }
    ]
  };

  const calculateProgressPercentage = () => {
    return (userProgress.currentXp / userProgress.xpToNextLevel) * 100;
  };

  const renderQuestProgress = (quest) => {
    const percentage = (quest.progress.current / quest.progress.total) * 100;
    
    return (
      <div className="quest-progress">
        <div className="quest-progress-bar">
          <div 
            className="quest-progress-fill"
            style={{ width: `${percentage}%` }}
          ></div>
        </div>
        <div className="quest-progress-text">
          {quest.progress.current}/{quest.progress.total} {quest.progress.type}
        </div>
      </div>
    );
  };

  return (
    <div className="gamification-panel">
      <div className="level-section">
        <h2>Level {userProgress.level}</h2>
        <div className="xp-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${calculateProgressPercentage()}%` }}
            ></div>
          </div>
          <div className="xp-text">
            {userProgress.currentXp} / {userProgress.xpToNextLevel} XP
          </div>
        </div>
      </div>

      <div className="quests-section">
        <h3>Active Quests</h3>
        <div className="quests-list">
          {userProgress.activeQuests
            .sort((a, b) => {
              // Sort order: in_progress, not_started, completed
              const order = { in_progress: 0, not_started: 1, completed: 2 };
              return order[a.status] - order[b.status];
            })
            .map(quest => (
              <div key={quest.id} className={`quest-item ${quest.status}`}>
                <div className="quest-header">
                  <h4>{quest.title}</h4>
                  <span className="xp-reward">+{quest.xpReward} XP</span>
                </div>
                <p>{quest.description}</p>
                {renderQuestProgress(quest)}
                <div className={`quest-status ${quest.status}`}>
                  {quest.status.replace('_', ' ')}
                </div>
              </div>
            ))}
        </div>
      </div>

      <div className="badges-section">
        <h3>Badges Earned</h3>
        <div className="badges-grid">
          {userProgress.badges.map(badge => (
            <div key={badge.id} className="badge-item">
              <div className="badge-icon">{badge.imageUrl}</div>
              <div className="badge-info">
                <h4>{badge.name}</h4>
                <p>{badge.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GamificationPanel; 