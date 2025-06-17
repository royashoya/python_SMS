/*
 * SMS Platform - Apple-Inspired JavaScript
 * Version 2.0
 * Enhanced functionality with smooth animations and modern UX
 */

// Global Application State
class SMSApp {
    constructor() {
        this.currentUploadedContacts = [];
        this.notifications = [];
        this.init();
    }
    
    init() {
        this.setupGlobalEventListeners();
        this.initPageSpecificFunctionality();
        this.setupFlashMessages();
    }
    
    // Enhanced notification system
    showNotification(message, type = 'info', duration = 5000) {
        const notificationId = Date.now();
        const notification = this.createNotificationElement(message, type, notificationId);
        
        const container = document.querySelector('.flash-messages') || this.createNotificationContainer();
        container.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        });
        
        // Auto-remove after duration
        setTimeout(() => this.removeNotification(notificationId), duration);
        
        return notificationId;
    }
    
    createNotificationContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }
    
    createNotificationElement(message, type, id) {
        const notification = document.createElement('div');
        notification.className = `flash-message flash-${type}`;
        notification.dataset.id = id;
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        notification.style.transition = 'all 0.3s ease-out';
        
        const iconMap = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        
        notification.innerHTML = `
            <div class="flash-content">
                <i class="fas fa-${iconMap[type] || 'info-circle'}"></i>
                <span>${message}</span>
                <button type="button" class="flash-close" onclick="smsApp.removeNotification(${id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        return notification;
    }
    
    removeNotification(id) {
        const notification = document.querySelector(`[data-id="${id}"]`);
        if (notification) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }
    }
    
    setupFlashMessages() {
        // Handle close buttons on existing flash messages
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('flash-close') || e.target.closest('.flash-close')) {
                const message = e.target.closest('.flash-message');
                if (message) {
                    message.style.transform = 'translateX(100%)';
                    message.style.opacity = '0';
                    setTimeout(() => message.remove(), 300);
                }
            }
        });
    }
    
    setupGlobalEventListeners() {
        // Mobile navigation toggle
        const navToggle = document.getElementById('navToggle');
        const navMenu = document.getElementById('navMenu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
                navMenu.classList.toggle('active');
                navToggle.setAttribute('aria-expanded', !isExpanded);
                
                // Animate hamburger lines
                const lines = navToggle.querySelectorAll('.hamburger-line');
                lines.forEach((line, index) => {
                    if (!isExpanded) {
                        if (index === 0) line.style.transform = 'rotate(45deg) translate(5px, 5px)';
                        if (index === 1) line.style.opacity = '0';
                        if (index === 2) line.style.transform = 'rotate(-45deg) translate(7px, -6px)';
                    } else {
                        line.style.transform = '';
                        line.style.opacity = '';
                    }
                });
            });
        }
        
        // Set active navigation link
        this.updateActiveNavigation();
    }
    
    updateActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }
    
    initPageSpecificFunctionality() {
        const path = window.location.pathname;
        
        if (path.includes('send-single') || path === '/send-single') {
            this.initSingleSMS();
        } else if (path.includes('send-bulk') || path === '/send-bulk') {
            this.initBulkSMS();
        } else if (path.includes('reports') || path === '/reports') {
            this.initReports();
        } else if (path.includes('balance') || path === '/balance') {
            this.initBalance();
        }
    }
    
    // Enhanced Single SMS functionality
    initSingleSMS() {
        const form = document.getElementById('singleSmsForm');
        if (!form) return;
        
        this.setupFormValidation(form);
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const phoneNumber = formData.get('phone_number')?.trim();
            const message = formData.get('message')?.trim();
            const sender = formData.get('sender')?.trim() || '';
            
            if (!this.validateSingleSMSForm(phoneNumber, message)) return;
            
            const submitBtn = form.querySelector('button[type="submit"]');
            this.setButtonLoading(submitBtn, 'Sending...');
            
            try {
                const result = await this.sendSMS({
                    phone_numbers: [this.formatPhoneNumber(phoneNumber)],
                    message,
                    sender
                });
                
                if (result.success) {
                    this.showNotification(
                        `Message sent successfully! Delivery tracking: ${result.bulk_id}`,
                        'success'
                    );
                    form.reset();
                    this.addSendAnimation(submitBtn);
                } else {
                    this.showNotification(`Failed to send: ${result.error}`, 'error');
                }
            } catch (error) {
                this.showNotification('Network error. Please try again.', 'error');
                console.error('SMS sending error:', error);
            } finally {
                this.resetButtonLoading(submitBtn, 'Send Message');
            }
        });
    }
    
    // Enhanced Bulk SMS functionality
    initBulkSMS() {
        const form = document.getElementById('bulkSmsForm');
        if (!form) return;
        
        this.setupFileUpload();
        this.setupFormValidation(form);
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const message = formData.get('message')?.trim();
            const sender = formData.get('sender')?.trim() || '';
            
            let phoneNumbers = this.getPhoneNumbers();
            
            if (!this.validateBulkSMSForm(message, phoneNumbers)) return;
            
            const submitBtn = form.querySelector('button[type="submit"]');
            this.setButtonLoading(submitBtn, 'Sending Bulk SMS...');
            
            try {
                const result = await this.sendSMS({
                    phone_numbers: phoneNumbers,
                    message,
                    sender
                });
                
                if (result.success) {
                    this.showNotification(
                        `Bulk SMS sent! ${result.successful}/${result.total_sent} delivered. ID: ${result.bulk_id}`,
                        'success',
                        8000
                    );
                    form.reset();
                    this.clearUploadedContacts();
                } else {
                    this.showNotification(`Bulk send failed: ${result.error}`, 'error');
                }
            } catch (error) {
                this.showNotification('Network error during bulk send.', 'error');
                console.error('Bulk SMS error:', error);
            } finally {
                this.resetButtonLoading(submitBtn, 'Send Bulk SMS');
            }
        });
    }
    
    setupFileUpload() {
        const fileInput = document.getElementById('phoneFile');
        const uploadArea = document.getElementById('uploadArea');
        
        if (!fileInput || !uploadArea) return;
        
        // Enhanced drag and drop
        uploadArea.addEventListener('click', () => fileInput.click());
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('dragover');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            }, false);
        });
        
        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileUpload(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
    }
    
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    async handleFileUpload(file) {
        if (!this.validateFileType(file)) {
            this.showNotification('Please upload a .txt or .csv file.', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/upload-phones', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentUploadedContacts = result.phone_numbers;
                this.showNotification(
                    `📱 ${result.count} contacts loaded from ${file.name}`,
                    'success'
                );
                this.updateContactsDisplay();
            } else {
                this.showNotification(`Upload failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification('File upload failed. Please try again.', 'error');
            console.error('File upload error:', error);
        }
    }
    
    validateFileType(file) {
        const allowedTypes = ['.txt', '.csv'];
        const fileName = file.name.toLowerCase();
        return allowedTypes.some(type => fileName.endsWith(type));
    }
    
    getPhoneNumbers() {
        if (this.currentUploadedContacts.length > 0) {
            return this.currentUploadedContacts;
        }
        
        const phoneTextarea = document.getElementById('phoneNumbers');
        if (!phoneTextarea) return [];
        
        return phoneTextarea.value
            .split('\n')
            .map(line => line.trim())
            .filter(line => line && this.validatePhoneNumber(line))
            .map(phone => this.formatPhoneNumber(phone));
    }
    
    updateContactsDisplay() {
        const container = document.getElementById('uploadedContacts');
        if (!container) return;
        
        if (this.currentUploadedContacts.length > 0) {
            const preview = this.currentUploadedContacts.slice(0, 3).join(', ');
            const remaining = this.currentUploadedContacts.length - 3;
            
            container.innerHTML = `
                <div class="contacts-preview">
                    <div class="contacts-header">
                        <span class="contacts-count">${this.currentUploadedContacts.length} contacts loaded</span>
                        <button type="button" class="btn btn-small btn-secondary" onclick="smsApp.clearUploadedContacts()">
                            Clear
                        </button>
                    </div>
                    <div class="contacts-list">
                        ${preview}${remaining > 0 ? ` and ${remaining} more...` : ''}
                    </div>
                </div>
            `;
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    }
    
    clearUploadedContacts() {
        this.currentUploadedContacts = [];
        this.updateContactsDisplay();
        
        const fileInput = document.getElementById('phoneFile');
        if (fileInput) fileInput.value = '';
        
        this.showNotification('Uploaded contacts cleared.', 'info', 3000);
    }
    
    // Reports functionality
    initReports() {
        const form = document.getElementById('reportsForm');
        if (!form) return;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const bulkId = formData.get('bulk_id')?.trim();
            const limit = formData.get('limit') || 50;
            
            const submitBtn = form.querySelector('button[type="submit"]');
            this.setButtonLoading(submitBtn, 'Loading...');
            
            try {
                const params = new URLSearchParams();
                if (bulkId) params.append('bulk_id', bulkId);
                params.append('limit', limit);
                
                const response = await fetch(`/api/reports?${params}`);
                const result = await response.json();
                
                if (result.success) {
                    this.displayReports(result.reports);
                    this.showNotification(
                        `Loaded ${result.reports?.length || 0} delivery reports`,
                        'success'
                    );
                } else {
                    this.showNotification(`Error loading reports: ${result.error}`, 'error');
                }
            } catch (error) {
                this.showNotification('Failed to load reports.', 'error');
                console.error('Reports error:', error);
            } finally {
                this.resetButtonLoading(submitBtn, 'Load Reports');
            }
        });
    }
    
    displayReports(reports) {
        const container = document.getElementById('reportsContainer');
        if (!container) return;
        
        if (!reports || reports.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 19c-5 0-8-3-8-8s3-8 8-8 8 3 8 8-3 8-8 8z"></path>
                        <path d="M17.9 20.9a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"></path>
                    </svg>
                    <h3>No Reports Found</h3>
                    <p>Try adjusting your search criteria or send some messages first.</p>
                </div>
            `;
            return;
        }
        
        const table = `
            <div class="reports-table">
                <div class="table-header">
                    <div class="table-cell">Recipient</div>
                    <div class="table-cell">Status</div>
                    <div class="table-cell">Message ID</div>
                    <div class="table-cell">Cost</div>
                    <div class="table-cell">Sent</div>
                    <div class="table-cell">Delivered</div>
                </div>
                <div class="table-body">
                    ${reports.map(report => `
                        <div class="table-row">
                            <div class="table-cell">${report.to || 'N/A'}</div>
                            <div class="table-cell">
                                <span class="status-badge status-${this.getStatusClass(report.status?.name)}">
                                    ${report.status?.name || 'Unknown'}
                                </span>
                            </div>
                            <div class="table-cell font-mono">${this.truncateId(report.messageId)}</div>
                            <div class="table-cell">${this.formatPrice(report.price)}</div>
                            <div class="table-cell">${this.formatDateTime(report.sentAt)}</div>
                            <div class="table-cell">${this.formatDateTime(report.doneAt)}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        container.innerHTML = table;
    }
    
    getStatusClass(status) {
        const statusMap = {
            'DELIVERED': 'success',
            'PENDING': 'warning',
            'EXPIRED': 'error',
            'REJECTED': 'error',
            'UNDELIVERABLE': 'error'
        };
        return statusMap[status] || 'secondary';
    }
    
    truncateId(id) {
        if (!id) return 'N/A';
        return id.length > 12 ? id.substring(0, 12) + '...' : id;
    }
    
    formatPrice(price) {
        if (!price || !price.pricePerMessage) return 'N/A';
        return `${price.pricePerMessage} ${price.currency || ''}`;
    }
    
    // Balance functionality
    initBalance() {
        this.loadBalance();
    }
    
    async loadBalance() {
        const container = document.getElementById('balanceContainer');
        if (!container) return;
        
        // Show loading state
        container.innerHTML = `
            <div class="loading-state">
                <div class="pulse"></div>
                <p>Loading balance information...</p>
            </div>
        `;
        
        try {
            const response = await fetch('/api/balance');
            const result = await response.json();
            
            if (result.success) {
                this.displayBalance(result.balance);
            } else {
                container.innerHTML = `
                    <div class="error-state">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="15" y1="9" x2="9" y2="15"></line>
                            <line x1="9" y1="9" x2="15" y2="15"></line>
                        </svg>
                        <h3>Unable to Load Balance</h3>
                        <p>${result.error}</p>
                        <button class="btn btn-primary" onclick="smsApp.loadBalance()">Try Again</button>
                    </div>
                `;
            }
        } catch (error) {
            container.innerHTML = `
                <div class="error-state">
                    <h3>Connection Error</h3>
                    <p>Please check your internet connection and try again.</p>
                    <button class="btn btn-primary" onclick="smsApp.loadBalance()">Retry</button>
                </div>
            `;
            console.error('Balance loading error:', error);
        }
    }
    
    displayBalance(balance) {
        const container = document.getElementById('balanceContainer');
        if (!container) return;
        
        const balanceHtml = `
            <div class="balance-cards grid grid-2">
                <div class="card balance-card fade-in">
                    <div class="balance-amount">
                        <span class="currency">${balance.currency || '$'}</span>
                        <span class="amount">${balance.balance || '0.00'}</span>
                    </div>
                    <div class="balance-label">Available Balance</div>
                </div>
                
                <div class="card account-info fade-in">
                    <h3 class="card-title">Account Details</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Account ID</span>
                            <span class="value">${balance.accountId || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Account Name</span>
                            <span class="value">${balance.name || 'N/A'}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Currency</span>
                            <span class="value">${balance.currency || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = balanceHtml;
        
        // Trigger animations
        setTimeout(() => {
            container.querySelectorAll('.fade-in').forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        }, 100);
    }
    
    // Utility functions
    formatPhoneNumber(phone) {
        const cleaned = phone.replace(/\D/g, '');
        if (!cleaned.startsWith('1') && cleaned.length === 10) {
            return '1' + cleaned;
        }
        return cleaned;
    }
    
    validatePhoneNumber(phone) {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.length >= 10 && cleaned.length <= 15;
    }
    
    validateSingleSMSForm(phone, message) {
        if (!phone || !message) {
            this.showNotification('Please fill in all required fields.', 'error');
            return false;
        }
        
        if (!this.validatePhoneNumber(phone)) {
            this.showNotification('Please enter a valid phone number.', 'error');
            return false;
        }
        
        return true;
    }
    
    validateBulkSMSForm(message, phoneNumbers) {
        if (!message) {
            this.showNotification('Please enter a message.', 'error');
            return false;
        }
        
        if (phoneNumbers.length === 0) {
            this.showNotification('Please provide phone numbers.', 'error');
            return false;
        }
        
        return true;
    }
    
    async sendSMS(data) {
        const response = await fetch('/api/send-sms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        return await response.json();
    }
    
    setButtonLoading(button, text) {
        button.dataset.originalText = button.textContent;
        button.innerHTML = `<span class="loading-spinner"></span>${text}`;
        button.disabled = true;
        button.classList.add('loading');
    }
    
    resetButtonLoading(button, fallbackText) {
        const originalText = button.dataset.originalText || fallbackText;
        button.textContent = originalText;
        button.disabled = false;
        button.classList.remove('loading');
    }
    
    addSendAnimation(button) {
        button.style.transform = 'scale(1.05)';
        button.style.backgroundColor = 'var(--color-success)';
        
        setTimeout(() => {
            button.style.transform = '';
            button.style.backgroundColor = '';
        }, 200);
    }
    
    formatDateTime(dateString) {
        if (!dateString) return 'N/A';
        
        try {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
        } catch (error) {
            return 'Invalid Date';
        }
    }
    
    setupFormValidation(form) {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';
        
        if (field.required && !value) {
            isValid = false;
            message = 'This field is required';
        } else if (field.type === 'tel' && value && !this.validatePhoneNumber(value)) {
            isValid = false;
            message = 'Please enter a valid phone number';
        }
        
        this.setFieldValidation(field, isValid, message);
        return isValid;
    }
    
    setFieldValidation(field, isValid, message) {
        const wrapper = field.closest('.form-group');
        if (!wrapper) return;
        
        // Remove existing validation
        wrapper.querySelectorAll('.field-error').forEach(error => error.remove());
        field.classList.remove('error');
        
        if (!isValid) {
            field.classList.add('error');
            const errorEl = document.createElement('div');
            errorEl.className = 'field-error';
            errorEl.textContent = message;
            wrapper.appendChild(errorEl);
        }
    }
    
    clearFieldError(field) {
        const wrapper = field.closest('.form-group');
        if (wrapper) {
            wrapper.querySelectorAll('.field-error').forEach(error => error.remove());
            field.classList.remove('error');
        }
    }
}

// Initialize the application
let smsApp;
document.addEventListener('DOMContentLoaded', () => {
    smsApp = new SMSApp();
});

