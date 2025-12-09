import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

// Common components
import LandingPage from './components/common/landing_page'
import LoginPage from './components/common/login'
import SignupPage from './components/common/signup'

// Student components
import StudentDashboard from './components/student/student_dashboard'
import AssignmentList from './components/student/assignment_list'
import AssignmentDetails from './components/student/assignment_details'
import ProjectsPage from './components/student/projects_page'
import ProjectDetails from './components/student/project_details'
import MasteryTracker from './components/student/mastery_tracker'
import BadgesPage from './components/student/badges'
import LeaderboardPage from './components/common/leaderboard'

// Teacher components
import TeacherDashboard from './components/teacher/teacher_dashboard'
import AnalyticsDashboard from './components/teacher/analytics_dashboard'
import AIContentGenerator from './components/teacher/ai_content_generator'
import ClassManagement from './components/teacher/class_management'
import StudentProgress from './components/teacher/student_progress'
import InterventionsPage from './components/teacher/interventions_page'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Common routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          
          {/* Student routes */}
          <Route path="/student/dashboard" element={<StudentDashboard />} />
          <Route path="/student/assignments" element={<AssignmentList />} />
          <Route path="/student/assignments/:id" element={<AssignmentDetails />} />
          <Route path="/student/projects" element={<ProjectsPage />} />
          <Route path="/student/projects/:id" element={<ProjectDetails />} />
          <Route path="/student/mastery" element={<MasteryTracker />} />
          <Route path="/student/badges" element={<BadgesPage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
          
          {/* Teacher routes */}
          <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
          <Route path="/teacher/analytics" element={<AnalyticsDashboard />} />
          <Route path="/teacher/ai-content" element={<AIContentGenerator />} />
          <Route path="/teacher/classes" element={<ClassManagement />} />
          <Route path="/teacher/students/:id" element={<StudentProgress />} />
          <Route path="/teacher/interventions" element={<InterventionsPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App