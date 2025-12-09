// API service to communicate with the backend
const API_BASE_URL = 'http://localhost:8000';

// User authentication endpoints
export const authAPI = {
  signup: (userData) => {
    return fetch(`${API_BASE_URL}/student/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
  },
  
  login: (credentials) => {
    return fetch(`${API_BASE_URL}/student/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
  },
};

// Student endpoints
export const studentAPI = {
  getMastery: () => {
    return fetch(`${API_BASE_URL}/student/mastery`);
  },
  
  getAssignments: (studentId) => {
    return fetch(`${API_BASE_URL}/student/assignments?student_id=${studentId}`);
  },
  
  submitAssignment: (studentId, assignmentId) => {
    return fetch(`${API_BASE_URL}/student/assignments/submit?student_id=${studentId}&assignment_id=${assignmentId}`, {
      method: 'POST',
    });
  },
  
  getProjects: () => {
    return fetch(`${API_BASE_URL}/student/projects`);
  },
  
  getLeaderboard: () => {
    return fetch(`${API_BASE_URL}/student/leaderboard`);
  },
  
  getBadges: (studentId) => {
    return fetch(`${API_BASE_URL}/student/badges?student_id=${studentId}`);
  },
  
  logEngagement: (engagementData) => {
    return fetch(`${API_BASE_URL}/student/engagement`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(engagementData),
    });
  },
};

// Teacher endpoints
export const teacherAPI = {
  getAIAssignments: (conceptId, apiKey) => {
    const url = apiKey 
      ? `${API_BASE_URL}/teacher/ai/assignments?concept_id=${conceptId}&api_key=${apiKey}`
      : `${API_BASE_URL}/teacher/ai/assignments?concept_id=${conceptId}`;
      
    return fetch(url);
  },
  
  createAssignments: (assignments) => {
    return fetch(`${API_BASE_URL}/teacher/assignments/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(assignments),
    });
  },
  
  getAIProjects: (skillArea, apiKey) => {
    const url = apiKey 
      ? `${API_BASE_URL}/teacher/ai/projects?skill_area=${skillArea}&api_key=${apiKey}`
      : `${API_BASE_URL}/teacher/ai/projects?skill_area=${skillArea}`;
      
    return fetch(url);
  },
  
  createProjects: (projects) => {
    return fetch(`${API_BASE_URL}/teacher/projects/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(projects),
    });
  },
  
  getDashboard: (teacherId) => {
    return fetch(`${API_BASE_URL}/teacher/dashboard?teacher_id=${teacherId}`);
  },
  
  getInterventions: (teacherId) => {
    return fetch(`${API_BASE_URL}/teacher/interventions?teacher_id=${teacherId}`);
  },
  
  intervene: (interventionData) => {
    return fetch(`${API_BASE_URL}/teacher/intervene`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(interventionData),
    });
  },
  
  scoreSoftSkills: (scores) => {
    return fetch(`${API_BASE_URL}/teacher/softskills/score`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(scores),
    });
  },
};