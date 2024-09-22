import os
import sys
import time
import getpass
import platform
from defs.amfCall import AmfCall
from defs.menuList import wheel_spins, lisa_hack, block_defaults

#ver.0.3.2

# Cls/Clear
def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Funkcja logowania.
def input_login():
    login = input("Login: ")
    password = getpass.getpass("Password: ")
    return login, password

# Zapisywanie pasow do pliku .txt.
def save_account(login, password, file_dir):
    clear()
    with open(file_dir, 'a') as plik:  # Otwieranie pliku w trybie dopisywania.
        plik.write(f"{login},{password}\n")
    print("Account saved to .txt file.")

# Wybieranie serwera.
def server_picker():
    clear()
    print("CHOOSE SERVER:     (USA server not implemented)")
    print("1. PL")
    print("2. UK")
    print("3. DE")
    print("4. USA")
    
    sv_choice = input("Choice: ")
    
    servers = {
        "1": "PL",
        "2": "UK",
        "3": "DE",
        "4": "USA"
    }
    
    return servers.get(sv_choice, "PL") # If sv_choice is uncorrect - default server is "PL".

# Request sending, response translate.
def login_to_msp(login, password, server):
    clear()
    status_code, response_amf = AmfCall(server, 'MovieStarPlanet.WebService.User.AMFUserServiceWeb.Login',
                                        [
                                            login,
                                            password,
                                            [],
                                            None,
                                            None,
                                            'MSP1-Standalone:XXXXXX'
                                        ])

    logged_in = response_amf.get('loginStatus', {}).get('status')
    locked_status = response_amf.get('loginStatus', {}).get('statusDetails')
    # Response checking from 'response.amf'.
    if logged_in == "InvalidCredentials":
        print("Invalid username or password, check your spelling.")
        return None, None, None  # Return None if login failed.
    elif locked_status == "LockPermanent":
        print("Account is permanently locked.")
        return None, None, None  # Return None if account is locked.
    elif logged_in == "Success":
        print(f"Login successfull! Logged in as {login}.")
        actorId = response_amf['loginStatus']['actor']['ActorId']
        name = response_amf["loginStatus"]["actor"]["Name"]
        ticket = response_amf['loginStatus']['ticket']
        accessToken = response_amf["loginStatus"]["nebulaLoginStatus"]["accessToken"]
        profileId = response_amf["loginStatus"]["nebulaLoginStatus"]["profileId"]
        return server, actorId, ticket
    else:
        print("Login error. Please try again.")
        return None, None, None  # Return None if other error.

# Menu funkcji.
def menu(server, actorId, ticket):
    clear()    
    print("What do you want to do now?")
    print(" ")
    print("     1. Lisa Hack")
    print(" ")
    print("     2. Wheel Spin")
    print(" ")
    print("     3. Block Pixie, Zac, etc.")
    print(" ")
    print("     4. Exit")
    print(" ")
    
    menu_choice = input("Choice: ")
    
    functions = {
        "1": lambda:lisa_hack(server, actorId, ticket),
        "2": lambda:wheel_spins(server, actorId, ticket),
        "3": lambda:block_defaults(server, actorId, ticket),
        "4": lambda:sys.exit(0)
    }
    
    action = functions.get(menu_choice)
    if action:
        action()
    else:
        print("Invalid choice. Please select again.")
        time.sleep(2)
    
# Glowna funkcja.
def main():
    login, password = input_login() # Call login procedure.
    
    file_dir = r"accounts.txt"
    save_account(login, password, file_dir) # Call account logging procedure.
    
    server = server_picker() # Call server picker.
    
    server, actorId, ticket = login_to_msp(login, password, server) # Call login request to AMF with 3 arguments.
    
    if server and actorId and ticket:  # Proceed ONLY if login was successful.
        time.sleep(2)
        while True:
            menu(server, actorId, ticket)  # Keep showing menu after each action

if __name__ == "__main__":
    main()

