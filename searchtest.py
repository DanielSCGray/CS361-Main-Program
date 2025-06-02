import json
import time
from db import database as db

def send_data(data:list, file_name:str, params:dict):
    with open(file_name, 'w') as f:
        f.write(json.dumps(params))
        f.write("\n")
        datastr = json.dumps(data)
        f.write(datastr)

def read_data(file_name):
        time.sleep(.11111)
        with open(file_name, 'r') as f:
            data = f.read()
        with open(file_name, 'w') as f:
            pass
        if data:
            return json.loads(data)

def display(arr):
    for house in arr:
        print(f'{house["price"]}, {house["bed"]}, {house["bath"]}, {house["city"]}')

rq_file = "request.txt"
resp_file = "results.txt"

p1 = {"price_range": None, "min_beds": None, "min_baths": None, "city": None }
p2 = {"price_range": [0,500000], "min_beds": None, "min_baths": None, "city": None }
p3 = {"price_range": None, "min_beds": 5, "min_baths": None, "city": None }
p4 = {"price_range": None, "min_beds": None, "min_baths": 3, "city": None }
p5 = {"price_range": None, "min_beds": None, "min_baths": None, "city": "Eugene" }
p6 = {"price_range": [1500000, 2000000], "min_beds": 5, "min_baths": None, "city": None }
p7 = {"price_range": [1500000, 2000000], "min_beds": 5, "min_baths": None, "city": "Eugene" }


def main():
    print("\n all none:")
    send_data(db, rq_file, p1)
    display(read_data(resp_file))
    print("\nprice under 500000")
    send_data(db, rq_file, p2)
    display(read_data(resp_file))
    print("\n 5 beds")
    send_data(db, rq_file, p3)
    display(read_data(resp_file))
    print("\n 3 baths")
    send_data(db, rq_file, p4)
    display(read_data(resp_file))
    print("\n eugene:")
    send_data(db, rq_file, p5)
    display(read_data(resp_file))
    print("\n big cost:")
    send_data(db, rq_file, p6)
    display(read_data(resp_file))
    print("\n no match:")
    send_data(db, rq_file, p7)
    display(read_data(resp_file))

if __name__ == "__main__":
    main()