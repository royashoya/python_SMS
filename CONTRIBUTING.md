# Contributing to SMS Web Application

Thank you for your interest in contributing to the SMS Web Application! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Modern web browser
- Infobip account (for testing)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/royashoya/sms-web-application.git
   cd sms-web-application
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration:**
   ```bash
   cp config_template.py config.py
   # Edit config.py with your test credentials
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

## 🔄 Development Workflow

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, focused commits
4. **Test your changes** thoroughly
5. **Submit a pull request** with a clear description

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Frontend Code Style
- Use consistent indentation (2 spaces for HTML/CSS/JS)
- Follow Bootstrap conventions
- Use semantic HTML elements
- Add comments for complex JavaScript logic

### Git Commit Messages
Use conventional commit format:
```
type(scope): description

- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting changes
- refactor: code refactoring
- test: adding tests
- chore: maintenance tasks
```

Examples:
```
feat(ui): add dark mode toggle
fix(api): handle timeout errors gracefully
docs(readme): update installation instructions
```

## 🧪 Testing

### Manual Testing
1. Test all web interface features
2. Verify responsive design on different screen sizes
3. Test file upload functionality
4. Verify error handling

### Test Coverage Areas
- [ ] Single SMS sending
- [ ] Bulk SMS with manual input
- [ ] Bulk SMS with file upload
- [ ] File format validation
- [ ] Phone number validation
- [ ] Error handling
- [ ] Mobile responsiveness
- [ ] API endpoints

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment details** (OS, Python version, browser)
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Error messages** (full stack trace)

### Bug Report Template
```markdown
**Environment:**
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.7]
- Browser: [e.g., Chrome 95.0]

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior:**
A clear description of what you expected to happen.

**Actual Behavior:**
A clear description of what actually happened.

**Screenshots:**
If applicable, add screenshots to help explain your problem.

**Additional Context:**
Add any other context about the problem here.
```

## ✨ Feature Requests

When requesting features, please include:

- **Use case description**
- **Proposed solution**
- **Alternative solutions considered**
- **Additional context**

## 🔒 Security

For security vulnerabilities:
1. **Do NOT** create a public issue
2. **Do NOT** commit sensitive information
3. Contact the maintainer privately
4. Follow responsible disclosure practices

### Security Checklist
- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] File upload restrictions in place
- [ ] XSS protection enabled
- [ ] HTTPS enforced in production

## 📚 Documentation

When updating documentation:
- Use clear, concise language
- Include code examples
- Update relevant sections
- Check for broken links
- Verify accuracy

## 🎯 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Manual testing completed

### PR Description Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature)
- [ ] Documentation update

## Testing
- [ ] Manual testing completed
- [ ] All features work as expected
- [ ] No regression issues found

## Screenshots (if applicable)
[Add screenshots of UI changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏗️ Project Structure

```
sms-web-application/
├── app.py                 # Main Flask application
├── sms_application.py     # SMS client and CLI
├── config_template.py     # Configuration template
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   └── *.html          # Feature pages
├── static/              # Static assets
│   ├── css/style.css   # Custom styles
│   └── js/app.js      # JavaScript utilities
├── uploads/            # Temporary file uploads
└── docs/              # Documentation
```

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/royashoya/sms-web-application/issues)
- **Discussions**: [GitHub Discussions](https://github.com/royashoya/sms-web-application/discussions)
- **Documentation**: README.md and WEB_APP_README.md

## 🏆 Recognition

Contributors will be:
- Listed in the project contributors
- Mentioned in release notes
- Given credit for their contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the SMS Web Application!** 🎉

