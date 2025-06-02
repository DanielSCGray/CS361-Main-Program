from communications import send_data, send_text,  read_req

# Communication Pipes
request_file = "acct_request.txt"
acct_response = "acct_resp.txt"
# Acct Data
accounts = {
    "bob": {"username": "bob", "password": "a", "email": "bob@mail.com"}
}

def process_req(request_code, data):
    match request_code:
        case "username":
            if data["username"] in accounts.keys():
                send_text(acct_response, "invalid")
                print("username is taken")
            else:
                send_text(acct_response, "valid")
                print("valid username")
        case "login":
            if data["username"] in accounts.keys():
                if accounts[data["username"]]["password"] == data["password"]:
                    send_data(acct_response, accounts[data["username"]], "valid")
                else:
                    send_data(acct_response, [], "invalid")
                    print("invalid request")
            else:
                    send_data(acct_response, [], "invalid")
                    print("invalid request")
        case "create":
            accounts[data["username"]] = data
            send_data(acct_response, data)
            print("account created")

def main():
    while True:
        request_code, data = read_req(request_file)
        if request_code:
            print(f"{request_code} request received")
            process_req(request_code, data)

if __name__ == "__main__":
    main()