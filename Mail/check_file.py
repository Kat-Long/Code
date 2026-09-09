import os
sz = os.path.getsize('extract_v3_full.txt')
print(f'File size: {sz} bytes')

import subprocess
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
lines = [l for l in result.stdout.splitlines() if l.strip()]
print(f'Python processes: {len(lines)}')