import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Roadmap.css';

const Roadmap = ({ recommendations }) => {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/career-form');
  };

  const defaultCourses = {
    "Senior Data Scientist": {
      courses: [
        {
          title: "Machine Learning A-Z™: Hands-On Python & R In Data Science",
          platform: "Udemy",
          link: "https://www.udemy.com/course/machinelearning/",
          price: "$12.99",
          rating: 4.5,
          skill: "Machine Learning",
          difficulty: "Intermediate"
        },
        {
          title: "Deep Learning Specialization",
          platform: "Coursera",
          link: "https://www.coursera.org/specializations/deep-learning",
          price: "$49/month",
          rating: 4.8,
          skill: "Deep Learning",
          difficulty: "Advanced"
        }
      ],
      additional_resources: [
        {
          title: "Machine Learning Documentation",
          type: "Documentation",
          link: "https://scikit-learn.org/stable/",
          description: "Official ML documentation and tutorials",
          format: "Text"
        },
        {
          title: "Deep Learning Book",
          type: "Book",
          link: "https://www.deeplearningbook.org/",
          description: "Comprehensive deep learning book by Ian Goodfellow",
          format: "Text"
        }
      ]
    },
    "Senior Software Engineer": {
      courses: [
        {
          title: "System Design Interview",
          platform: "Educative",
          link: "https://www.educative.io/courses/grokking-the-system-design-interview",
          price: "$59",
          rating: 4.8,
          skill: "System Design",
          difficulty: "Advanced"
        },
        {
          title: "Cracking the Coding Interview",
          platform: "Amazon",
          link: "https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850",
          price: "$26.49",
          rating: 4.6,
          skill: "Coding",
          difficulty: "Intermediate"
        }
      ],
      additional_resources: [
        {
          title: "LeetCode",
          type: "Practice Platform",
          link: "https://leetcode.com",
          description: "Practice coding problems and prepare for technical interviews",
          format: "Interactive"
        },
        {
          title: "HackerRank",
          type: "Practice Platform",
          link: "https://www.hackerrank.com",
          description: "Practice coding problems and compete in contests",
          format: "Interactive"
        }
      ]
    },
    "Data Engineer": {
      courses: [
        {
          title: "Data Engineering Nanodegree",
          platform: "Udacity",
          link: "https://www.udacity.com/course/data-engineer-nanodegree--nd027",
          price: "$399/month",
          rating: 4.6,
          skill: "Data Engineering",
          difficulty: "Intermediate"
        },
        {
          title: "Big Data Specialization",
          platform: "Coursera",
          link: "https://www.coursera.org/specializations/big-data",
          price: "$49/month",
          rating: 4.7,
          skill: "Big Data",
          difficulty: "Intermediate"
        }
      ],
      additional_resources: [
        {
          title: "Data Engineering on Google Cloud Platform Specialization",
          type: "Coursera Specialization",
          link: "https://www.coursera.org/specializations/gcp-data-machine-learning",
          description: "Learn to design, build, and operate systems on Google Cloud Platform",
          format: "Video"
        },
        {
          title: "Data Engineering Cookbook",
          type: "Book",
          link: "https://www.oreilly.com/library/view/data-engineering-cookbook/9781491995841/",
          description: "Recipes for building scalable data pipelines",
          format: "Text"
        }
      ]
    },
    "Full Stack Software Engineer": {
      courses: [
        {
          title: "The Web Developer Bootcamp 2021",
          platform: "Udemy",
          link: "https://www.udemy.com/course/the-web-developer-bootcamp/",
          price: "$12.99",
          rating: 4.7,
          skill: "Web Development",
          difficulty: "Beginner"
        },
        {
          title: "React - The Complete Guide (incl Hooks, React Router, Redux)",
          platform: "Udemy",
          link: "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
          price: "$12.99",
          rating: 4.7,
          skill: "React",
          difficulty: "Intermediate"
        }
      ],
      additional_resources: [
        {
          title: "freeCodeCamp",
          type: "Online Learning Platform",
          link: "https://www.freecodecamp.org",
          description: "Learn to code and build projects for nonprofits",
          format: "Interactive"
        },
        {
          title: "MDN Web Docs",
          type: "Documentation",
          link: "https://developer.mozilla.org",
          description: "Comprehensive web development documentation",
          format: "Text"
        }
      ]
    },
    "Senior Frontend Developer": {
      courses: [
        {
          title: "Advanced CSS and Sass: Flexbox, Grid, Animations and More!",
          platform: "Udemy",
          link: "https://www.udemy.com/course/advanced-css-and-sass/",
          price: "$12.99",
          rating: 4.8,
          skill: "CSS",
          difficulty: "Intermediate"
        },
        {
          title: "React - The Complete Guide (incl Hooks, React Router, Redux)",
          platform: "Udemy",
          link: "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
          price: "$12.99",
          rating: 4.7,
          skill: "React",
          difficulty: "Intermediate"
        }
      ],
      additional_resources: [
        {
          title: "Frontend Masters",
          type: "Online Learning Platform",
          link: "https://frontendmasters.com",
          description: "Advance your skills with in-depth frontend development courses",
          format: "Video"
        },
        {
          title: "CodePen",
          type: "Development Tool",
          link: "https://codepen.io",
          description: "Frontend development playground for HTML, CSS, and JavaScript",
          format: "Interactive"
        }
      ]
    },
    "Data Scientist": {
      courses: [
        {
          title: "Complete SQL Mastery",
          platform: "Udemy",
          link: "https://www.udemy.com/course/complete-sql-mastery/",
          price: "$13.99",
          rating: 4.8,
          skill: "SQL",
          difficulty: "Intermediate"
        },
        {
          title: "Python for Data Science and Machine Learning",
          platform: "Udemy",
          link: "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/",
          price: "$14.99",
          rating: 4.9,
          skill: "Python",
          difficulty: "Intermediate"
        }
      ],
      additional_resources: [
        {
          title: "AWS Machine Learning",
          type: "Documentation",
          link: "https://aws.amazon.com/machine-learning/",
          description: "Learn about AWS Machine Learning services",
          format: "Text"
        },
        {
          title: "Machine Learning Documentation",
          type: "Documentation",
          link: "https://scikit-learn.org/stable/",
          description: "Official ML documentation and tutorials",
          format: "Text"
        }
      ]
    },
    "Web Developer": {
      "courses": [
        {
          title: "The Web Developer Bootcamp 2021",
          platform: "Udemy",
          link: "https://www.udemy.com/course/the-web-developer-bootcamp/",
          price: "$12.99",
          rating: 4.7,
          skill: "Web Development",
          difficulty: "Beginner"
        },
        {
          title: "JavaScript: Understanding the Weird Parts",
          platform: "Udemy",
          link: "https://www.udemy.com/course/understand-javascript/",
          price: "$12.99",
          rating: 4.8,
          skill: "JavaScript",
          difficulty: "Intermediate"
        },
        {
          title: "React - The Complete Guide (incl Hooks, React Router, Redux)",
          platform: "Udemy",
          link: "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
          price: "$12.99",
          rating: 4.7,
          skill: "React",
          difficulty: "Intermediate"
        }
      ],
      "additional_resources": [
        {
          title: "freeCodeCamp",
          type: "Online Learning Platform",
          link: "https://www.freecodecamp.org",
          description: "Learn to code and build projects for nonprofits",
          format: "Interactive"
        },
        {
          title: "MDN Web Docs",
          type: "Documentation",
          link: "https://developer.mozilla.org",
          description: "Comprehensive web development documentation",
          format: "Text"
        },
        {
          title: "CSS-Tricks",
          type: "Blog",
          link: "https://css-tricks.com",
          description: "Web design and development blog with CSS tips and tricks",
          format: "Text"
        }
      ]
    },
    "Frontend Developer": {
      "courses": [
        {
          title: "Front End Web Development Bootcamp",
          platform: "Udemy",
          link: "https://www.udemy.com/course/front-end-web-development-bootcamp/",
          price: "$12.99",
          rating: 4.7,
          skill: "Frontend Development",
          difficulty: "Beginner"
        },
        {
          title: "React - The Complete Guide (incl Hooks, React Router, Redux)",
          platform: "Udemy",
          link: "https://www.udemy.com/course/react-the-complete-guide-incl-redux/",
          price: "$12.99",
          rating: 4.7,
          skill: "React",
          difficulty: "Intermediate"
        },
        {
          title: "Advanced CSS and Sass: Flexbox, Grid, Animations and More!",
          platform: "Udemy",
          link: "https://www.udemy.com/course/advanced-css-and-sass/",
          price: "$12.99",
          rating: 4.8,
          skill: "CSS",
          difficulty: "Intermediate"
        }
      ],
      "additional_resources": [
        {
          title: "Frontend Masters",
          type: "Online Learning Platform",
          link: "https://frontendmasters.com",
          description: "Advance your skills with in-depth frontend development courses",
          format: "Video"
        },
        {
          title: "CodePen",
          type: "Development Tool",
          link: "https://codepen.io",
          description: "Frontend development playground for HTML, CSS, and JavaScript",
          format: "Interactive"
        }
      ]
    },
    "Data Engineer": {
      "courses": [
        {
          title: "Data Engineering Nanodegree",
          platform: "Udacity",
          link: "https://www.udacity.com/course/data-engineer-nanodegree--nd027",
          price: "$399/month",
          rating: 4.6,
          skill: "Data Engineering",
          difficulty: "Intermediate"
        },
        {
          title: "Big Data Specialization",
          platform: "Coursera",
          link: "https://www.coursera.org/specializations/big-data",
          price: "$49/month",
          rating: 4.7,
          skill: "Big Data",
          difficulty: "Intermediate"
        },
        {
          title: "Apache Spark for Data Engineers",
          platform: "Udemy",
          link: "https://www.udemy.com/course/apache-spark-for-data-engineers/",
          price: "$12.99",
          rating: 4.5,
          skill: "Apache Spark",
          difficulty: "Intermediate"
        }
      ],
      "additional_resources": [
        {
          title: "Data Engineering on Google Cloud Platform Specialization",
          type: "Coursera Specialization",
          link: "https://www.coursera.org/specializations/gcp-data-machine-learning",
          description: "Learn to design, build, and operate systems on Google Cloud Platform",
          format: "Video"
        },
        {
          title: "Data Engineering Cookbook",
          type: "Book",
          link: "https://www.oreilly.com/library/view/data-engineering-cookbook/9781491995841/",
          description: "Recipes for building scalable data pipelines",
          format: "Text"
        },
        {
          title: "Google Cloud Platform",
          type: "Online Learning Platform",
          link: "https://cloud.google.com/training",
          description: "Learn data engineering on Google Cloud Platform",
          format: "Interactive"
        }
      ]
    },
    "Data Analyst": {
      "courses": [
        {
          title: "Data Analyst Nanodegree",
          platform: "Udacity",
          link: "https://www.udacity.com/course/data-analyst-nanodegree--nd002",
          price: "$399/month",
          rating: 4.6,
          skill: "Data Analysis",
          difficulty: "Intermediate"
        },
        {
          title: "Data Analysis and Visualization with Python",
          platform: "Udemy",
          link: "https://www.udemy.com/course/data-analysis-and-visualization-with-python/",
          price: "$12.99",
          rating: 4.5,
          skill: "Python",
          difficulty: "Intermediate"
        },
        {
          title: "SQL for Data Science",
          platform: "Coursera",
          link: "https://www.coursera.org/learn/sql-for-data-science",
          price: "$49.99",
          rating: 4.7,
          skill: "SQL",
          difficulty: "Beginner"
        }
      ], "additional_resources": [
        {
          title: "Mode Analytics SQL Tutorial",
          type: "Tutorial",
          link: "https://mode.com/sql-tutorial/",
          description: "Learn SQL with this interactive tutorial",
          format: "Interactive"
        },
        {
          title: "DataQuest",
          type: "Online Learning Platform",
          link: "https://www.dataquest.io",
          description: "Learn data science in your browser",
          format: "Interactive"
        },
        {
          title: "Data.gov",
          type: "Data Source",
          link: "https://www.data.gov",
          description: "Open data from the US government",
          format: "Text"
        }
      ],
    },
    "Software Engineer": {
      "courses": [
        {
          title: "Software Engineer Interview Preparation",
          platform: "Udemy",
          link: "https://www.udemy.com/course/software-engineer-interview-preparation/",
          price: "$12.99",
          rating: 4.7,
          skill: "Interviewing",
          difficulty: "Intermediate"
        },
        {
          title: "System Design Interview",
          platform: "Educative",
          link: "https://www.educative.io/courses/grokking-the-system-design-interview",
          price: "$59",
          rating: 4.8,
          skill: "System Design",
          difficulty: "Advanced"
        },
        {
          title: "Cracking the Coding Interview",
          platform: "Amazon",
          link: "https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850",
          price: "$26.49",
          rating: 4.6,
          skill: "Coding",
          difficulty: "Intermediate"
        }
      ], "additional_resources": [
        {
          title: "LeetCode",
          type: "Practice Platform",
          link: "https://leetcode.com",
          description: "Practice coding problems and prepare for technical interviews",
          format: "Interactive"
        },
        {
          title: "HackerRank",
          type: "Practice Platform",
          link: "https://www.hackerrank.com",
          description: "Practice coding problems and compete in contests",
          format: "Interactive"
        }
      ]
    },
    "Machine Learning Engineer": {
      "courses": [
        {
          title: "Machine Learning Engineer Nanodegree",
          platform: "Udacity",
          link: "https://www.udacity.com/course/machine-learning-engineer-nanodegree--nd009t",
          price: "$399/month",
          rating: 4.6,
          skill: "Machine Learning",
          difficulty: "Intermediate"
        },
        {
          title: "Deep Learning Specialization",
          platform: "Coursera",
          link: "https://www.coursera.org/specializations/deep-learning",
          price: "$49/month",
          rating: 4.8,
          skill: "Deep Learning",
          difficulty: "Advanced"
        },
        {
          title: "Natural Language Processing Specialization",
          platform: "Coursera",
          link: "https://www.coursera.org/specializations/natural-language-processing",
          price: "$49/month",
          rating: 4.7,
          skill: "NLP",
          difficulty: "Advanced"
        }
      ], "additional_resources": [
        {
          title: "fast.ai",
          type: "Online Learning Platform",
          link: "https://www.fast.ai",
          description: "Practical deep learning for coders",
          format: "Interactive"
        },
        {
          title: "Kaggle",
          type: "Practice Platform",
          link: "https://www.kaggle.com",
          description: "Compete in machine learning challenges and build your data science portfolio",
          format: "Interactive"
        }
      ]
    },
  };

  const jobListings = {
    "Data Scientist": [
      {
        company: "TechCorp",
        title: "Senior Data Scientist",
        location: "San Francisco, CA",
        salary: "$140,000 - $180,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Python", "Machine Learning", "SQL", "AWS"]
      },
      {
        company: "AI Solutions",
        title: "Machine Learning Engineer",
        location: "Remote",
        salary: "$130,000 - $160,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["TensorFlow", "Python", "Deep Learning"]
      }
    ],
    "Data Analyst": [
      {
        company: "DataCo",
        title: "Business Intelligence Analyst",
        location: "New York, NY",
        salary: "$85,000 - $110,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["SQL", "Tableau", "Excel", "Python"]
      },
      {
        company: "Analytics Inc",
        title: "Data Analyst",
        location: "Chicago, IL",
        salary: "$75,000 - $95,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Power BI", "SQL", "Python"]
      }
    ],
    "Web Developer": [
      {
        company: "WebTech",
        title: "Frontend Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "JavaScript", "HTML/CSS"]
      },
      {
        company: "Digital Solutions",
        title: "Full Stack Developer",
        location: "Remote",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Node.js", "React", "MongoDB"]
      }
    ],
    "Frontend Developer": [
      {
        company: "WebTech",
        title: "Frontend Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "JavaScript", "HTML/CSS"]
      },
      {
        company: "Digital Solutions",
        title: "Full Stack Developer",
        location: "Remote",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Node.js", "React", "MongoDB"]
      }
    ],
    "Data Engineer": [
      {
        company: "DataCo",
        title: "Data Engineer",
        location: "San Francisco, CA",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Hadoop", "Spark", "SQL", "Python"]
      },
      {
        company: "Tech Solutions",
        title: "Big Data Engineer",
        location: "Remote",
        salary: "$130,000 - $160,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Kafka", "Hive", "AWS"]
      }
    ],
    "Software Engineer": [
      {
        company: "TechCorp",
        title: "Software Engineer",
        location: "San Francisco, CA",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Java", "Spring Boot", "SQL"]
      },
      {
        company: "WebTech",
        title: "Full Stack Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "Node.js", "MongoDB"]
      }
    ],
    "Machine Learning Engineer": [
      {
        company: "AI Solutions",
        title: "Machine Learning Engineer",
        location: "Remote",
        salary: "$130,000 - $160,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["TensorFlow", "Python", "Deep Learning"]
      },
      {
        company: "TechCorp",
        title: "Senior Machine Learning Engineer",
        location: "San Francisco, CA",
        salary: "$140,000 - $180,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Python", "Machine Learning", "AWS"]
      }
    ],
    "Senior Data Scientist": [
      {
        company: "TechCorp",
        title: "Senior Data Scientist",
        location: "San Francisco, CA",
        salary: "$140,000 - $180,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Python", "Machine Learning", "SQL", "AWS"]
      },
      {
        company: "AI Solutions",
        title: "Machine Learning Engineer",
        location: "Remote",
        salary: "$130,000 - $160,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["TensorFlow", "Python", "Deep Learning"]
      }
    ],
    "Senior Software Engineer": [
      {
        company: "TechCorp",
        title: "Senior Software Engineer",
        location: "San Francisco, CA",
        salary: "$140,000 - $180,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Java", "Spring Boot", "SQL"]
      },
      {
        company: "WebTech",
        title: "Full Stack Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "Node.js", "MongoDB"]
      }
    ],
    "Senior Frontend Developer": [
      {
        company: "WebTech",
        title: "Frontend Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "JavaScript", "HTML/CSS"]
      },
      {
        company: "Digital Solutions",
        title: "Full Stack Developer",
        location: "Remote",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Node.js", "React", "MongoDB"]
      }
    ],
    "Full Stack Software Engineer": [
      {
        company: "WebTech",
        title: "Frontend Developer",
        location: "Austin, TX",
        salary: "$100,000 - $130,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["React", "JavaScript", "HTML/CSS"]
      },
      {
        company: "Digital Solutions",
        title: "Full Stack Developer",
        location: "Remote",
        salary: "$120,000 - $150,000",
        link: "https://www.linkedin.com/jobs/",
        skills: ["Node.js", "React", "MongoDB"]
      }
    ],
  };

  useEffect(() => {
    console.log('Full recommendations:', recommendations);
  }, [recommendations]);

  if (!recommendations) {
    return <div className="loading">Loading recommendations...</div>;
  }

  const { 
    job_title = '', 
    confidence_score = 0,
    required_skills = [],
    learning_roadmap = {
      immediate: [],
      short_term: [],
      long_term: []
    }
  } = recommendations;


  const displayResources = defaultCourses[job_title] || {
    courses: [],
    additional_resources: []
  };


  const careerJobs = jobListings[job_title] || [];


  const getDifficultyColor = (difficulty) => {
    switch(difficulty?.toLowerCase()) {
      case 'beginner':
        return 'difficulty-beginner';
      case 'intermediate':
        return 'difficulty-intermediate';
      case 'advanced':
        return 'difficulty-advanced';
      default:
        return '';
    }
  };

  const getFormatIcon = (format) => {
    switch(format?.toLowerCase()) {
      case 'video':
        return '🎥';
      case 'text':
        return '📚';
      case 'interactive':
        return '💻';
      default:
        return '📌';
    }
  };

  return (
    <div className="roadmap-container">
      <button className="back-button" onClick={handleBack}>
        ← Back to Form
      </button>
      
      <div className="recommendation-header">
        <div className="role-container">
          <h4 className="recommended-label">Recommended Role</h4>
          <h1 className="role-title">{job_title}</h1>
          <div className="confidence-score">
            Match Score: {Math.round(confidence_score * 100)}%
          </div>
        </div>
      </div>

      <div className="gamification-panel">
        <div className="level-info">
          <h3>Career Progress</h3>
          <div className="level-container">
            <div className="level-circle">1</div>
            <div className="level-details">
              <span className="level-label">Level 1</span>
              <div className="progress-bar">
                <div className="progress" style={{ width: '45%' }}></div>
              </div>
              <span className="xp-text">450/1000 XP</span>
            </div>
          </div>
        </div>

        <div className="active-quests">
          <h3>Active Quests</h3>
          <div className="quest-list">
            <div className="quest-item">
              <div className="quest-info">
                <h4>Complete First Course</h4>
                <p>Finish your first recommended course</p>
              </div>
              <div className="quest-progress">
                <span className="xp-reward">+100 XP</span>
                <div className="progress-bar">
                  <div className="progress" style={{ width: '60%' }}></div>
                </div>
              </div>
            </div>
            <div className="quest-item">
              <div className="quest-info">
                <h4>Skill Master</h4>
                <p>Learn 3 new required skills</p>
              </div>
              <div className="quest-progress">
                <span className="xp-reward">+150 XP</span>
                <div className="progress-bar">
                  <div className="progress" style={{ width: '30%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="section-container">
        <h3 className="section-title">Required Skills</h3>
        <div className="skills-grid">
          {required_skills.map((skill, index) => (
            <div key={index} className="skill-card">
              {skill}
            </div>
          ))}
        </div>
      </div>

      <div className="section-container">
        <h3 className="section-title">Learning Path</h3>
        <div className="timeline">
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Immediate</h4>
              <span className="timeline-duration">0-2 weeks</span>
            </div>
            <ul>
              {learning_roadmap.immediate.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Short Term</h4>
              <span className="timeline-duration">2-4 weeks</span>
            </div>
            <ul>
              {learning_roadmap.short_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
          <div className="timeline-section">
            <div className="timeline-header">
              <h4 className="timeline-title">Long Term</h4>
              <span className="timeline-duration">1-2 months</span>
            </div>
            <ul>
              {learning_roadmap.long_term.map((skill, index) => (
                <li key={index}>{skill}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="section-container resources-container">
        
        <div className="courses-section">
          <h1 className="subsection-title">Recommended Courses</h1>
          <div className="courses-grid">
            {displayResources.courses.map((course, index) => (
              <a
                key={index}
                href={course.link}
                target="_blank"
                rel="noopener noreferrer"
                className="course-card"
              >
                <div className="course-content">
                  <div className="course-header">
                    <div className="course-platform">{course.platform}</div>
                    <div className={`difficulty ${getDifficultyColor(course.difficulty)}`}>
                      {course.difficulty}
                    </div>
                  </div>
                  <h5>{course.title}</h5>
                </div>
                <div className="course-footer">
                  <div className="course-details">
                    <span className="course-rating">★ {course.rating}</span>
                    <span className="course-price">{course.price}</span>
                  </div>
                  <div className="course-skill">
                    <span>{course.skill}</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>

        <div className="additional-resources">
          <h1>Additional Learning Resources</h1>
          <div className="resources-grid">
            {displayResources.additional_resources.map((resource, index) => (
              <a
                key={index}
                href={resource.link}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-card"
              >
                <div className="resource-header">
                  <div className="resource-type">{resource.type}</div>
                  <div className="resource-format">
                    {getFormatIcon(resource.format)} {resource.format}
                  </div>
                </div>
                <h5>{resource.title}</h5>
                <p className="resource-description">{resource.description}</p>
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="job-listings-section">
        <h1>Featured Job Opportunities</h1>
        <div className="jobs-grid">
          {careerJobs.map((job, index) => (
            <a
              key={index}
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="job-card"
            >
              <div className="job-header">
                <h4>{job.title}</h4>
                <div className="company-name">{job.company}</div>
              </div>
              <div className="job-details">
                <div className="detail-item">
                  <span className="icon">📍</span>
                  {job.location}
                </div>
                <div className="detail-item">
                  <span className="icon">💰</span>
                  {job.salary}
                </div>
              </div>
              <div className="job-skills">
                {job.skills.map((skill, i) => (
                  <span key={i} className="skill-tag">{skill}</span>
                ))}
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Roadmap; 