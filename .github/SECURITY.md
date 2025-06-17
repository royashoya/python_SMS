# Security Policy

## Supported Versions

We actively support the following versions of the SMS Web Application:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | ✅ Yes             |
| 1.1.x   | ✅ Yes             |
| < 1.1   | ❌ No              |

## Security Features

The SMS Web Application includes several security features:

- **Input Validation**: All user inputs are validated and sanitized
- **File Upload Security**: File type and size restrictions
- **XSS Protection**: HTML sanitization and CSP headers
- **Credential Protection**: API keys never exposed to frontend
- **Secure File Handling**: Temporary files automatically cleaned up
- **HTTPS Enforcement**: SSL/TLS encryption in production

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities via:

### Email
Send an email to: **[your-email@domain.com]**

Include the following information:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Time
- **Initial Response**: Within 48 hours
- **Status Update**: Within 1 week
- **Resolution**: Within 30 days (depending on severity)

## Security Best Practices

When using this application:

### For Users
- ✅ **Never commit `config.py`** to version control
- ✅ **Use strong API credentials** and rotate regularly
- ✅ **Enable HTTPS** in production
- ✅ **Validate phone numbers** before sending
- ✅ **Monitor usage** and set up alerts
- ✅ **Use environment variables** for sensitive data

### For Developers
- ✅ **Sanitize all inputs** before processing
- ✅ **Validate file uploads** strictly
- ✅ **Use parameterized queries** if adding database support
- ✅ **Implement rate limiting** for API endpoints
- ✅ **Add CSRF protection** for forms
- ✅ **Set security headers** appropriately

## Known Security Considerations

### File Uploads
- File size limited to 16MB
- Only .txt and .csv files accepted
- Files processed in memory and immediately deleted
- No executable files allowed

### API Security
- API credentials stored server-side only
- Request validation on all endpoints
- Error messages don't expose sensitive information

### Web Application
- Bootstrap 5 for secure UI components
- No inline JavaScript execution
- Content Security Policy headers
- XSS protection enabled

## Security Updates

Security updates will be:
- **Released immediately** for critical vulnerabilities
- **Documented** in the CHANGELOG
- **Announced** via GitHub releases
- **Tagged** with security labels

## Third-Party Dependencies

We regularly monitor our dependencies for security vulnerabilities:

- **Python packages**: Updated via `pip-audit`
- **JavaScript libraries**: CDN-hosted with SRI hashes
- **Flask framework**: Latest stable version
- **Bootstrap**: Latest stable version

## Security Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Initial assessment and acknowledgment
3. **Day 3-7**: Investigation and reproduction
4. **Day 8-21**: Development of fix
5. **Day 22-28**: Testing and validation
6. **Day 29-30**: Release and disclosure

## Contact Information

For security-related questions:
- **Security Email**: [your-security-email@domain.com]
- **GPG Key**: [Your GPG Key ID if applicable]
- **Response Time**: Within 48 hours

## Acknowledgments

We thank the following security researchers for their responsible disclosure:

<!-- Will be updated as reports are received -->

---

**Note**: This security policy applies to the SMS Web Application repository. For Infobip API security, please refer to [Infobip's security documentation](https://www.infobip.com/security).

