const API_BASE_URL = 'http://localhost:8000';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('auth_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('auth_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('auth_token');
    }

    getAuthHeader() {
        return this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...this.getAuthHeader(),
            ...options.headers,
        };

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers,
            });

            if (response.status === 401) {
                this.clearToken();
                window.location.href = '/login.html';
                return null;
            }

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async login(email, password) {
        const data = await this.request('/student/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        if (data && data.access_token) {
            this.setToken(data.access_token);
            return this.getCurrentUser();
        }
        return null;
    }

    async getCurrentUser() {
        return this.request('/student/me');
    }

    // Assignment endpoints
    async getAssignments(status) {
        const query = status ? `?status=${status}` : '';
        return this.request(`/student/assignments${query}`);
    }

    async getAssignmentDetails(assignmentId) {
        return this.request(`/student/assignments/${assignmentId}`);
    }

    async submitAssignment(assignmentId, submissionUrl, notes = '') {
        return this.request(`/student/assignments/${assignmentId}/submit`, {
            method: 'POST',
            body: JSON.stringify({
                student_id: (await this.getCurrentUser()).id,
                submission_url: submissionUrl,
                submission_notes: notes
            })
        });
    }

    // Teacher endpoints
    async assignToClass(classId, assignmentData) {
        return this.request(`/teacher/assignments/class/${classId}`, {
            method: 'POST',
            body: JSON.stringify(assignmentData)
        });
    }

    async getClassAssignments(classId) {
        return this.request(`/teacher/classes/${classId}/assignments`);
    }

    async getAssignmentSubmissions(assignmentId, classId = null) {
        const query = classId ? `?class_id=${classId}` : '';
        return this.request(`/teacher/assignments/${assignmentId}/submissions${query}`);
    }
}

export const apiService = new ApiService();
