#!/usr/bin/env python3
import requests
import json

# Configuration
API_BASE_URL = "https://qd9ver.api.infobip.com"
SENDER_ID = "Isuzu_EA"
API_KEY = "3ac40821cb2173d277d7f0c2bfbcb8ef-35d902cd-7b2b-4dae-ba99-14ffc33efd4c"

# Test payload
payload = {
    "messages": [{
        "from": SENDER_ID,
        "destinations": [{"to": "+254721446106"}],
        "text": "Test message from debug script",
        "notifyUrl": "",
        "notifyContentType": "application/json",
        "callbackData": "",
        "validityPeriod": 720
    }]
}

print("Sending payload:")
print(json.dumps(payload, indent=2))
print("\n" + "="*50 + "\n")

# Send request
headers = {
    'Authorization': f'App {API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

url = f"{API_BASE_URL}/sms/2/text/advanced"

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text}")
    
    if response.status_code != 200:
        print("\nError Details:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print("Could not parse error response as JSON")
            
except Exception as e:
    print(f"Request failed: {str(e)}")

