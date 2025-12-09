// Global navigation functionality for AMEP frontend

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle functionality
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const closeMobileNav = document.getElementById('close-mobile-nav');
    const mobileNavOverlay = document.getElementById('mobile-nav-overlay');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            if (mobileNavOverlay) {
                mobileNavOverlay.classList.remove('hidden');
            }
        });
    }
    
    if (closeMobileNav) {
        closeMobileNav.addEventListener('click', function() {
            if (mobileNavOverlay) {
                mobileNavOverlay.classList.add('hidden');
            }
        });
    }
    
    // Close mobile menu when clicking on a link
    if (mobileNavOverlay) {
        const mobileLinks = mobileNavOverlay.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileNavOverlay.classList.add('hidden');
            });
        });
    }
    
    // Highlight active nav link
    highlightActiveNavLink();
    
    // Breadcrumb navigation
    updateBreadcrumb();
});

// Function to highlight active navigation link
function highlightActiveNavLink() {
    const currentPage = getCurrentPageName();
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('text-white', 'font-medium');
        link.classList.add('text-gray-300');
        
        // Map pages to their respective nav items
        const pageMap = {
            'student-dashboard.html': 'dashboard',
            'mastery-tracker.html': 'mastery',
            'assignments.html': 'assignments',
            'assignment-details.html': 'assignments',
            'projects.html': 'projects',
            'project-details.html': 'projects',
            'leaderboard.html': 'leaderboard',
            'badges.html': 'badges',
            'teacher-dashboard.html': 'dashboard',
            'ai-content-generator.html': 'content',
            'classes.html': 'classes',
            'student-progress.html': 'progress',
            'interventions.html': 'interventions',
            'analytics.html': 'analytics'
        };
        
        const pageKey = pageMap[currentPage];
        if (link.getAttribute('data-page') === pageKey) {
            link.classList.remove('text-gray-300');
            link.classList.add('text-white', 'font-medium');
        }
    });
}

// Function to update breadcrumb navigation
function updateBreadcrumb() {
    const breadcrumbNav = document.getElementById('breadcrumb-nav');
    const breadcrumbCurrent = document.getElementById('breadcrumb-current');
    
    if (!breadcrumbNav || !breadcrumbCurrent) return;
    
    // Mapping of pages to breadcrumb names
    const breadcrumbMap = {
        'student-dashboard.html': 'Student Dashboard',
        'mastery-tracker.html': 'Mastery Tracker',
        'assignments.html': 'Assignments',
        'assignment-details.html': 'Assignment Details',
        'projects.html': 'Projects',
        'project-details.html': 'Project Details',
        'leaderboard.html': 'Leaderboard',
        'badges.html': 'Badges',
        'teacher-dashboard.html': 'Teacher Dashboard',
        'ai-content-generator.html': 'AI Content Generator',
        'classes.html': 'Class Management',
        'student-progress.html': 'Student Progress',
        'interventions.html': 'Interventions',
        'analytics.html': 'Analytics'
    };
    
    // Get current page
    const currentPage = getCurrentPageName();
    
    // Show breadcrumb for authenticated pages only
    if (currentPage !== 'landing.html' && currentPage !== 'login.html' && currentPage !== 'signup.html') {
        breadcrumbNav.classList.remove('hidden');
        
        // Set current page name
        if (breadcrumbMap[currentPage]) {
            breadcrumbCurrent.textContent = breadcrumbMap[currentPage];
        } else {
            breadcrumbCurrent.textContent = 'Page';
        }
    }
}

// Helper function to get current page name
function getCurrentPageName() {
    return window.location.pathname.split('/').pop();
}

// Function to show the correct header based on current page
function showCorrectHeader() {
    // Hide all headers
    const studentHeader = document.getElementById('student-header');
    const teacherHeader = document.getElementById('teacher-header');
    const landingHeader = document.getElementById('landing-header');
    
    if (studentHeader) studentHeader.classList.add('hidden');
    if (teacherHeader) teacherHeader.classList.add('hidden');
    if (landingHeader) landingHeader.classList.add('hidden');
    
    // Get current page filename
    const currentPage = getCurrentPageName();
    
    // Show appropriate header based on page
    if (currentPage === 'landing.html' && landingHeader) {
        landingHeader.classList.remove('hidden');
    } else if (['student-dashboard.html', 'mastery-tracker.html', 'assignments.html', 'assignment-details.html', 
                 'projects.html', 'project-details.html', 'leaderboard.html', 'badges.html'].includes(currentPage) && studentHeader) {
        studentHeader.classList.remove('hidden');
        // Highlight active nav link
        highlightActiveNavLink();
    } else if (['teacher-dashboard.html', 'ai-content-generator.html', 'classes.html', 'student-progress.html', 
                 'interventions.html', 'analytics.html'].includes(currentPage) && teacherHeader) {
        teacherHeader.classList.remove('hidden');
        // Highlight active nav link
        highlightActiveNavLink();
    }
}