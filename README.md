# SMS Application using Infobip API

A Python application for sending SMS messages using the Infobip SMS API. Supports both single and bulk SMS sending with interactive and command-line interfaces.

## Features

- 📱 Send single or bulk SMS messages
- 🔒 Secure credential management
- 📊 Delivery report tracking
- 💰 Account balance checking
- ⚡ Interactive and CLI modes
- 🛡️ Input validation and error handling
- 📝 Detailed logging and reporting

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/python_SMS.git
   cd python_SMS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials:**
   ```bash
   cp config_template.py config.py
   ```
   Edit `config.py` and add your Infobip API credentials:
   ```python
   API_BASE_URL = "https://yourapi.api.infobip.com"
   SENDER_ID = "YourSenderID"
   API_KEY = "your-api-key-here"
   ```

## Usage

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

**⚠️ Security Notice:** Never commit your `config.py` file or expose API credentials in public repositories.

