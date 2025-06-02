from communications import send_data, read_req
from datetime import date
# Communication Pipes
request_file = "add_request.txt"
resp_file = "add_resp.txt"

def process_house(data):
    data["ppf"] = round(data["price"] / data["sqft"], 2)
    data["city"] = data["city"].capitalize()
    data["address"] = data["address"].title()
    data["date"] = str(date.today())
    return data

def main():


    while True:

        request_code, data = read_req(request_file)
        if request_code:
            print(f"{request_code} request received")
            new_data = process_house(data)
            send_data(resp_file, new_data)
            print("response sent")


if __name__ == "__main__":
    main()