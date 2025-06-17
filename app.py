#!/usr/bin/env python3
"""
Flask Web Application for SMS Service

A modern web interface for the Infobip SMS application with features:
- Single SMS sending
- Bulk SMS sending
- File upload for phone numbers
- Delivery reports
- Account balance checking
- Responsive design
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
import time
from datetime import datetime
from typing import List, Dict

# Import our SMS client
from sms_application import SMSClient, format_response

# Configuration
try:
    from config import API_BASE_URL, SENDER_ID, API_KEY
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please copy config_template.py to config.py and fill in your API credentials.")
    exit(1)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SMS client
sms_client = SMSClient(API_KEY, API_BASE_URL, SENDER_ID)

# Allowed file extensions for phone number uploads
ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_phone_numbers_from_file(filepath):
    """Extract phone numbers from uploaded file"""
    phone_numbers = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip comments
                    # Handle CSV format (take first column)
                    if ',' in line:
                        phone = line.split(',')[0].strip()
                    else:
                        phone = line
                    
                    if phone:
                        phone_numbers.append(phone)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return phone_numbers

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/send-single')
def send_single():
    """Single SMS sending page"""
    return render_template('send_single.html')

@app.route('/send-bulk')
def send_bulk():
    """Bulk SMS sending page"""
    return render_template('send_bulk.html')

@app.route('/reports')
def reports():
    """Delivery reports page"""
    return render_template('reports.html')

@app.route('/balance')
def balance():
    """Account balance page"""
    return render_template('balance.html')

@app.route('/api/send-sms', methods=['POST'])
def api_send_sms():
    """API endpoint to send SMS"""
    try:
        data = request.get_json()
        
        phone_numbers = data.get('phone_numbers', [])
        message = data.get('message', '').strip()
        sender = data.get('sender', '').strip() or None
        
        if not phone_numbers:
            return jsonify({'error': 'No phone numbers provided'}), 400
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Convert single phone number to list
        if isinstance(phone_numbers, str):
            phone_numbers = [phone_numbers]
        
        # Clean phone numbers
        phone_numbers = [p.strip() for p in phone_numbers if p.strip()]
        
        start_time = time.time()
        response = sms_client.send_sms(phone_numbers, message, sender=sender)
        end_time = time.time()
        
        # Process response
        messages = response.get('messages', [])
        success_count = sum(1 for msg in messages if msg.get('status', {}).get('groupName') == 'PENDING')
        total_count = len(messages)
        
        result = {
            'success': True,
            'total_sent': total_count,
            'successful': success_count,
            'failed': total_count - success_count,
            'bulk_id': response.get('bulkId'),
            'duration': round(end_time - start_time, 3),
            'messages': messages
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-phones', methods=['POST'])
def api_upload_phones():
    """API endpoint to upload phone numbers file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse phone numbers
            phone_numbers = parse_phone_numbers_from_file(filepath)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if not phone_numbers:
                return jsonify({'error': 'No valid phone numbers found in file'}), 400
            
            return jsonify({
                'success': True,
                'phone_numbers': phone_numbers,
                'count': len(phone_numbers)
            })
        
        return jsonify({'error': 'Invalid file format. Only .txt and .csv files are allowed'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/balance')
def api_balance():
    """API endpoint to check account balance"""
    try:
        balance_info = sms_client.check_account_balance()
        return jsonify({
            'success': True,
            'balance': balance_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/reports')
def api_reports():
    """API endpoint to get delivery reports"""
    try:
        bulk_id = request.args.get('bulk_id')
        limit = int(request.args.get('limit', 50))
        
        kwargs = {'limit': limit}
        if bulk_id:
            kwargs['bulk_id'] = bulk_id
        
        reports = sms_client.get_delivery_reports(**kwargs)
        
        return jsonify({
            'success': True,
            'reports': reports
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    import sys
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0-apple-inspired',
        'python_version': sys.version,
        'app_name': 'SMS Web Application'
    })

@app.route('/metrics')
def metrics():
    """Basic metrics endpoint"""
    import os
    import psutil
    from datetime import datetime
    
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return jsonify({
            'timestamp': datetime.now().isoformat(),
            'memory_usage_mb': round(memory_info.rss / 1024 / 1024, 2),
            'cpu_percent': process.cpu_percent(),
            'uptime_seconds': round(time.time() - process.create_time(), 2),
            'threads': process.num_threads()
        })
    except Exception as e:
        return jsonify({
            'error': 'Metrics unavailable',
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

