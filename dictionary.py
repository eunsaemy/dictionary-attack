import pwd
import crypt
import getpass
from hmac import compare_digest as compare_hash
import os

DICTIONARY = ""
SHADOW = ""
USERS = []

def is_exist(path):
    return os.path.exists(path)

def is_file(path):
    return os.path.isfile(path)

def set_shadow():
    global SHADOW
    path = input("Path to shadow file [default=/current_directory/shadow]: ")
    path = path.strip()
    path = path.replace(" ", "")

    if path is not None and path !="":
        if is_exist(path) and is_file(path):
            SHADOW = path
        else:
            print("\nInvalid shadow path. Input was: {0}".format(path))
            print("Please try again.\n")
            set_shadow()
    else:
        SHADOW = os.path.join(os.getcwd(), "shadow")

def set_dictionary():
    global DICTIONARY
    path = input("Path to dictionary file [default=/current_directory/rockyou.txt]: ")
    path = path.strip()
    path = path.replace(" ", "")

    if path is not None and path != "":
        if is_exist(path) and is_file(path):
            DICTIONARY = path
        else:
            print("\nInvalid dictionary path. Input was: {0}".format(path))
            print("Please try again.\n")
            set_dictionary()
    else:
        DICTIONARY = os.path.join(os.getcwd(), "rockyou.txt")

def set_users():
    with open(SHADOW, "r") as shadow:
        for line in shadow:
            split1 = line.split(":")
            split2 = line.split("$")

            username = split1[0]
            hashed_password = split1[1]

            try:
                yescrypt1 = "$y$"
                yescrypt2 = "$7$"

                if yescrypt1 in split1[1] or yescrypt2 in split1[1]:
                    salt = f"${split2[1]}${split2[2]}${split2[3]}$"
                    user = [username, salt, hashed_password]
                else:
                    salt = f"${split2[1]}${split2[2]}$"
                    user = [username, salt, hashed_password]
                USERS.append(user)
            except IndexError:
                pass

def dictionary_attack():
    for x in range(len(USERS)):
        username = USERS[x][0]
        salt = USERS[x][1]
        hashed_password = USERS[x][2]

        print("Looking for a password match for user: {0}...".format(username))

        with open(DICTIONARY, "r") as dictionary:
            for word in dictionary:
                password = word.strip()
                
                if crypt.crypt(password, salt) == hashed_password:
                    print("username: {0} | password: {1}".format(username, password))

                    with open(os.path.join(os.getcwd(), "password.log"), "a") as f:
                        f.write("username: " + username + " | password: " + password + "\n")
                    break

if __name__ == "__main__":
    set_shadow()
    set_dictionary()
    set_users()

    dictionary_attack()
