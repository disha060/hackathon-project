const API_BASE_URL = 'http://localhost:8000'; // Adjust this to your backend URL

// Helper function for API requests
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Set default headers
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  // Merge headers
  const headers = {
    ...defaultHeaders,
    ...options.headers,
  };
  
  // Add authorization token if available
  const token = localStorage.getItem('authToken');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  // Create fetch options
  const fetchOptions = {
    ...options,
    headers,
  };
  
  try {
    const response = await fetch(url, fetchOptions);
    
    // Handle unauthorized access
    if (response.status === 401) {
      // Clear auth token and redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('userRole');
      window.location.href = '/frontend2/pages/login.html';
      return;
    }
    
    // Handle successful responses
    if (response.ok) {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return await response.text();
      }
    }
    
    // Handle error responses
    let errorMessage = `HTTP Error: ${response.status}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch (parseError) {
      // If we can't parse the error response, use the status text
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  } catch (error) {
    console.error(`API request failed: ${error.message}`);
    throw error;
  }
}

// Auth endpoints
export const authAPI = {
  signup: (userData) => apiRequest('/student/signup', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  login: (credentials) => apiRequest('/student/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),
};

// Student endpoints
export const studentAPI = {
  getMastery: () => apiRequest('/student/mastery'),
  
  getAssignments: (studentId) => apiRequest(`/student/assignments?student_id=${studentId}`),
  
  getAssignmentById: (assignmentId) => apiRequest(`/student/assignments/${assignmentId}`),
  
  submitAssignment: (studentId, assignmentId) => apiRequest('/student/assignments/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `student_id=${studentId}&assignment_id=${assignmentId}`,
  }),
  
  logEngagement: (engagementData) => apiRequest('/student/engagement', {
    method: 'POST',
    body: JSON.stringify(engagementData),
  }),
  
  getProjects: (studentId) => apiRequest(`/student/projects?student_id=${studentId}`),
  
  getLeaderboard: () => apiRequest('/student/leaderboard'),
  
  getBadges: (studentId) => apiRequest(`/student/badges?student_id=${studentId}`),
};

// Teacher endpoints
export const teacherAPI = {
  getAIAssignments: (conceptId, apiKey = null) => {
    const params = new URLSearchParams({ concept_id: conceptId });
    if (apiKey) params.append('api_key', apiKey);
    return apiRequest(`/teacher/ai/assignments?${params.toString()}`);
  },
  
  createAssignments: (assignments) => apiRequest('/teacher/assignments/create', {
    method: 'POST',
    body: JSON.stringify(assignments),
  }),
  
  getAIProjects: (skillArea, apiKey = null) => {
    const params = new URLSearchParams({ skill_area: skillArea });
    if (apiKey) params.append('api_key', apiKey);
    return apiRequest(`/teacher/ai/projects?${params.toString()}`);
  },
  
  createProjects: (projects) => apiRequest('/teacher/projects/create', {
    method: 'POST',
    body: JSON.stringify(projects),
  }),
  
  getDashboard: (teacherId) => apiRequest(`/teacher/dashboard?teacher_id=${teacherId}`),
  
  getInterventions: (teacherId) => apiRequest(`/teacher/interventions?teacher_id=${teacherId}`),
  
  createIntervention: (interventionData) => apiRequest('/teacher/intervene', {
    method: 'POST',
    body: JSON.stringify(interventionData),
  }),
  
  // Class management endpoints
  createClass: (classData) => apiRequest('/classes/', {
    method: 'POST',
    body: JSON.stringify(classData),
  }),
  
  getClasses: (teacherId) => apiRequest(`/classes/?teacher_id=${teacherId}`),
  
  getClassById: (classId) => apiRequest(`/classes/${classId}`),
  
  enrollStudent: (classId, enrollmentData) => apiRequest(`/classes/${classId}/enroll`, {
    method: 'POST',
    body: JSON.stringify(enrollmentData),
  }),
  
  getClassStudents: (classId) => apiRequest(`/classes/${classId}/students`),
  
  assignProjectToClass: (classId, projectData) => apiRequest(`/classes/${classId}/assign-project`, {
    method: 'POST',
    body: JSON.stringify(projectData),
  }),
  
  assignAssignmentToClass: (classId, assignmentData) => apiRequest(`/classes/${classId}/assign-assignment`, {
    method: 'POST',
    body: JSON.stringify(assignmentData),
  }),
  
  getClassProjects: (classId) => apiRequest(`/classes/${classId}/projects`),
  
  getClassAssignments: (classId) => apiRequest(`/classes/${classId}/assignments`),
};
