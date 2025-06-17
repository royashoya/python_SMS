# 📱 SMS Web Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**A modern, feature-rich web application for SMS messaging using the Infobip API**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Screenshots](#-screenshots) • [API](#-api-reference)

</div>

---

## 🌟 Overview

The SMS Web Application is a comprehensive, modern web interface built with Flask that provides both individual and bulk SMS messaging capabilities through the Infobip API. It features a responsive design, real-time progress tracking, file upload support, and detailed delivery reporting.

### 💡 Why This Application?

- **User-Friendly**: Clean, intuitive web interface accessible to non-technical users
- **Dual Interface**: Both command-line and web interfaces available
- **Enterprise-Ready**: Robust error handling, validation, and security features
- **Mobile-Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Production-Ready**: Comprehensive logging, monitoring, and deployment options

---

## ✨ Features

### 🎯 Core Functionality
- **📱 Single SMS**: Send messages to individual recipients with custom sender ID
- **📢 Bulk SMS**: Send to multiple recipients (up to 100 per batch)
- **📁 File Upload**: Support for .txt and .csv phone number files (drag & drop)
- **📊 Delivery Reports**: Real-time tracking with detailed status information
- **💰 Account Balance**: Monitor your Infobip account balance and usage
- **🔍 Search & Filter**: Advanced filtering options for delivery reports

### 🎨 User Interface
- **🎨 Modern Design**: Clean, professional Bootstrap 5 interface
- **📱 Responsive Layout**: Optimized for all screen sizes and devices
- **⚡ Real-time Updates**: Live progress bars and status indicators
- **🌙 Professional Theme**: Consistent color scheme and typography
- **🔔 Toast Notifications**: Non-intrusive success/error messages
- **📈 Visual Analytics**: Charts and statistics for campaign results

### 🛡️ Security & Validation
- **🔒 Secure File Handling**: Temporary uploads with automatic cleanup
- **✅ Input Validation**: Phone number format and message length validation
- **🛡️ XSS Protection**: Sanitized inputs and secure form handling
- **🔐 API Security**: Secure credential management (never exposed to frontend)
- **📝 Audit Logging**: Comprehensive logging for monitoring and debugging

### 🚀 Technical Features
- **⚡ Asynchronous Processing**: Non-blocking file uploads and SMS sending
- **🔄 Progress Tracking**: Real-time progress indicators for bulk operations
- **📊 Detailed Analytics**: Success rates, delivery statistics, and timing
- **🔧 Error Recovery**: Graceful error handling with detailed error messages
- **📱 Mobile-First**: Optimized for mobile usage and touch interfaces

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed on your system
- **Infobip account** with API credentials
- **Modern web browser** (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/python_SMS.git
cd python_SMS

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy configuration template
cp config_template.py config.py
```

Edit `config.py` with your Infobip credentials:
```python
API_BASE_URL = "https://xxxxx.api.infobip.com"  # Your Infobip base URL
SENDER_ID = "YourSenderID"                      # Your approved sender ID
API_KEY = "your-api-key-here"                   # Your Infobip API key
```

### 3. Launch Web Application

```bash
# Start the web server
python app.py
```

🎉 **Access your application at:** `http://localhost:5001`

---

## 📖 Documentation

### 🌐 Web Interface Guide

#### Dashboard
The main dashboard provides quick access to all features:
- **Feature Cards**: Visual overview of available functions
- **Quick Stats**: At-a-glance information about supported formats
- **Navigation Menu**: Easy access to all sections

#### Single SMS
1. Navigate to **Send Single SMS**
2. Enter recipient phone number (with country code: `+1234567890`)
3. Compose your message (up to 1600 characters)
4. Optionally set custom sender ID
5. Click **Send SMS**
6. View results in popup modal

#### Bulk SMS
1. Navigate to **Send Bulk SMS**
2. Choose input method:
   - **Manual Input**: Type/paste phone numbers (one per line)
   - **File Upload**: Upload .txt or .csv file
3. Compose your message
4. Optionally set custom sender ID
5. Click **Send Bulk SMS**
6. Monitor real-time progress
7. Review detailed results with success/failure breakdown

#### File Upload Support
**Supported Formats:**
- **.txt files**: One phone number per line
- **.csv files**: Phone numbers in first column

**Example .txt file:**
```text
+1234567890
+1987654321
+254700000000
```

**Example .csv file:**
```csv
+1234567890,John Doe
+1987654321,Jane Smith
+254700000000,Bob Johnson
```

#### Delivery Reports
1. Navigate to **Reports**
2. Optionally filter by:
   - Bulk ID (from previous campaigns)
   - Number of reports to display (10, 25, 50, 100)
3. Click **Apply Filter** or **Refresh**
4. View detailed status information:
   - Phone numbers
   - Delivery status (Pending, Delivered, Failed)
   - Timestamps
   - Message IDs
   - Pricing information

#### Account Balance
1. Navigate to **Balance**
2. Click **Refresh** to check current balance
3. View balance details and usage tips

**Note:** Balance checking requires additional API permissions. Contact Infobip support if needed.

### 📊 Understanding SMS Status

| Status | Description | Icon |
|--------|-------------|------|
| **PENDING** | Message accepted and queued | 🟡 |
| **DELIVERED** | Successfully delivered | 🟢 |
| **UNDELIVERED** | Failed to deliver | 🔴 |
| **EXPIRED** | Message expired | ⚪ |
| **REJECTED** | Message rejected | 🔴 |
| **UNKNOWN** | Status unknown | ⚫ |

---

## 💻 Command Line Interface

For advanced users and automation, use the command-line interface:

### Command Line Interface

#### Send a single SMS:
```bash
python3 sms_application.py -t "+1234567890" -m "Hello, World!"
```

#### Send bulk SMS to multiple numbers:
```bash
python3 sms_application.py -t "+1234567890,+0987654321" -m "Bulk message"
```

#### Send SMS from a file of phone numbers:
```bash
python3 sms_application.py -f phone_numbers.txt -m "Message from file"
```

#### Check account balance:
```bash
python3 sms_application.py --balance
```

#### Get delivery reports:
```bash
python3 sms_application.py --reports
```

#### Verbose output:
```bash
python3 sms_application.py -t "+1234567890" -m "Test" -v
```

### Interactive Mode

Run the application in interactive mode for a guided experience:
```bash
python3 sms_application.py -i
```

### Phone Numbers File Format

Create a text file with phone numbers (one per line):
```
+1234567890
+0987654321
+1122334455
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-t, --to` | Phone number(s) to send SMS to (comma-separated) |
| `-m, --message` | SMS message text |
| `-s, --sender` | Custom sender ID (optional) |
| `-f, --file` | File containing phone numbers (one per line) |
| `-i, --interactive` | Run in interactive mode |
| `--balance` | Check account balance |
| `--reports` | Get delivery reports |
| `--bulk-id` | Bulk ID for delivery reports |
| `-v, --verbose` | Show detailed output |

## Configuration

### Environment Variables (Alternative)

You can also use environment variables instead of `config.py`:
```bash
export INFOBIP_API_KEY="your-api-key"
export INFOBIP_SENDER_ID="your-sender-id"
export INFOBIP_BASE_URL="https://yourapi.api.infobip.com"
```

### Security Best Practices

- ✅ Never commit `config.py` to version control
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Use HTTPS only
- ✅ Validate all phone numbers

## API Response Format

### Successful SMS Response:
```json
{
  "messages": [
    {
      "messageId": "4500737166044335450699",
      "status": {
        "description": "Message sent to next instance",
        "groupId": 1,
        "groupName": "PENDING",
        "id": 26,
        "name": "PENDING_ACCEPTED"
      },
      "to": "+254721446106"
    }
  ]
}
```

## Error Handling

The application handles various error scenarios:

- Invalid phone number formats
- Missing API credentials
- Network connectivity issues
- API rate limiting
- Message length validation
- Character encoding issues

## Troubleshooting

### Common Issues:

1. **400 Bad Request Error:**
   - Check API credentials
   - Validate phone number format
   - Ensure message is not empty

2. **403 Forbidden Error:**
   - Verify API key permissions
   - Check account balance
   - Ensure sender ID is approved

3. **Config Import Error:**
   ```
   ❌ Error: config.py not found!
   ```
   Solution: Copy `config_template.py` to `config.py` and add your credentials.

## Dependencies

- `requests` - HTTP library for API calls
- `python3.6+` - Minimum Python version

See `requirements.txt` for complete dependency list.

## Development

### Project Structure:
```
python_SMS/
├── sms_application.py      # Main application
├── config_template.py      # Configuration template
├── config.py              # Your credentials (gitignored)
├── requirements.txt       # Python dependencies
├── phone_numbers.txt      # Sample phone numbers (gitignored)
├── debug_sms.py          # Debug script
├── SMS_FIX_SUMMARY.md    # Fix documentation
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

### Running Tests:
```bash
# Test single SMS
python3 sms_application.py -t "+1234567890" -m "Test message" -v

# Test debug script
python3 debug_sms.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the Infobip API documentation

## Changelog

### v1.1.0 (Latest)
- ✅ Fixed 400 Bad Request error
- ✅ Removed problematic deliveryTimeWindow
- ✅ Added secure credential management
- ✅ Improved error handling
- ✅ Added comprehensive documentation

### v1.0.0
- Initial release with basic SMS functionality

---

---

## 📷 Screenshots

### Dashboard Overview
```
┌─────────────────────────────────────────────────────────────┐
│  📱 SMS Application                           [Navigation Menu] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📱 SMS Dashboard                                           │
│  Welcome to your SMS management system                      │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────│
│  │    📱      │ │     📢     │ │     📊     │ │   💰   │
│  │ Send Single │ │ Send Bulk   │ │  Reports    │ │ Balance│
│  │     SMS     │ │     SMS     │ │             │ │        │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────│
│                                                             │
│  Quick Information                                          │
│  ✅ Single SMS sending    📄 Text files (.txt)           │
│  ✅ Bulk SMS campaigns   📊 CSV files (.csv)            │
│  ✅ File upload support  🌍 International numbers        │
└─────────────────────────────────────────────────────────────┘
```

### Bulk SMS Interface
```
┌─────────────────────────────────────────────────────────────┐
│  Send Bulk SMS                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Choose Input Method:                                       │
│  [ Manual Input ] [ File Upload ]                          │
│                                                             │
│  Phone Numbers:                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ +1234567890                                             │ │
│  │ +1987654321                                             │ │
│  │ +254700000000                                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  0 numbers entered                                          │
│                                                             │
│  Message:                                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Your message here...                                    │ │
│  └─────────────────────────────────────────────────────────┘ │
│  0/1600 characters                                          │
│                                                             │
│  [Clear]  [Send Bulk SMS]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📡 API Reference

### Web API Endpoints

The web application exposes RESTful API endpoints for programmatic access:

#### Send SMS
```http
POST /api/send-sms
Content-Type: application/json

{
  "phone_numbers": ["+1234567890", "+1987654321"],
  "message": "Your message here",
  "sender": "Optional Sender ID"
}
```

**Response:**
```json
{
  "success": true,
  "total_sent": 2,
  "successful": 2,
  "failed": 0,
  "bulk_id": "bulk-id-here",
  "duration": 1.234,
  "messages": [...]
}
```

#### Upload Phone Numbers
```http
POST /api/upload-phones
Content-Type: multipart/form-data

file: phone_numbers.txt
```

**Response:**
```json
{
  "success": true,
  "phone_numbers": ["+1234567890", "+1987654321"],
  "count": 2
}
```

#### Get Delivery Reports
```http
GET /api/reports?bulk_id=optional&limit=50
```

**Response:**
```json
{
  "success": true,
  "reports": {
    "results": [
      {
        "to": "+1234567890",
        "status": {"name": "DELIVERED"},
        "sentAt": "2023-01-01T10:00:00Z",
        "doneAt": "2023-01-01T10:00:05Z",
        "messageId": "msg-id-here"
      }
    ]
  }
}
```

#### Check Balance
```http
GET /api/balance
```

**Response:**
```json
{
  "success": true,
  "balance": {
    "amount": "10.50",
    "currency": "USD"
  }
}
```

---

## 🛠️ Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │  Flask Web App  │    │  Infobip API    │
│                 │◄──►│                 │◄──►│                 │
│ • JavaScript    │    │ • Python Flask │    │ • SMS Gateway   │
│ • Bootstrap CSS │    │ • File Upload   │    │ • Delivery      │
│ • Responsive UI │    │ • Validation    │    │ • Reports       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  File System    │◄─────────────┘
                        │                 │
                        │ • Config Files  │
                        │ • Upload Cache  │
                        │ • Static Assets │
                        └─────────────────┘
```

### File Structure
```
python_SMS/
├── 🌐 Web Application
│   ├── app.py                    # Flask web server
│   ├── templates/                # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Dashboard
│   │   ├── send_single.html     # Single SMS
│   │   ├── send_bulk.html       # Bulk SMS
│   │   ├── reports.html         # Delivery reports
│   │   └── balance.html         # Account balance
│   └── static/                  # Static assets
│       ├── css/style.css        # Custom styles
│       └── js/app.js           # JavaScript utilities
├── 💻 Core Application
│   ├── sms_application.py       # SMS client & CLI
│   ├── config.py               # API configuration
│   ├── config_template.py      # Config template
│   └── requirements.txt        # Dependencies
├── 📄 Documentation
│   ├── README.md               # This file
│   ├── WEB_APP_README.md       # Web app guide
│   ├── SMS_README.md           # CLI documentation
│   └── SMS_FIX_SUMMARY.md      # Technical fixes
├── 📞 Sample Data
│   └── phone_numbers.txt       # Sample numbers
└── 🔧 Development
    ├── debug_sms.py            # Debug utilities
    └── uploads/                # Temporary uploads
```

---

## 🚀 Deployment

### Development Environment
```bash
# Run in development mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Production Deployment

#### 1. Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5001 --workers 4 app:app
```

#### 2. Using Docker
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

```bash
# Build and run
docker build -t sms-app .
docker run -p 5001:5001 sms-app
```

#### 3. Environment Variables
```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY="your-secret-key-here"
export INFOBIP_API_KEY="your-api-key"
export INFOBIP_SENDER_ID="your-sender-id"
export INFOBIP_BASE_URL="https://api.infobip.com"
```

#### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/your/app/static/;
    }
}
```

---

## 📊 Performance & Monitoring

### Performance Optimization
- **File Upload**: Streaming upload with progress tracking
- **Bulk SMS**: Batch processing with rate limiting
- **Caching**: Static asset caching with ETags
- **Compression**: Gzip compression for all responses
- **Database**: Optimized queries with connection pooling

### Monitoring
```python
# Add to app.py for monitoring
import logging
from flask import request

@app.before_request
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)

@app.after_request
def log_response_info(response):
    logger.info('Response: %s', response.status_code)
    return response
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

---

## 🔒 Security Considerations

### Security Checklist
- ✅ **HTTPS Only**: Force SSL in production
- ✅ **Input Validation**: Sanitize all user inputs
- ✅ **File Upload Security**: Restrict file types and sizes
- ✅ **API Rate Limiting**: Prevent abuse
- ✅ **CSRF Protection**: Enable CSRF tokens
- ✅ **Secure Headers**: Set security headers
- ✅ **Audit Logging**: Log all SMS operations

### Implementation
```python
# Security headers
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## 📝 License & Contributing

### License
```
MIT License

Copyright (c) 2023 SMS Web Application

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

### Contributing Guidelines
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/new-feature`
3. **Commit** changes: `git commit -am 'Add new feature'`
4. **Push** to branch: `git push origin feature/new-feature`
5. **Submit** a pull request

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/yourusername/python_SMS.git
cd python_SMS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt  # Development dependencies

# Run tests
python -m pytest tests/

# Start development server
FLASK_ENV=development python app.py
```

---

## 📞 Support & Resources

### Getting Help
- 📚 **Documentation**: Read this README and linked docs
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/python_SMS/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/python_SMS/discussions)
- 📧 **Email**: [support@yourcompany.com](mailto:support@yourcompany.com)

### External Resources
- 📄 [Infobip API Documentation](https://www.infobip.com/docs/api)
- 🌍 [Flask Documentation](https://flask.palletsprojects.com/)
- 🎨 [Bootstrap Documentation](https://getbootstrap.com/docs/)

### Troubleshooting

#### Common Error Solutions

**1. "Config not found" Error**
```bash
❌ Error: config.py not found!

✅ Solution:
cp config_template.py config.py
# Edit config.py with your credentials
```

**2. "Permission denied" on file upload**
```bash
❌ Error: Permission denied

✅ Solution:
mkdir uploads
chmod 755 uploads
```

**3. "Module not found" errors**
```bash
❌ Error: No module named 'flask'

✅ Solution:
pip install -r requirements.txt
```

**4. "API key invalid" errors**
```bash
❌ Error: 401 Unauthorized

✅ Solution:
1. Check API_KEY in config.py
2. Verify API_BASE_URL is correct
3. Ensure account is active
```

---

## 🎆 Changelog

### v2.0.0 (Current) - Web Application Release
- ✨ **NEW**: Complete web interface with Flask
- ✨ **NEW**: Responsive Bootstrap 5 design
- ✨ **NEW**: File upload for bulk SMS
- ✨ **NEW**: Real-time progress tracking
- ✨ **NEW**: Interactive delivery reports
- ✨ **NEW**: Account balance monitoring
- ✨ **NEW**: RESTful API endpoints
- 🔧 **IMPROVED**: Enhanced error handling
- 🔧 **IMPROVED**: Security features
- 🔧 **IMPROVED**: Mobile responsiveness

### v1.1.0 - CLI Improvements
- ✅ **FIXED**: 400 Bad Request error
- ✅ **FIXED**: Removed problematic deliveryTimeWindow
- ✨ **ADDED**: Secure credential management
- ✨ **ADDED**: Interactive mode
- ✨ **ADDED**: Verbose output option
- 🔧 **IMPROVED**: Error messages
- 🔧 **IMPROVED**: Documentation

### v1.0.0 - Initial Release
- ✨ **INITIAL**: Basic SMS sending functionality
- ✨ **INITIAL**: Command-line interface
- ✨ **INITIAL**: Infobip API integration

---

<div align="center">

## 🚀 Ready to Start?

**Choose your preferred interface:**

[🌐 **Launch Web App**](http://localhost:5001) • [📱 **CLI Guide**](#command-line-interface) • [📄 **API Docs**](#api-reference)

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/python_SMS?style=social)](https://github.com/yourusername/python_SMS)

---

📧 **Questions?** • 🐛 **Found a bug?** • 💡 **Have a suggestion?**

[Create an issue](https://github.com/yourusername/python_SMS/issues) and we'll help you out!

---

**⚠️ Security Notice:** Never commit your `config.py` file or expose API credentials in public repositories.

</div>

