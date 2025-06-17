// Global JavaScript for SMS Application

// Utility functions
const Utils = {
    // Show toast notification
    showToast(message, type = 'info') {
        const toastHtml = `
            <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Add toast to container
        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHtml;
        toastContainer.appendChild(toastElement.firstElementChild);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastElement.firstElementChild, {
            autohide: true,
            delay: 5000
        });
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.firstElementChild.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    },
    
    // Format phone number for display
    formatPhoneNumber(phoneNumber) {
        if (!phoneNumber) return 'N/A';
        
        // Add spacing for better readability
        if (phoneNumber.startsWith('+')) {
            return phoneNumber.replace(/(\+\d{1,3})(\d{3})(\d{3})(\d+)/, '$1 $2 $3 $4');
        }
        return phoneNumber;
    },
    
    // Validate phone number format
    isValidPhoneNumber(phoneNumber) {
        const cleaned = phoneNumber.replace(/[^+\d]/g, '');
        return /^\+\d{7,15}$/.test(cleaned);
    },
    
    // Copy text to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            this.showToast('Failed to copy to clipboard', 'danger');
        }
    },
    
    // Debounce function for input events
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    // Sanitize HTML to prevent XSS
    sanitizeHtml(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
};

// API helper functions
const API = {
    // Generic fetch wrapper with error handling
    async fetch(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Send SMS
    async sendSMS(phoneNumbers, message, sender = null) {
        return this.fetch('/api/send-sms', {
            method: 'POST',
            body: JSON.stringify({
                phone_numbers: phoneNumbers,
                message: message,
                sender: sender
            })
        });
    },
    
    // Upload phone numbers file
    async uploadPhoneNumbers(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        return fetch('/api/upload-phones', {
            method: 'POST',
            body: formData
        }).then(response => response.json());
    },
    
    // Get delivery reports
    async getReports(bulkId = null, limit = 50) {
        const params = new URLSearchParams();
        if (bulkId) params.append('bulk_id', bulkId);
        params.append('limit', limit);
        
        return this.fetch(`/api/reports?${params}`);
    },
    
    // Check account balance
    async getBalance() {
        return this.fetch('/api/balance');
    }
};

// Form validation helpers
const Validation = {
    // Validate form fields
    validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'This field is required');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
        });
        
        return isValid;
    },
    
    // Show field error
    showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        let errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            field.parentNode.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
    },
    
    // Clear field error
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorElement = field.parentNode.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    },
    
    // Validate phone numbers
    validatePhoneNumbers(phoneNumbers) {
        const errors = [];
        const validNumbers = [];
        
        phoneNumbers.forEach((number, index) => {
            const trimmed = number.trim();
            if (!trimmed) return;
            
            if (Utils.isValidPhoneNumber(trimmed)) {
                validNumbers.push(trimmed);
            } else {
                errors.push(`Line ${index + 1}: Invalid phone number format`);
            }
        });
        
        return { validNumbers, errors };
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // Don't show error toast for every error to avoid spam
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault();
});

// Make utilities available globally
window.Utils = Utils;
window.API = API;
window.Validation = Validation;

// Export for modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Utils, API, Validation };
}

