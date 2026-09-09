import os
import time

for i in range(30):
    time.sleep(10)
    sz = os.path.getsize('extract_v3_final.txt')
    print(f'Check {i+1}: Size = {sz} bytes')
    if sz > 100000:
        print('File is growing, script is running...')