from communications import send_data, send_text, read_data, read_req, read_text
from db import accounts_db as accounts


request_file = "acct_request.txt"

acct_response = "acct_resp.txt"

def process_req(request_code, data):
    match request_code:
        case "username":
            if data["username"] in accounts.keys():
                send_text(acct_response, "invalid")
            else:
                send_text(acct_response, "valid")
        case "login":
            if data["username"] in accounts.keys():
                if accounts[data["username"]]["password"] == data["password"]:
                    send_data(acct_response, accounts[data["username"]], "valid")
                else:
                    send_data(acct_response, [], "invalid")
            else:
                    send_data(acct_response, [], "invalid")
        case "create":
            accounts[data["username"]] = data
            send_data(acct_response, data)


def main():


    while True:

        request_code, data = read_req(request_file)
        if request_code:
            process_req(request_code, data)

if __name__ == "__main__":
    main()