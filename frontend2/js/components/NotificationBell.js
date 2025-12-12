class NotificationBell {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.notificationCount = 0;
        this.notificationList = null;
        this.isOpen = false;
        
        this.init();
    }
    
    async init() {
        this.render();
        await this.loadNotifications();
        this.setupEventListeners();
        
        // Poll for new notifications every 30 seconds
        setInterval(() => this.loadNotifications(), 30000);
    }
    
    render() {
        this.container.innerHTML = `
            <div class="notification-bell">
                <button class="notification-button" aria-label="Notifications">
                    <i class="fas fa-bell"></i>
                    ${this.notificationCount > 0 ? 
                        `<span class="notification-badge">${this.notificationCount}</span>` : ''}
                </button>
                <div class="notification-dropdown">
                    <div class="notification-header">
                        <h4>Notifications</h4>
                        <button class="mark-all-read">Mark all as read</button>
                    </div>
                    <div class="notification-list">
                        <div class="notification-empty">No new notifications</div>
                    </div>
                    <div class="notification-footer">
                        <a href="/notifications.html">View all notifications</a>
                    </div>
                </div>
            </div>
        `;
        
        this.notificationList = this.container.querySelector('.notification-list');
    }
    
    async loadNotifications() {
        try {
            const response = await fetch('/api/notifications?unread=true&limit=5');
            const notifications = await response.json();
            
            this.notificationCount = notifications.length;
            this.updateBadge();
            this.renderNotifications(notifications);
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }
    
    renderNotifications(notifications) {
        if (notifications.length === 0) {
            this.notificationList.innerHTML = `
                <div class="notification-empty">No new notifications</div>
            `;
            return;
        }
        
        this.notificationList.innerHTML = notifications.map(notification => `
            <div class="notification-item ${notification.is_read ? 'read' : 'unread'}" 
                 data-id="${notification.id}">
                <div class="notification-icon">
                    <i class="fas ${this.getNotificationIcon(notification.notification_type)}"></i>
                </div>
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-message">${notification.message}</div>
                    <div class="notification-time">${this.formatTimeAgo(notification.created_at)}</div>
                </div>
            </div>
        `).join('');
    }
    
    getNotificationIcon(type) {
        const icons = {
            'assignment_submission': 'fa-file-upload',
            'announcement': 'fa-bullhorn',
            'grade': 'fa-star',
            'system': 'fa-info-circle'
        };
        return icons[type] || 'fa-bell';
    }
    
    formatTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const seconds = Math.floor((now - date) / 1000);
        
        const intervals = {
            year: 31536000,
            month: 2592000,
            week: 604800,
            day: 86400,
            hour: 3600,
            minute: 60
        };
        
        for (const [unit, secondsInUnit] of Object.entries(intervals)) {
            const interval = Math.floor(seconds / secondsInUnit);
            if (interval >= 1) {
                return interval === 1 ? `1 ${unit} ago` : `${interval} ${unit}s ago`;
            }
        }
        
        return 'Just now';
    }
    
    updateBadge() {
        const badge = this.container.querySelector('.notification-badge');
        const button = this.container.querySelector('.notification-button');
        
        if (this.notificationCount > 0) {
            if (badge) {
                badge.textContent = this.notificationCount > 9 ? '9+' : this.notificationCount;
            } else {
                button.insertAdjacentHTML('beforeend', 
                    `<span class="notification-badge">${this.notificationCount > 9 ? '9+' : this.notificationCount}</span>`
                );
            }
            button.classList.add('has-notifications');
        } else {
            if (badge) {
                badge.remove();
            }
            button.classList.remove('has-notifications');
        }
    }
    
    setupEventListeners() {
        // Toggle dropdown
        this.container.querySelector('.notification-button').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown();
        });
        
        // Mark all as read
        this.container.querySelector('.mark-all-read')?.addEventListener('click', (e) => {
            e.stopPropagation();
            this.markAllAsRead();
        });
        
        // Mark as read when clicking a notification
        this.notificationList.addEventListener('click', (e) => {
            const notificationItem = e.target.closest('.notification-item');
            if (notificationItem) {
                const notificationId = notificationItem.dataset.id;
                this.markAsRead(notificationId);
                
                // Navigate to relevant page
                // You can customize this based on notification type
                const notificationType = notificationItem.dataset.type;
                if (notificationType === 'assignment_submission') {
                    const assignmentId = notificationItem.dataset.assignmentId;
                    window.location.href = `/teacher/assignments/${assignmentId}/submissions`;
                }
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.closeDropdown();
            }
        });
    }
    
    toggleDropdown() {
        this.isOpen ? this.closeDropdown() : this.openDropdown();
    }
    
    openDropdown() {
        this.container.classList.add('open');
        this.isOpen = true;
    }
    
    closeDropdown() {
        this.container.classList.remove('open');
        this.isOpen = false;
    }
    
    async markAsRead(notificationId) {
        try {
            await fetch(`/api/notifications/${notificationId}/read`, { method: 'POST' });
            const item = this.notificationList.querySelector(`[data-id="${notificationId}"]`);
            if (item) {
                item.classList.remove('unread');
                item.classList.add('read');
                this.updateNotificationCount(-1);
            }
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }
    
    async markAllAsRead() {
        try {
            await fetch('/api/notifications/read-all', { method: 'POST' });
            this.notificationList.querySelectorAll('.unread').forEach(item => {
                item.classList.remove('unread');
                item.classList.add('read');
            });
            this.updateNotificationCount(-this.notificationCount);
        } catch (error) {
            console.error('Error marking all notifications as read:', error);
        }
    }
    
    updateNotificationCount(delta) {
        this.notificationCount = Math.max(0, this.notificationCount + delta);
        this.updateBadge();
    }
}

// Initialize the notification bell if the container exists
document.addEventListener('DOMContentLoaded', () => {
    const notificationContainer = document.getElementById('notification-container');
    if (notificationContainer) {
        new NotificationBell('notification-container');
    }
});
