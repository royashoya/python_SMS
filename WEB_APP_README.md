# SMS Web Application

A modern web interface for the Infobip SMS application with a user-friendly dashboard and comprehensive features.

## Features

- **Dashboard**: Overview and quick access to all features
- **Single SMS**: Send SMS to one recipient
- **Bulk SMS**: Send SMS to multiple recipients with file upload support
- **Delivery Reports**: View and track message delivery status
- **Account Balance**: Check your Infobip account balance
- **File Upload**: Support for .txt and .csv phone number files
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live status updates and progress tracking

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

1. Copy the configuration template:
   ```bash
   cp config_template.py config.py
   ```

2. Edit `config.py` and add your Infobip credentials:
   ```python
   API_BASE_URL = "https://your-infobip-base-url.api.infobip.com"
   SENDER_ID = "YOUR_SENDER_ID"
   API_KEY = "YOUR_API_KEY_HERE"
   ```

### 3. Run the Web Application

```bash
python app.py
```

The web application will be available at: `http://localhost:5001`

## Usage

### Dashboard
- Navigate to `http://localhost:5001` to access the main dashboard
- Use the navigation menu to access different features

### Single SMS
1. Click "Send Single SMS" from the dashboard or navigation
2. Enter the phone number (with country code)
3. Type your message
4. Optionally set a custom sender ID
5. Click "Send SMS"

### Bulk SMS
1. Click "Send Bulk SMS" from the dashboard or navigation
2. Choose input method:
   - **Manual Input**: Enter phone numbers directly (one per line)
   - **File Upload**: Upload a .txt or .csv file with phone numbers
3. Type your message
4. Click "Send Bulk SMS"

### File Format for Bulk SMS

**Text File (.txt):**
```
+1234567890
+1987654321
+254700000000
```

**CSV File (.csv):**
```
+1234567890,John Doe
+1987654321,Jane Smith
+254700000000,Bob Johnson
```

### Delivery Reports
1. Click "Reports" from the navigation
2. Optionally filter by Bulk ID
3. Set the number of reports to display
4. Click "Apply Filter" or "Refresh"

### Account Balance
1. Click "Balance" from the navigation
2. Click "Refresh" to check current balance

## API Endpoints

The web application provides the following API endpoints:

- `POST /api/send-sms` - Send SMS messages
- `POST /api/upload-phones` - Upload phone numbers file
- `GET /api/reports` - Get delivery reports
- `GET /api/balance` - Check account balance

## File Structure

```
├── app.py                 # Main Flask application
├── sms_application.py     # SMS client and core functionality
├── config.py             # API configuration (create from template)
├── config_template.py    # Configuration template
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── send_single.html # Single SMS page
│   ├── send_bulk.html   # Bulk SMS page
│   ├── reports.html     # Delivery reports
│   └── balance.html     # Account balance
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── app.js       # JavaScript utilities
├── uploads/             # Temporary file uploads (auto-created)
└── phone_numbers.txt    # Sample phone numbers file
```

## Security Notes

- The `config.py` file is ignored by Git to protect your API credentials
- File uploads are temporarily stored and immediately deleted after processing
- Maximum file upload size is limited to 16MB
- Input validation is performed on all user inputs

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### Common Issues

1. **"config.py not found" error**
   - Make sure you've copied `config_template.py` to `config.py`
   - Fill in your actual API credentials

2. **Balance checking fails**
   - This feature requires additional API permissions
   - Contact Infobip support to enable account access features
   - SMS sending functionality works independently

3. **File upload issues**
   - Ensure file format is .txt or .csv
   - Check that phone numbers include country codes
   - Maximum file size is 16MB

4. **SMS delivery issues**
   - Verify phone numbers include country codes (e.g., +1234567890)
   - Check your Infobip account balance
   - Ensure your sender ID is approved

### Development Mode

To run in development mode with debug enabled:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```

### Production Deployment

For production deployment:

1. Set `app.secret_key` to a secure random value
2. Use a production WSGI server (e.g., Gunicorn, uWSGI)
3. Configure proper logging
4. Set up HTTPS
5. Use environment variables for sensitive configuration

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the main SMS_README.md for API-related issues
3. Contact Infobip support for account and API issues

## License

This project is for educational and demonstration purposes.

