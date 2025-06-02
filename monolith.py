from db import database as db 
from db import watchlists as wl
from communications import send_data, send_text, read_data, read_req, read_text, send_search
import time



def display_listings(data):
    for house in data:
        print(f"""
        id:         {house["id"]}
        address:    {house["address"]}
        price:      {house["price"]}
        bed:        {house["bed"]}
        bath:       {house["bath"]}
        sqft:       {house["sqft"]}
        city:       {house["city"]}
    """)
    return
def display_search(data):
    for house in data:
        print(f"""
        id:         {house["id"]}
        address:    {house["address"]}
        price:      {house["price"]}
        bed:        {house["bed"]}
        bath:       {house["bath"]}
        sqft:       {house["sqft"]}
        city:       {house["city"]}
        list date:  {house["date"]}
        $/sqft:     {house["ppf"]}
        contact:    {house["email"]}
        """)

def display_details(num, db):
    house = db[num]
    print(f"""
        id:         {house["id"]}
        address:    {house["address"]}
        price:      {house["price"]}
        bed:        {house["bed"]}
        bath:       {house["bath"]}
        sqft:       {house["sqft"]}
        City:       {house["city"]}
        List Date:  {house["date"]}
        $/sqft:     {house["ppf"]}
        contact:    {house["email"]}
    """)
    return

def display_wl(arr):
    for i in range(len(arr)):
        display_details(i,arr)
    return

def remove_from_wl(arr, id):
    for i in range(len(arr)):
        house =arr[i]
        if house["id"] == id:
            arr.pop(i)
            return
    print("listing id not found")


# help msgs

add_help= """
To add a property to your watchlist:
select the main menu (m)
select listings (a)
select details (a)
enter the id of the house you want to add
enter y when asked if you want to add the property
the command sequence from this page is: m-a-a-id#-y"""

remove_help = """
To remove a watchlist property
select the main menu (m)
select watchlist (b)
select remove a property (a)
enter the id of the house you want to remove
enter y when asked to confirm
the command sequence from this page is: m-b-a-id#-y"""
exit_help = """
To exit
select the main menu (m)
select exit (x)
enter y when asked to confirm
the command sequence from this page is: m-x-y
"""

#Files
acct_request = "acct_request.txt"
acct_response = "acct_resp.txt"
form_request = "form_request.txt"
form_response ="form_resp.txt"
add_listing_request = "add_request.txt"
add_listing_response = "add_resp.txt"
search_request= 'request.txt'
search_response = 'results.txt'

print("---------- HOUSE HUNTER ----------\n\n")



print("""\n
    The login process is simple and easy:
    first enter your username
    a second prompt will request your password
    you will then be taken to the main menu
    """)
def main():
    while True:
        print("""
        enter one of the following commands to navigate the site
        a) log in
        b) create new account
        """)
        user_data = {}
        comm = input("enter here: ")
        match comm:
            case "a":
                #pwd login
                while True:
                    user_data["username"] = input("Please enter your user name: ")
                    
                    user_data["password"] = input("Please enter your password: ")

                    send_data(acct_request, user_data, "login")
                    # set this up to read data
                    resp, data = read_req(acct_response)
                    print("resp: ", resp)
                    if resp == "valid":
                        user_data = data
                        break
                    print("Invalid attempt, please try again")
            case "b": # Account Creation
                # Confirm unique user name
                while True:
                    user_data["username"] = input("Please enter your user name: ")
                    # sends data to Accounts MS through acct_request pipe 
                    send_data(acct_request, user_data, "username")
                    # reads response from acct_response pipe
                    if not read_text(acct_response) == "valid":
                        continue
                    break
                # Validate Password
                while True:
                    print("paswords must be 8-20 characters")
                    print("Passwords must contain an uppercase letter, a lowercase letter and a number")
                    user_data["password"] = input("Please enter your password: ")
                    # sends data to form validation through form_request pipe 
                    send_data(form_request, user_data, "password")
                    if not read_text(form_response) == 'valid':
                        print("Invalid password")
                        continue
                    break
                while True:
                    user_data["email"] = input("Please enter your email: ")
                    send_data(form_request, user_data, "email")
                    if not read_text(form_response) == 'valid':
                        print("Invalid email")
                        continue
                    break
            case _:
                print("invalid command")
                continue
        break

    user = user_data["username"]
    while True:
        show_listings = False
        show_details = False
        show_watchlist = False
        show_help = False
        show_add_listing = False
        show_search = False

        print("---------- MAIN MENU ----------\n\n")

        print("""
        Welcome to House Hunter!
        We feature listings through out the state of Oregon.
        You can browse through listings for general information,
        select properties to learn more details,
        and save prorties that catch your eye to your personal watchlist.
        
        Find your dream home today!
        """)

        print("""
            enter one of the following commands to navigate the site
            a) browse listings - see all our available listings
            b) check your watchlist - see properties you have saved
            c) search listings - search listings with specific criteria
            d) add a listing - post a property for sale
            e) get help - get an overview of our site features
            x) exit the program
            """)
        main_comm = input("enter here: ")

        match main_comm:
            case 'a':
                show_listings = True
            case 'b':
                show_watchlist = True
            case 'c':
                show_search = True
            case 'd':
                show_add_listing = True
            case 'e':
                show_help = True
            case 'x':
                print("exiting will log you out and end your session")
                confirm = input("are you sure you want to exit (y/n)?")
                if confirm == 'y':
                    break
            case _:
                print("invalid input, please try again")
        
        while show_listings:
            print("---------- LISTINGS ----------\n\n")
            display_listings(db)
            print("""
                enter one of the following commands
                a) details - get detailed information about a property 
                m) return to main menu
                """)
            listing_comm = input("enter here: ")

            match listing_comm:
                case 'a':
                    show_details = True
                case 'm':
                    show_listings =False
                case _:
                    print("invalid input, please try again")
            while show_details:
                print(f"each property has a unique ID between 1 and {len(db)}")
                selection = input("enter the ID of the property you want to see more about: ")
                selection = int(selection)
                selection -= 1
                if selection in range(len(db)):
                    display_details(selection, db)
                    print("""House Hunter allows you to save properties to your personal watchlist.
                        while it is possible to add as many houses as you want, we recommend keeping 
                        an orderly list by only adding properties that make sense for you.\n""")
                    add = input("add this property to your watchlist(y/n)? ")
                    if add == 'y':
                        wl[user].append(db[selection])
                else:
                    print("invalid listing")
                print("""
                enter one of the following commands
                a) select another property 
                b) return to listings
                m) return to main menu
                """)
                details_comm = input("enter here: ")
                match details_comm:
                    case 'a':
                        continue
                    case 'b':
                        show_details = False
                    case 'm':
                        show_details = False
                        show_listings =False
                    case _:
                        print("invalid input, returning to details menu")

        while show_watchlist:
            print("---------- WATCHLIST ----------\n\n")
            display_wl(wl[user])
            print("""
            enter one of the following commands
            a) remove a property 
            m) return to main menu
            """)
            watch_comm = input("enter here: ")
            match watch_comm:
                case 'a':
                    target = int(input("select an id to delete: "))
                    print("this property will be removed from your watchlist and must be manually added back")
                    confirm = confirm = input("are you sure you want to remove this (y/n)?")
                    if confirm == 'y':
                        remove_from_wl(wl[user], target)
                case 'm':
                    show_watchlist = False
                    
                case _:
                    print("invalid input")

        while show_help:
            print("---------- HELP ----------\n\n")
            print("""
            select a topic to learn more about
            a) how to add a property to my watchlist 
            b) how to remove a property from my watchlist
            c) how to exit
            m) return to main menu
            """)
            help_comm = input("enter here: ")
            match help_comm:
                case 'a':
                    print(add_help)
                case 'b':
                    print(remove_help)
                case 'c':
                    print(exit_help)
                case 'm':
                    show_help = False
                case _:
                    print("invalid input, please try again")
        
        while show_search:
            print("---------- SEARCH LISTINGS ----------\n\n")
            print("""
            enter one of the following commands
            a) search for a property
            m) return to main menu
            """)
            search_comm = input("enter here: ")
            match search_comm:
                case 'a':
                    search_params = {"price_range": None, "min_beds": None, "min_baths": None, "city": None }
                    while True:
                        print("""
                        add criteria to your search and then execute with the following commands
                        a) set price range
                        b) set minimum bedrooms
                        c) set minimum bathrooms
                        d) select a city
                        e) submit search and see results
                        """)
                        command = input("enter here: ")
                        match command:
                            case 'a':
                                min_price = int(input("enter minimum price: "))
                                max_price = int(input("enter maximum price: "))
                                search_params["price_range"] = [min_price, max_price]
                            case 'b':
                                search_params["min_beds"] = int(input("enter minimum bedrooms: "))
                            case 'c':
                                search_params["min_baths"] = int(input("enter minimum bathrooms: "))
                            case 'd':
                                search_params["city"] = int(input("enter city: "))
                            case 'e':
                                print("Your Results")
                                # Send Search request
                                send_search(search_request, db, search_params)
                                # Read response and display
                                results = read_data(search_response)
                                display_search(results)
                                break
                            case _:
                                print("invalid input, please try again")


                case 'm':
                    show_search = False
                case _:
                    print("invalid input, please try again")

        while show_add_listing:
            print("---------- LIST FOR SALE ----------\n\n")
            print("""
            enter one of the following commands
            a) list a property for sale 
            m) return to main menu
            """)
            house_for_sale = {"id": len(db)+1, "email": user_data["email"]}
            add_comm = input("enter here: ")
            match add_comm:
                case 'a':
                    house_for_sale["address"] = input("enter the property address: ")
                    house_for_sale["price"] = int(input("enter the asking price in thousands: ")) * 1000
                    house_for_sale["bed"] = int(input("enter the number of bedrooms: "))
                    house_for_sale["bath"] = int(input("enter the number of bathrooms: "))
                    house_for_sale["sqft"] = int(input("enter the property's square footage: "))
                    house_for_sale["city"] = input("enter the city the property is located in: ")
                    # Request form validation
                    send_data(form_request, house_for_sale, "house")
                    print("Validating listing...")
                    # Read validation response
                    if read_text(form_response) == 'valid':
                        # Send Valid data to Add Listings Microservice
                        send_data(add_listing_request, house_for_sale, "create")
                        # Read Listing Response
                        # time.sleep(.5)
                        new_listing = read_data(add_listing_response)
                        db.append(new_listing)
                        print("New Listing created:")
                        display_details(-1, db)
                        
                    else: 
                        print("Invalid listing")
                        
                case 'm':
                    show_add_listing = False
                case _:
                    print("invalid input, please try again")




if __name__ == "__main__":
    main()





