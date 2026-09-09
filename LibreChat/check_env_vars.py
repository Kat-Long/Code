#!/usr/bin/env python3
import requests
import json

render_api_key = 'rnd_ABi2u4FwRw68B9newWOeEP01b3zg'
service_id = 'srv-d8i4aa48aovs73f6ka00'

headers = {
    'Authorization': f'Bearer {render_api_key}',
    'Content-Type': 'application/json'
}

url = f'https://api.render.com/v1/services/{service_id}'

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        env_vars = data.get('envVars', [])
        print('\n=== Current Environment Variables ===')
        for var in env_vars:
            key = var.get('key', 'Unknown')
            value = var.get('value', 'Not set')
            if 'REGISTRATION' in key or 'JWT' in key or 'PORT' in key:
                if len(str(value)) > 50:
                    print(f'{key}: {str(value)[:50]}...')
                else:
                    print(f'{key}: {value}')
    else:
        print(f'Error: {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')
