from communications import send_data, send_text, read_data, read_req, read_text
import time
import json
from datetime import date


request_file = "listing_request.txt"
resp_file = "listing_resp.txt"

def process_house(data):
    data["ppf"] = round((data["price"] / data["sqft"], 2))
    data["city"] = data["city"].capitalize()
    data["address"] = data["address"].title()
    data["date"] = date.today()
    return data

def main():


    while True:
        time.sleep(.103)

        request_code, data = read_data(request_file)
        if request_code:
            new_data = process_house(request_code, data)
            send_data(resp_file, new_data)


if __name__ == "__main__":
    main()