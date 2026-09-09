import time
import os

print("Waiting for script to finish...")
time.sleep(45)

sz = os.path.getsize('extract_v3_profiles.txt')
print(f'File size: {sz} bytes')