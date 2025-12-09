# AMEP Frontend (HTML Version)

## Overview
This directory contains the complete HTML frontend implementation for the AMEP platform. All pages have been converted from React components to standalone HTML files with Tailwind CSS styling.

## Directory Structure
```
frontend2/
├── pages/           # All HTML pages
├── components/      # Reusable HTML components
├── js/             # JavaScript files
├── NAVIGATION.md   # Navigation structure documentation
└── README.md       # This file
```

## Pages Included

### Common Pages
- `landing.html` - Main landing page
- `login.html` - User login page
- `signup.html` - User registration page

### Student Pages
- `student-dashboard.html` - Student main dashboard
- `mastery-tracker.html` - Track subject mastery levels
- `assignments.html` - List of assignments
- `assignment-details.html` - Detailed view of an assignment
- `projects.html` - List of projects
- `project-details.html` - Detailed view of a project
- `leaderboard.html` - Student ranking leaderboard
- `badges.html` - Earned and available badges

### Teacher Pages
- `teacher-dashboard.html` - Teacher main dashboard
- `ai-content-generator.html` - AI-powered content creation tool
- `classes.html` - Class management interface
- `student-progress.html` - Detailed student progress tracking
- `interventions.html` - Student intervention management
- `analytics.html` - Data analytics and reporting

## How to Use

1. **Open in Browser**: Simply open any HTML file directly in a web browser
2. **Navigation**: Use the navigation links in the header to move between pages
3. **Responsive Design**: All pages are mobile-responsive and work on all device sizes

## Features

- Dark theme UI with modern styling
- Responsive navigation (desktop and mobile)
- Breadcrumb navigation on authenticated pages
- Consistent branding and design language
- Interactive elements and hover effects
- Mobile-friendly hamburger menu

## Backend Integration

These HTML pages are designed to work with your backend API. To connect to your backend:

1. Add API endpoint URLs to each page where data is displayed
2. Implement AJAX calls using JavaScript to fetch and send data
3. Handle authentication tokens and session management
4. Update UI elements dynamically based on API responses

## Customization

To customize the frontend:

1. Modify the HTML files directly to change content
2. Update CSS classes to change styling
3. Add new JavaScript functionality in the js/ directory
4. Create new pages by copying existing ones as templates

## Dependencies

All pages use:
- Tailwind CSS (via CDN)
- Font Awesome (via CDN)
- Google Fonts

No build process is required - these are static HTML files.

## Navigation Structure

See `NAVIGATION.md` for a complete map of how all pages are connected.

## Browser Support

Works in all modern browsers (Chrome, Firefox, Safari, Edge).

## Notes

- All pages are standalone and don't require a web server to run
- Images are loaded from external sources (placeholders)
- Form submissions will need backend integration to function