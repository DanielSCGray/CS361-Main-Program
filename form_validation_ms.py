from communications import send_data, send_text, read_data, read_req, read_text
import time
import json
import re

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

def house_validation(house):
    pass

def process_req(request_code, data):
    match request_code:
        case "password":
            if pwd_validation(data["password"]):
                send_text(resp_file, "valid")
            else:
                send_text(resp_file, "rejected")
        case "email":
            if email_validation(data["email"]):
                send_text(resp_file, "valid")
            else:
                send_text(resp_file, "rejected")
        case "house":
            if type(data["beds"]) == int and type(data["baths"]) == int :
                send_text(resp_file, "valid")
            else:
                send_text(resp_file, "rejected")

def main():


    while True:

        request_code, data = read_req(request_file)
        if request_code:
            process_req(request_code, data)


if __name__ == "__main__":
    main()