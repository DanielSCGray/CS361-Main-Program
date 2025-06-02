from communications import send_text, read_req
import re
# Communication Pipes
request_file = "form_request.txt"
resp_file = "form_resp.txt"

def pwd_validation(pwd):
    if len(pwd) < 8 or len(pwd) > 20:
        return False
    has_lc, has_uc, has_num = False, False, False
    for char in pwd:
        if char.islower():
            has_lc = True
        if char.isupper():
            has_uc = True
        if char in "0123456789":
            has_num = True
    if has_lc and has_uc and has_num:
        return True
    return False

def email_validation(email):
    email_reg = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_reg, email):
        return True
    else:
        return False

def validate_house(data):
    if data["price"] < 50000 or data["sqft"] < 500:
        return False
    if data["bed"] < 1 or data["bath"] < 1:
        return False
    return True

def process_req(request_code, data):
    match request_code:
        case "password":
            if pwd_validation(data["password"]):
                send_text(resp_file, "valid")
                print("valid")
            else:
                send_text(resp_file, "rejected")
                print("invalid request")
        case "email":
            if email_validation(data["email"]):
                send_text(resp_file, "valid")
                print("valid")
            else:
                send_text(resp_file, "rejected")
                print("invalid request")
        case "house":
            if validate_house(data):
                send_text(resp_file, "valid")
                print("valid")
            else:
                send_text(resp_file, "rejected")
                print("invalid request")

def main():


    while True:

        request_code, data = read_req(request_file)
        if request_code:
            print(f"{request_code} request received")
            process_req(request_code, data)


if __name__ == "__main__":
    main()