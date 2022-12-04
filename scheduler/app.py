import datetime
import os
import time

import requests


while True:
    try:
        print(f'[EXECUTING BACKGROUND TASK] {datetime.datetime.now().isoformat()}')

        backend_url = os.getenv('BACKEND_URL')
    
        if backend_url is not None:
            backend_url = 'http://172.17.0.1:7002'
        
        requests.get(f'{backend_url}/predict-scheduler')

        # Predict dummy if defined
        if os.getenv('PREDICT_DUMMY') == 'yes':
            requests.get(f'{backend_url}/predict-dummy')

    except:
        print(e)

    sleep_interval = os.getenv('SCHEDULER_INTERVAL')

    try:
        sleep_interval = int(sleep_interval)
    except Exception as e:
        sleep_interval = 60

    
    time.sleep(sleep_interval)