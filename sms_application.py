#!/usr/bin/env python3
"""
SMS Application using Infobip API

This application allows you to send SMS messages using the Infobip SMS API.
Supports single and bulk SMS sending with interactive and CLI modes.
"""

import requests
import json
import argparse
import sys
import time
from typing import List, Dict, Optional, Union
from datetime import datetime

# Configuration - Import from config.py
try:
    from config import API_BASE_URL, SENDER_ID, API_KEY
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please copy config_template.py to config.py and fill in your API credentials.")
    sys.exit(1)

# Constants
MAX_SMS_LENGTH = 160
MAX_RECIPIENTS = 100
DEFAULT_TIMEOUT = 30

class SMSClient:
    """Infobip SMS Client for sending SMS messages"""
    
    def __init__(self, api_key: str, base_url: str, sender_id: str):
        """
        Initialize SMS Client
        
        Args:
            api_key: Infobip API key
            base_url: API base URL
            sender_id: Sender ID for SMS messages
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.sender_id = sender_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'App {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def send_sms(self, to: Union[str, List[str]], text: str, 
                 sender: Optional[str] = None, 
                 delivery_report: bool = True) -> Dict:
        """
        Send SMS message(s)
        
        Args:
            to: Phone number(s) to send SMS to (with country code)
            text: SMS message text
            sender: Custom sender ID (optional)
            delivery_report: Whether to request delivery report
            
        Returns:
            Dict containing API response
            
        Raises:
            ValueError: If parameters are invalid
            requests.RequestException: If API request fails
        """
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("SMS text cannot be empty")
        
        if len(text) > MAX_SMS_LENGTH:
            print(f"Warning: SMS text is {len(text)} characters. May be split into multiple parts.")
        
        # Normalize phone numbers
        if isinstance(to, str):
            to = [to]
        
        if len(to) > MAX_RECIPIENTS:
            raise ValueError(f"Cannot send to more than {MAX_RECIPIENTS} recipients at once")
        
        # Validate phone numbers
        for phone in to:
            if not self._validate_phone_number(phone):
                raise ValueError(f"Invalid phone number format: {phone}")
        
        # Prepare destinations
        destinations = [{"to": phone} for phone in to]
        
        # Prepare payload
        payload = {
            "messages": [{
                "from": sender or self.sender_id,
                "destinations": destinations,
                "text": text.strip(),
                "notifyUrl": "",  # Add your callback URL if needed
                "notifyContentType": "application/json",
                "callbackData": "",
                "validityPeriod": 720  # 12 hours in minutes
            }]
        }
        
        # Note: deliveryTimeWindow removed to avoid API validation errors
        # Can be added back if needed for specific use cases
        
        # Send request
        url = f"{self.base_url}/sms/2/text/advanced"
        
        try:
            response = self.session.post(
                url, 
                json=payload, 
                timeout=DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to send SMS: {str(e)}")
    
    def get_delivery_reports(self, bulk_id: Optional[str] = None, 
                           message_id: Optional[str] = None, 
                           limit: int = 50) -> Dict:
        """
        Get delivery reports for sent messages
        
        Args:
            bulk_id: Bulk ID from send response
            message_id: Specific message ID
            limit: Maximum number of reports to retrieve
            
        Returns:
            Dict containing delivery reports
        """
        url = f"{self.base_url}/sms/1/reports"
        params = {"limit": limit}
        
        if bulk_id:
            params["bulkId"] = bulk_id
        if message_id:
            params["messageId"] = message_id
        
        try:
            response = self.session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to get delivery reports: {str(e)}")
    
    def check_account_balance(self) -> Dict:
        """
        Check account balance
        
        Returns:
            Dict containing account balance information
        
        Note: This feature requires specific API permissions that may not be 
        available with all API keys. SMS sending functionality works independently.
        """
        url = f"{self.base_url}/account/1/balance"
        
        try:
            response = self.session.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise requests.RequestException(
                    "Balance checking requires additional API permissions. "
                    "Contact Infobip support to enable account access features. "
                    "SMS sending functionality is not affected."
                )
            else:
                raise requests.RequestException(f"Failed to check balance: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to check balance: {str(e)}")
    
    def _validate_phone_number(self, phone: str) -> bool:
        """
        Basic phone number validation
        
        Args:
            phone: Phone number to validate
            
        Returns:
            bool: True if valid format
        """
        # Remove common separators
        cleaned = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Check if it's all digits and reasonable length
        return cleaned.isdigit() and 7 <= len(cleaned) <= 15
    
    def close(self):
        """Close the session"""
        self.session.close()

def format_response(response: Dict, show_details: bool = False) -> str:
    """
    Format API response for display
    
    Args:
        response: API response dictionary
        show_details: Whether to show detailed information
        
    Returns:
        Formatted string
    """
    if 'messages' in response:
        messages = response['messages']
        total = len(messages)
        
        result = f"\n📱 SMS Batch Summary:\n"
        result += f"{'='*50}\n"
        result += f"Total messages: {total}\n"
        
        success_count = 0
        error_count = 0
        
        for i, msg in enumerate(messages, 1):
            status = msg.get('status', {})
            group_name = status.get('groupName', 'Unknown')
            description = status.get('description', 'No description')
            
            if group_name == 'PENDING':
                success_count += 1
                status_emoji = "✅"
            else:
                error_count += 1
                status_emoji = "❌"
            
            result += f"\n{status_emoji} Message {i}:\n"
            result += f"  Phone: {msg.get('to', 'Unknown')}\n"
            result += f"  Status: {group_name}\n"
            result += f"  Description: {description}\n"
            
            if show_details:
                result += f"  Message ID: {msg.get('messageId', 'N/A')}\n"
                result += f"  SMS Count: {msg.get('smsCount', 'N/A')}\n"
        
        result += f"\n{'='*50}\n"
        result += f"✅ Successful: {success_count}\n"
        result += f"❌ Failed: {error_count}\n"
        
        if 'bulkId' in response:
            result += f"📦 Bulk ID: {response['bulkId']}\n"
    
    else:
        result = f"Response: {json.dumps(response, indent=2)}"
    
    return result

def interactive_mode():
    """Interactive mode for SMS sending"""
    print("\n🚀 === Infobip SMS Application ===")
    print("Choose an option:")
    print("1. Send Single SMS")
    print("2. Send Bulk SMS")
    print("3. Check Account Balance")
    print("4. Check Delivery Reports")
    print("5. Exit")
    
    client = SMSClient(API_KEY, API_BASE_URL, SENDER_ID)
    
    try:
        while True:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '5':
                print("👋 Goodbye!")
                break
            
            elif choice == '1':
                # Single SMS
                phone = input("Enter phone number (with country code, e.g., +254700000000): ").strip()
                message = input("Enter SMS message: ").strip()
                
                if not phone or not message:
                    print("❌ Phone number and message are required!")
                    continue
                
                try:
                    start_time = time.time()
                    response = client.send_sms(phone, message)
                    end_time = time.time()
                    
                    print(format_response(response))
                    print(f"⏱️ Request completed in {end_time - start_time:.3f} seconds")
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
            
            elif choice == '2':
                # Bulk SMS
                print("Enter phone numbers (one per line, press Enter twice to finish):")
                phones = []
                while True:
                    phone = input().strip()
                    if not phone:
                        break
                    phones.append(phone)
                
                if not phones:
                    print("❌ No phone numbers entered!")
                    continue
                
                message = input("Enter SMS message: ").strip()
                if not message:
                    print("❌ Message is required!")
                    continue
                
                try:
                    start_time = time.time()
                    response = client.send_sms(phones, message)
                    end_time = time.time()
                    
                    print(format_response(response, show_details=True))
                    print(f"⏱️ Request completed in {end_time - start_time:.3f} seconds")
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
            
            elif choice == '3':
                # Check balance
                try:
                    balance = client.check_account_balance()
                    print(f"\n💰 Account Balance:")
                    print(f"Currency: {balance.get('currency', 'N/A')}")
                    print(f"Amount: {balance.get('amount', 'N/A')}")
                    
                except Exception as e:
                    print(f"❌ Error checking balance: {str(e)}")
            
            elif choice == '4':
                # Check delivery reports
                bulk_id = input("Enter Bulk ID (optional, press Enter to skip): ").strip()
                limit = input("Enter limit (default 10): ").strip() or "10"
                
                try:
                    limit = int(limit)
                    kwargs = {"limit": limit}
                    if bulk_id:
                        kwargs["bulk_id"] = bulk_id
                    
                    reports = client.get_delivery_reports(**kwargs)
                    
                    if 'results' in reports and reports['results']:
                        print(f"\n📊 Delivery Reports:")
                        for i, report in enumerate(reports['results'], 1):
                            print(f"\nReport {i}:")
                            print(f"  Phone: {report.get('to', 'N/A')}")
                            print(f"  Status: {report.get('status', {}).get('name', 'N/A')}")
                            print(f"  Sent At: {report.get('sentAt', 'N/A')}")
                            print(f"  Done At: {report.get('doneAt', 'N/A')}")
                    else:
                        print("📭 No delivery reports found.")
                        
                except ValueError:
                    print("❌ Invalid limit value!")
                except Exception as e:
                    print(f"❌ Error getting reports: {str(e)}")
            
            else:
                print("❌ Invalid choice. Please select 1-5.")
    
    finally:
        client.close()

def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Infobip SMS Application')
    parser.add_argument('-t', '--to', required=False, 
                       help='Phone number(s) to send SMS to (comma-separated)')
    parser.add_argument('-m', '--message', required=False,
                       help='SMS message text')
    parser.add_argument('-s', '--sender', 
                       help='Custom sender ID (optional)')
    parser.add_argument('-f', '--file', 
                       help='File containing phone numbers (one per line)')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--balance', action='store_true',
                       help='Check account balance')
    parser.add_argument('--reports', action='store_true',
                       help='Get delivery reports')
    parser.add_argument('--bulk-id', 
                       help='Bulk ID for delivery reports')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed output')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    client = SMSClient(API_KEY, API_BASE_URL, SENDER_ID)
    
    try:
        if args.balance:
            # Check balance
            balance = client.check_account_balance()
            print(f"💰 Account Balance: {balance.get('amount', 'N/A')} {balance.get('currency', '')}")
        
        elif args.reports:
            # Get delivery reports
            kwargs = {"limit": 50}
            if args.bulk_id:
                kwargs["bulk_id"] = args.bulk_id
            
            reports = client.get_delivery_reports(**kwargs)
            if 'results' in reports and reports['results']:
                print("📊 Recent Delivery Reports:")
                for report in reports['results'][:10]:  # Show last 10
                    status = report.get('status', {}).get('name', 'Unknown')
                    phone = report.get('to', 'Unknown')
                    sent_at = report.get('sentAt', 'N/A')
                    print(f"  {phone}: {status} at {sent_at}")
            else:
                print("📭 No delivery reports found.")
        
        else:
            # Send SMS
            if not args.message:
                print("❌ Error: Message is required. Use -m/--message or -i/--interactive")
                sys.exit(1)
            
            # Get phone numbers
            phones = []
            if args.to:
                phones.extend([p.strip() for p in args.to.split(',')])
            
            if args.file:
                try:
                    with open(args.file, 'r') as f:
                        file_phones = [line.strip() for line in f if line.strip()]
                        phones.extend(file_phones)
                except FileNotFoundError:
                    print(f"❌ Error: File '{args.file}' not found")
                    sys.exit(1)
            
            if not phones:
                print("❌ Error: No phone numbers provided. Use -t/--to or -f/--file")
                sys.exit(1)
            
            # Send SMS
            start_time = time.time()
            response = client.send_sms(phones, args.message, sender=args.sender)
            end_time = time.time()
            
            if args.verbose:
                print(format_response(response, show_details=True))
            else:
                messages = response.get('messages', [])
                success_count = sum(1 for msg in messages if msg.get('status', {}).get('groupName') == 'PENDING')
                total_count = len(messages)
                print(f"📱 SMS sent to {success_count}/{total_count} recipients")
                if response.get('bulkId'):
                    print(f"📦 Bulk ID: {response['bulkId']}")
            
            print(f"⏱️ Completed in {end_time - start_time:.3f} seconds")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    
    finally:
        client.close()

if __name__ == '__main__':
    main()

