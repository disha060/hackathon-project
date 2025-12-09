# AMEP Frontend Navigation Structure

## Overview
This document outlines the complete navigation flow and page connections for the AMEP frontend HTML pages. All pages are located in the `/frontend2/pages/` directory.

## Authentication Flow
```
landing.html → login.html → student-dashboard.html OR teacher-dashboard.html
landing.html → signup.html → student-dashboard.html OR teacher-dashboard.html
```

## Student Navigation Flow
```
student-dashboard.html
├── mastery-tracker.html
├── assignments.html
│   └── assignment-details.html
├── projects.html
│   └── project-details.html
├── leaderboard.html
└── badges.html
```

## Teacher Navigation Flow
```
teacher-dashboard.html
├── ai-content-generator.html
├── classes.html
├── student-progress.html
├── interventions.html
└── analytics.html
```

## Page Connections Summary

### Common Pages
| Page | URL | Connected From | Connects To |
|------|-----|----------------|-------------|
| Landing Page | landing.html | Entry point | login.html, signup.html |
| Login Page | login.html | landing.html | student-dashboard.html, teacher-dashboard.html |
| Signup Page | signup.html | landing.html | student-dashboard.html, teacher-dashboard.html |

### Student Pages
| Page | URL | Connected From | Connects To |
|------|-----|----------------|-------------|
| Student Dashboard | student-dashboard.html | login.html, signup.html | All student pages |
| Mastery Tracker | mastery-tracker.html | student-dashboard.html | student-dashboard.html |
| Assignments | assignments.html | student-dashboard.html | assignment-details.html, student-dashboard.html |
| Assignment Details | assignment-details.html | assignments.html | assignments.html |
| Projects | projects.html | student-dashboard.html | project-details.html, student-dashboard.html |
| Project Details | project-details.html | projects.html | projects.html |
| Leaderboard | leaderboard.html | student-dashboard.html | student-dashboard.html |
| Badges | badges.html | student-dashboard.html | student-dashboard.html |

### Teacher Pages
| Page | URL | Connected From | Connects To |
|------|-----|----------------|-------------|
| Teacher Dashboard | teacher-dashboard.html | login.html, signup.html | All teacher pages |
| AI Content Generator | ai-content-generator.html | teacher-dashboard.html | teacher-dashboard.html |
| Classes | classes.html | teacher-dashboard.html | teacher-dashboard.html |
| Student Progress | student-progress.html | teacher-dashboard.html | teacher-dashboard.html |
| Interventions | interventions.html | teacher-dashboard.html | teacher-dashboard.html |
| Analytics | analytics.html | teacher-dashboard.html | teacher-dashboard.html |

## Implementation Notes

1. **Responsive Navigation**: All pages include mobile-friendly navigation menus that adapt to screen size.

2. **Breadcrumb Navigation**: Authenticated pages (all except landing, login, and signup) include breadcrumb navigation for easy orientation.

3. **Consistent Headers**: Each page type (student, teacher, landing) has a consistent header with appropriate navigation links.

4. **Active State Indicators**: The current page is highlighted in the navigation menu.

5. **Footer Navigation**: All pages include a comprehensive footer with links to major sections.

## URL Structure
All pages are accessed directly via their HTML files:
- Student Dashboard: `/frontend2/pages/student-dashboard.html`
- Teacher Dashboard: `/frontend2/pages/teacher-dashboard.html`
- etc.

## Backend Integration
These HTML pages are designed to work with the existing backend API endpoints. AJAX calls should be implemented in each page to communicate with the backend services.

## Future Enhancements
1. Implement client-side routing for smoother navigation
2. Add loading states for AJAX calls
3. Implement proper authentication flow with session management
4. Add offline capability with service workers