import json
import time

def send_data(file_name:str, data:list, command=None):
    with open(file_name, 'w') as f:
        if command:
            command = str(command)
            f.write(f'{command}\n')
        datastr = json.dumps(data)
        f.write(datastr)

def send_text(file_name:str, message:str):
    with open(file_name, 'w') as f:
        f.write(message)
        
def read_data(file_name):
        time.sleep(.11111)
        with open(file_name, 'r') as f:
            data = f.read()
        with open(file_name, 'w') as f:
            pass
        return json.loads(data)

def read_req(file_name):
    
        time.sleep(.111111)
        # read contents
        with open(file_name, 'r') as f:
            method = f.readline().strip()
            data = f.readline().strip()
        if method:
            with open(file_name, 'w') as f:
                pass
            return method, json.loads(data)
        return None, None

def read_text(file_name):
    time.sleep(.111)
    with open(file_name, 'r') as f:
            text = f.readline()
    with open(file_name, 'w') as f:
        pass
    return text
