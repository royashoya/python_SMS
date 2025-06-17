# 🚀 Deployment Guide

This guide covers multiple deployment options for the SMS Web Application.

## 📋 Prerequisites

- Infobip API credentials
- Domain name (for production)
- SSL certificate (for HTTPS)
- Basic understanding of your chosen platform

## 🐳 Docker Deployment (Recommended)

### Local Development

```bash
# Clone the repository
git clone https://github.com/royashoya/sms-web-application.git
cd sms-web-application

# Create environment file
cp .env.example .env
# Edit .env with your credentials

# Build and run with Docker Compose
docker-compose up --build
```

### Production with Docker

```bash
# Build production image
docker build -t sms-web-app:latest .

# Run with environment variables
docker run -d \
  --name sms-web-app \
  -p 80:5000 \
  -e INFOBIP_API_KEY="your-api-key" \
  -e INFOBIP_SENDER_ID="your-sender-id" \
  -e INFOBIP_BASE_URL="https://your-api.api.infobip.com" \
  -e FLASK_ENV=production \
  sms-web-app:latest
```

## 🌊 DigitalOcean App Platform

1. **Create App**:
   ```bash
   # Using doctl CLI
   doctl apps create --spec .do/app.yaml
   ```

2. **App Spec** (`.do/app.yaml`):
   ```yaml
   name: sms-web-application
   services:
   - name: web
     source_dir: /
     github:
       repo: royashoya/sms-web-application
       branch: main
     run_command: gunicorn --bind 0.0.0.0:5000 app:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: INFOBIP_API_KEY
       scope: RUN_TIME
       type: SECRET
     - key: INFOBIP_SENDER_ID
       scope: RUN_TIME
       type: SECRET
     - key: INFOBIP_BASE_URL
       scope: RUN_TIME
       type: SECRET
   ```

## 🚀 Heroku Deployment

1. **Prepare Heroku Files**:
   
   Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
   
   Create `runtime.txt`:
   ```
   python-3.11.0
   ```

2. **Deploy**:
   ```bash
   # Install Heroku CLI and login
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set INFOBIP_API_KEY="your-api-key"
   heroku config:set INFOBIP_SENDER_ID="your-sender-id"
   heroku config:set INFOBIP_BASE_URL="https://your-api.api.infobip.com"
   
   # Deploy
   git push heroku main
   ```

## ☁️ AWS Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**:
   ```bash
   # Initialize EB application
   eb init sms-web-app --region us-east-1 --platform python-3.11
   
   # Create environment
   eb create production
   
   # Set environment variables
   eb setenv INFOBIP_API_KEY="your-api-key" \
           INFOBIP_SENDER_ID="your-sender-id" \
           INFOBIP_BASE_URL="https://your-api.api.infobip.com"
   
   # Deploy
   eb deploy
   ```

3. **EB Configuration** (`.ebextensions/01_flask.config`):
   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app:app
     aws:elasticbeanstalk:application:environment:
       FLASK_ENV: production
   ```

## 🔵 Google Cloud Platform

1. **App Engine** (`app.yaml`):
   ```yaml
   runtime: python311
   
   env_variables:
     FLASK_ENV: production
     INFOBIP_API_KEY: "your-api-key"
     INFOBIP_SENDER_ID: "your-sender-id"
     INFOBIP_BASE_URL: "https://your-api.api.infobip.com"
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
   ```

2. **Deploy**:
   ```bash
   gcloud app deploy
   ```

## 🌐 Traditional VPS/Server

### Ubuntu/Debian Setup

1. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx certbot
   ```

2. **Setup Application**:
   ```bash
   # Create user
   sudo useradd -m -s /bin/bash smsapp
   sudo su - smsapp
   
   # Clone and setup
   git clone https://github.com/royashoya/sms-web-application.git
   cd sms-web-application
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   
   # Configure
   cp config_template.py config.py
   # Edit config.py with your credentials
   ```

3. **Systemd Service** (`/etc/systemd/system/sms-web-app.service`):
   ```ini
   [Unit]
   Description=SMS Web Application
   After=network.target
   
   [Service]
   User=smsapp
   Group=smsapp
   WorkingDirectory=/home/smsapp/sms-web-application
   Environment="PATH=/home/smsapp/sms-web-application/venv/bin"
   ExecStart=/home/smsapp/sms-web-application/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Nginx Configuration** (`/etc/nginx/sites-available/sms-web-app`):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
   
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   
       location /static/ {
           alias /home/smsapp/sms-web-application/static/;
       }
   }
   ```

5. **Enable and Start**:
   ```bash
   sudo systemctl enable sms-web-app
   sudo systemctl start sms-web-app
   sudo ln -s /etc/nginx/sites-available/sms-web-app /etc/nginx/sites-enabled/
   sudo systemctl reload nginx
   
   # Setup SSL with Let's Encrypt
   sudo certbot --nginx -d yourdomain.com
   ```

## 📊 Monitoring Setup

### Application Monitoring

1. **Health Check Endpoint**:
   Add to `app.py`:
   ```python
   @app.route('/health')
   def health_check():
       return {
           'status': 'healthy',
           'timestamp': datetime.now().isoformat(),
           'version': '2.0.0'
       }
   ```

2. **Logging Configuration**:
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   if not app.debug:
       file_handler = RotatingFileHandler('logs/sms-app.log', maxBytes=10240, backupCount=10)
       file_handler.setFormatter(logging.Formatter(
           '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
       ))
       file_handler.setLevel(logging.INFO)
       app.logger.addHandler(file_handler)
   ```

3. **Prometheus Metrics** (optional):
   ```bash
   pip install prometheus-flask-exporter
   ```
   
   Add to `app.py`:
   ```python
   from prometheus_flask_exporter import PrometheusMetrics
   
   metrics = PrometheusMetrics(app)
   metrics.info('app_info', 'Application info', version='2.0.0')
   ```

## 🔒 Security Checklist

### Pre-deployment Security

- [ ] **Environment Variables**: Use environment variables for all secrets
- [ ] **HTTPS**: Enable SSL/TLS in production
- [ ] **Firewall**: Configure firewall rules
- [ ] **Updates**: Keep dependencies updated
- [ ] **Backups**: Set up automated backups
- [ ] **Monitoring**: Enable application monitoring
- [ ] **Rate Limiting**: Implement rate limiting
- [ ] **Input Validation**: Verify all input validation is working

### Production Security Headers

Add to `app.py`:
```python
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## 🔧 Environment Variables

### Required Variables
```bash
INFOBIP_API_KEY=your-api-key-here
INFOBIP_SENDER_ID=your-sender-id
INFOBIP_BASE_URL=https://xxxxx.api.infobip.com
```

### Optional Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
```

## 📈 Performance Optimization

### Production Settings

1. **Gunicorn Configuration** (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:5000"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   timeout = 30
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   ```

2. **Nginx Optimization**:
   ```nginx
   gzip on;
   gzip_types text/css application/javascript application/json;
   
   client_max_body_size 16M;
   
   location /static/ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Permission Denied**:
   ```bash
   sudo chown -R appuser:appuser /app
   sudo chmod -R 755 /app
   ```

3. **Module Not Found**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Config Import Error**:
   ```bash
   cp config_template.py config.py
   # Edit config.py with your credentials
   ```

### Log Locations

- **Application Logs**: `/var/log/sms-web-app/`
- **Nginx Logs**: `/var/log/nginx/`
- **Systemd Logs**: `journalctl -u sms-web-app`

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue on GitHub
4. Contact support team

---

**Note**: Always test deployments in a staging environment before deploying to production.

