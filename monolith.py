from db import database as db 
from db import watchlists as wl
from db import password_db as passwords


def verify(username, pwd):
    if passwords[username] == pwd:
        return True
    return False

def display_listings(data):
    for house in data:
        print(f"""
        id:         {house["id"]}
        address:    {house["address"]}
        price:      {house["price"]}
        bed:        {house["bed"]}
        bath:       {house["bath"]}
        sqft:       {house["sqft"]}
        City:       {house["city"]}
    """)
    return

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
        realtor:    {house["email"]}
        Motivated Seller:  {house["motivated"]}
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
print("---------- HOUSE HUNTER ----------\n\n")

print("""
    Welcome to House Hunter!
    We feature listings through out the state of Oregon
    You can browse our listings, save and track any house that catches your eye
    Find your dream home today!
    """)

print("""\n
    The login process is simple and easy:
    first enter your username
    a second prompt will request your password
    you will then be taken to the main menu
    """)

while True:
    user = input("Please enter your user name: ")
    password = input("Please enter your password: ")

    if verify(user, password):
        break
    print("Invalid attempt, please try again")

while True:
    show_listings = False
    show_details = False
    show_watchlist = False
    show_help = False

    print("---------- MAIN MENU ----------\n\n")
    print("""
        enter one of the following commands to navigate the site
        a) browse listings - see all our available listings
        b) check your watchlist - see properties you have saved
        c) get help - get an overview of our site features
        x) exit the program
        """)
    main_comm = input("enter here: ")

    match main_comm:
        case 'a':
            show_listings = True
        case 'b':
            show_watchlist = True
        case 'c':
            show_help = True
        case 'x':
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
                print("invalid input, returning to details menu")

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









