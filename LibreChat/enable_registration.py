#!/usr/bin/env python3
import requests
import json

render_api_key = 'rnd_ABi2u4FwRw68B9newWOeEP01b3zg'
service_id = 'srv-d8i4aa48aovs73f6ka00'

headers = {
    'Authorization': f'Bearer {render_api_key}',
    'Content-Type': 'application/json'
}

# 設定する環境変数
env_vars_to_set = [
    {'key': 'REGISTRATION_ENABLED', 'value': 'true'},
]

url = f'https://api.render.com/v1/services/{service_id}/env-vars'

for env_var in env_vars_to_set:
    try:
        print(f"Setting {env_var['key']} = {env_var['value']}")
        response = requests.post(url, json=env_var, headers=headers, timeout=10)
        print(f'Status Code: {response.status_code}')
        if response.status_code != 201:
            print(f'Response: {response.text}')
        else:
            print(f'✓ {env_var["key"]} was set successfully')
    except Exception as e:
        print(f'Error: {str(e)}')

print('\n=== Now triggering redeploy ===')

# 再デプロイ
redeploy_url = f'https://api.render.com/v1/services/{service_id}/deploys'
try:
    response = requests.post(redeploy_url, headers=headers, timeout=10)
    print(f'Redeploy Status Code: {response.status_code}')
    if response.status_code in [200, 201]:
        print('✓ Redeploy triggered successfully')
    else:
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')
