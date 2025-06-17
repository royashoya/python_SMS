#!/usr/bin/env python3
"""
Basic tests for SMS Web Application

These tests ensure the core functionality works correctly.
Run with: pytest test_app.py
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Set up test configuration before importing app
os.environ['TESTING'] = 'True'

# Mock the config import to avoid import errors during testing
with patch.dict('sys.modules', {
    'config': MagicMock(
        API_BASE_URL='https://test.api.infobip.com',
        SENDER_ID='TestSender',
        API_KEY='test_api_key'
    )
}):
    import app
    from sms_application import SMSClient


class TestFlaskApp:
    """Test Flask web application"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        with app.app.test_client() as client:
            yield client
    
    def test_index_page(self, client):
        """Test dashboard loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'SMS Dashboard' in response.data
        assert b'Send Single SMS' in response.data
        assert b'Send Bulk SMS' in response.data
    
    def test_send_single_page(self, client):
        """Test single SMS page loads"""
        response = client.get('/send-single')
        assert response.status_code == 200
        assert b'Send Single SMS' in response.data
        assert b'Phone Number' in response.data
    
    def test_send_bulk_page(self, client):
        """Test bulk SMS page loads"""
        response = client.get('/send-bulk')
        assert response.status_code == 200
        assert b'Send Bulk SMS' in response.data
        assert b'Choose Input Method' in response.data
    
    def test_reports_page(self, client):
        """Test reports page loads"""
        response = client.get('/reports')
        assert response.status_code == 200
        assert b'Delivery Reports' in response.data
    
    def test_balance_page(self, client):
        """Test balance page loads"""
        response = client.get('/balance')
        assert response.status_code == 200
        assert b'Account Balance' in response.data
    
    def test_api_send_sms_validation(self, client):
        """Test SMS API validation"""
        # Test missing data
        response = client.post('/api/send-sms', 
                             json={},
                             content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        
        # Test missing message
        response = client.post('/api/send-sms',
                             json={'phone_numbers': ['+1234567890']},
                             content_type='application/json')
        assert response.status_code == 400
        
        # Test missing phone numbers
        response = client.post('/api/send-sms',
                             json={'message': 'Test message'},
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_file_upload_validation(self, client):
        """Test file upload validation"""
        # Test no file
        response = client.post('/api/upload-phones')
        assert response.status_code == 400
        
        # Test invalid file type
        data = {
            'file': (StringIO('test content'), 'test.exe')
        }
        response = client.post('/api/upload-phones', data=data)
        assert response.status_code == 400
    
    def test_valid_file_upload(self, client):
        """Test valid file upload"""
        # Create temporary file with phone numbers
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('+1234567890\n+1987654321\n')
            temp_file = f.name
        
        try:
            with open(temp_file, 'rb') as f:
                data = {
                    'file': (f, 'phones.txt')
                }
                response = client.post('/api/upload-phones', data=data)
                
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert len(data['phone_numbers']) == 2
        finally:
            os.unlink(temp_file)


class TestSMSClient:
    """Test SMS client functionality"""
    
    def test_sms_client_init(self):
        """Test SMS client initialization"""
        client = SMSClient('test_key', 'https://test.api.infobip.com', 'TestSender')
        assert client.api_key == 'test_key'
        assert client.base_url == 'https://test.api.infobip.com'
        assert client.sender_id == 'TestSender'
    
    def test_phone_number_validation(self):
        """Test phone number validation"""
        client = SMSClient('test_key', 'https://test.api.infobip.com', 'TestSender')
        
        # Valid phone numbers
        assert client._validate_phone_number('+1234567890') is True
        assert client._validate_phone_number('1234567890') is True
        assert client._validate_phone_number('+254700000000') is True
        
        # Invalid phone numbers
        assert client._validate_phone_number('123') is False
        assert client._validate_phone_number('abc123') is False
        assert client._validate_phone_number('') is False
    
    @patch('requests.Session.post')
    def test_send_sms_success(self, mock_post):
        """Test successful SMS sending"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'messages': [{
                'messageId': 'test-id-123',
                'status': {'groupName': 'PENDING'},
                'to': '+1234567890'
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = SMSClient('test_key', 'https://test.api.infobip.com', 'TestSender')
        result = client.send_sms('+1234567890', 'Test message')
        
        assert 'messages' in result
        assert len(result['messages']) == 1
        assert result['messages'][0]['to'] == '+1234567890'
    
    def test_send_sms_validation_error(self):
        """Test SMS validation errors"""
        client = SMSClient('test_key', 'https://test.api.infobip.com', 'TestSender')
        
        # Test empty message
        with pytest.raises(ValueError, match="SMS text cannot be empty"):
            client.send_sms('+1234567890', '')
        
        # Test invalid phone number
        with pytest.raises(ValueError, match="Invalid phone number format"):
            client.send_sms('invalid', 'Test message')
        
        # Test too many recipients
        phone_numbers = [f'+123456789{i:02d}' for i in range(101)]
        with pytest.raises(ValueError, match="Cannot send to more than"):
            client.send_sms(phone_numbers, 'Test message')


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_allowed_file(self):
        """Test file extension validation"""
        assert app.allowed_file('test.txt') is True
        assert app.allowed_file('test.csv') is True
        assert app.allowed_file('test.TXT') is True
        assert app.allowed_file('test.CSV') is True
        
        assert app.allowed_file('test.exe') is False
        assert app.allowed_file('test.jpg') is False
        assert app.allowed_file('test') is False
    
    def test_parse_phone_numbers_from_file(self):
        """Test phone number parsing from file"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('+1234567890\n')
            f.write('+1987654321\n')
            f.write('# This is a comment\n')
            f.write('+254700000000\n')
            f.write('\n')  # Empty line
            temp_file = f.name
        
        try:
            phone_numbers = app.parse_phone_numbers_from_file(temp_file)
            assert len(phone_numbers) == 3
            assert '+1234567890' in phone_numbers
            assert '+1987654321' in phone_numbers
            assert '+254700000000' in phone_numbers
        finally:
            os.unlink(temp_file)
    
    def test_parse_csv_phone_numbers(self):
        """Test CSV phone number parsing"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('+1234567890,John Doe\n')
            f.write('+1987654321,Jane Smith\n')
            temp_file = f.name
        
        try:
            phone_numbers = app.parse_phone_numbers_from_file(temp_file)
            assert len(phone_numbers) == 2
            assert '+1234567890' in phone_numbers
            assert '+1987654321' in phone_numbers
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

