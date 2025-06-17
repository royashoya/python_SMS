# SMS Application with Infobip API

A comprehensive Python SMS application that uses the Infobip API to send SMS messages. Features both interactive and command-line interfaces with support for single and bulk SMS sending.

## Features

🚀 **Multiple Interfaces**
- Interactive mode with menu-driven interface
- Command-line interface for automation
- Batch processing support

📱 **SMS Capabilities**
- Send single SMS messages
- Send bulk SMS to multiple recipients
- Custom sender ID support
- Delivery reports tracking
- Account balance checking

🛡️ **Robust Design**
- Input validation and error handling
- Phone number format validation
- Rate limiting protection (max 100 recipients per batch)
- Session management with proper cleanup

⏱️ **Performance Monitoring**
- Request timing for performance analysis
- Detailed response formatting
- Progress tracking for bulk operations

## Installation

### Prerequisites
- Python 3.6 or higher
- Active Infobip account with API credentials

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Make the script executable:**
```bash
chmod +x sms_application.py
```

3. **Verify your credentials in the script:**
   - API Base URL: `qd9ver.api.infobip.com`
   - Sender ID: `Isuzu_EA`
   - API Key: (Already configured)

## Usage

### Interactive Mode

Run the application in interactive mode for a user-friendly experience:

```bash
python sms_application.py -i
```

**Interactive Menu Options:**
1. **Send Single SMS** - Send one message to one recipient
2. **Send Bulk SMS** - Send one message to multiple recipients
3. **Check Account Balance** - View your Infobip account balance
4. **Check Delivery Reports** - Get delivery status for sent messages
5. **Exit** - Close the application

### Command Line Interface

#### Basic SMS Sending

```bash
# Send single SMS
python sms_application.py -t "+254700000000" -m "Hello from Isuzu EA!"

# Send to multiple recipients
python sms_application.py -t "+254700000000,+254711111111" -m "Bulk message"

# Send using phone numbers from file
python sms_application.py -f phone_numbers.txt -m "Your message here"
```

#### Advanced Options

```bash
# Custom sender ID
python sms_application.py -t "+254700000000" -m "Custom sender" -s "MyBrand"

# Verbose output with detailed information
python sms_application.py -t "+254700000000" -m "Test" -v

# Check account balance
python sms_application.py --balance

# Get delivery reports
python sms_application.py --reports

# Get delivery reports for specific bulk ID
python sms_application.py --reports --bulk-id "12345"
```

### Phone Number File Format

Create a text file with one phone number per line:

```
+254700000000
+254711111111
+254722222222
```

## Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|--------|
| `--to` | `-t` | Phone number(s) - comma separated | `-t "+254700000000,+254711111111"` |
| `--message` | `-m` | SMS message text | `-m "Hello World!"` |
| `--sender` | `-s` | Custom sender ID | `-s "MyBrand"` |
| `--file` | `-f` | File with phone numbers | `-f phones.txt` |
| `--interactive` | `-i` | Run in interactive mode | `-i` |
| `--balance` | | Check account balance | `--balance` |
| `--reports` | | Get delivery reports | `--reports` |
| `--bulk-id` | | Bulk ID for specific reports | `--bulk-id "12345"` |
| `--verbose` | `-v` | Show detailed output | `-v` |

## Phone Number Format

**Required Format:** Include country code with `+` prefix

✅ **Correct Examples:**
- `+254700000000` (Kenya)
- `+1234567890` (US)
- `+44771234567` (UK)

❌ **Incorrect Examples:**
- `0700000000` (Missing country code)
- `254700000000` (Missing + prefix)
- `+254-700-000-000` (Hyphens - will be cleaned automatically)

## API Response Examples

### Successful SMS
```
📱 SMS Batch Summary:
==================================================
Total messages: 2

✅ Message 1:
  Phone: +254700000000
  Status: PENDING
  Description: Message sent to next instance

✅ Message 2:
  Phone: +254711111111
  Status: PENDING
  Description: Message sent to next instance

==================================================
✅ Successful: 2
❌ Failed: 0
📦 Bulk ID: 123456789
⏱️ Request completed in 1.234 seconds
```

### Account Balance
```
💰 Account Balance: 45.67 EUR
```

### Delivery Reports
```
📊 Delivery Reports:

Report 1:
  Phone: +254700000000
  Status: DELIVERED
  Sent At: 2024-01-15T10:30:00.000Z
  Done At: 2024-01-15T10:30:15.000Z
```

## Error Handling

The application includes comprehensive error handling:

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `SMS text cannot be empty` | Empty message | Provide message with `-m` or `--message` |
| `Invalid phone number format` | Wrong phone format | Use international format: `+countrycode...` |
| `Cannot send to more than 100 recipients` | Too many recipients | Split into smaller batches |
| `Failed to send SMS: 401` | Invalid API key | Check your API credentials |
| `Failed to send SMS: 403` | Insufficient balance | Top up your Infobip account |

### HTTP Status Codes

- **200 OK**: SMS sent successfully
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Invalid API key
- **403 Forbidden**: Insufficient account balance
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Infobip server error

## Configuration

### API Settings (configured in script)
```python
API_BASE_URL = "https://qd9ver.api.infobip.com"
SENDER_ID = "Isuzu_EA"
API_KEY = "your-api-key-here"
```

### Limits and Timeouts
```python
MAX_SMS_LENGTH = 160        # Characters per SMS
MAX_RECIPIENTS = 100        # Recipients per batch
DEFAULT_TIMEOUT = 30        # Request timeout in seconds
```

## Examples

### 1. Single SMS via CLI
```bash
python sms_application.py -t "+254700000000" -m "Hello from Isuzu EA! Your service is ready."
```

### 2. Bulk SMS from File
```bash
# Create phone_numbers.txt with:
# +254700000000
# +254711111111
# +254722222222

python sms_application.py -f phone_numbers.txt -m "Bulk notification message"
```

### 3. Interactive Session
```bash
python sms_application.py -i
# Follow the menu prompts
```

### 4. Check Account Status
```bash
python sms_application.py --balance
python sms_application.py --reports
```

## Security Considerations

🔒 **API Key Security:**
- Never commit API keys to version control
- Use environment variables in production:
```python
import os
API_KEY = os.getenv('INFOBIP_API_KEY', 'fallback-key')
```

🔒 **Phone Number Privacy:**
- Validate phone numbers before processing
- Log only masked phone numbers: `+254***000000`
- Implement opt-out mechanisms for recipients

## Troubleshooting

### Connection Issues
```bash
# Test API connectivity
curl -H "Authorization: App your-api-key" \
     https://qd9ver.api.infobip.com/account/1/balance
```

### Debug Mode
Run with verbose flag to see detailed API responses:
```bash
python sms_application.py -t "+254700000000" -m "Test" -v
```

### Common Issues

1. **"requests" module not found**
   ```bash
   pip install requests
   ```

2. **Permission denied**
   ```bash
   chmod +x sms_application.py
   ```

3. **Invalid phone number**
   - Ensure international format: `+countrycode...`
   - Remove spaces, hyphens, parentheses

## Development

### Project Structure
```
.
├── sms_application.py    # Main application
├── requirements.txt      # Python dependencies
├── SMS_README.md        # This documentation
└── phone_numbers.txt    # Example phone numbers file
```

### Adding New Features

The `SMSClient` class can be extended with additional Infobip API endpoints:

```python
def get_sent_messages(self, date_from: str, date_to: str):
    """Get sent messages in date range"""
    url = f"{self.base_url}/sms/1/logs"
    params = {"from": date_from, "to": date_to}
    # Implementation here
```

## Support

For Infobip API documentation and support:
- [Infobip API Documentation](https://www.infobip.com/docs/api)
- [SMS API Reference](https://www.infobip.com/docs/api#channels/sms)

## License

This project is open source and available under the MIT License.

