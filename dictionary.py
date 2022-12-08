#!/usr/bin/env python

###########################################################################################
# FILE
#
#   Name:  dictionary.py
#
#   Developer:  Eunsaem Lee
#
#   Date:       2022-12-08
#
#   Description:
#     A dictionary-based password cracker for Fedora 36. It compares the words in
#     dictionary file to the passwords in shadow file, and prints out username and password
#     if there is a match.
#
###########################################################################################

from hmac import compare_digest as compare_hash
import crypt
import os
import sys

# Path to dictionary file
DICTIONARY = ""
# Path to shadow file
SHADOW = ""
# List of users in the shadow file
USERS = []

###########################################################################################
# FUNCTION
#
#   Name:  is_exist
#
#   Parameters:
#     path      - path to a file
#
#   Returns:
#     True      - path is VALID
#     False     - path is INVALID
#
#   Description:
#     Determines whether path is valid.
#
###########################################################################################
def is_exist(path):
    return os.path.exists(path)

###########################################################################################
# FUNCTION
#
#   Name:  is_file
#
#   Parameters:
#     path      - path to a file
#
#   Returns:
#     True      - path is a file
#     False     - path is is NOT a file
#
#   Description:
#     Determines whether path is a file.
#
###########################################################################################
def is_file(path):
    return os.path.isfile(path)

###########################################################################################
# FUNCTION (SETTER)
#
#   Name:  set_shadow
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Sets file path of shadow file. If input is "exit", exit the program. If invalid
#     input, re-ask for shadow file path.
#
###########################################################################################
def set_shadow():
    global SHADOW
    path = input("Path to shadow file [default=/current_directory/shadow]: ")
    path = path.strip()
    path = path.replace(" ", "")

    if path is not None and path !="":
        if is_exist(path) and is_file(path):
            SHADOW = path
        elif path == "exit":
            print("\nGoodbye.")
            sys.exit(0)
        else:
            print("\nInvalid shadow path. Input was: {0}".format(path))
            print("Please try again.\n")
            set_shadow()
    else:
        SHADOW = os.path.join(os.getcwd(), "shadow")

###########################################################################################
# FUNCTION (SETTER)
#
#   Name:  set_dictionary
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Sets file path of dictionary file. If input is "exit", exit the program. If invalid
#     input, re-ask for dictionary file path.
#
###########################################################################################
def set_dictionary():
    global DICTIONARY
    path = input("Path to dictionary file [default=/current_directory/rockyou.txt]: ")
    path = path.strip()
    path = path.replace(" ", "")

    if path is not None and path != "":
        if is_exist(path) and is_file(path):
            DICTIONARY = path
        elif path == "exit":
            print("\nGoodbye.")
            sys.exit(0)
        else:
            print("\nInvalid dictionary path. Input was: {0}".format(path))
            print("Please try again.\n")
            set_dictionary()
    else:
        DICTIONARY = os.path.join(os.getcwd(), "rockyou.txt")

###########################################################################################
# FUNCTION (SETTER)
#
#   Name:  set_users
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Reads user information from shadow file and appends them to USERS list.
#
#     USERS     - list of users in the shadow file
#                 [user1, user2, ...]
#     user      - list of user information
#                 [username, salt value, hashed_password]
#
###########################################################################################
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

###########################################################################################
# FUNCTION
#
#   Name:  dictionary_attack
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Determines whether dictionary word matches password from shadow file.
#
###########################################################################################
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

###########################################################################################
# FUNCTION (MAIN)
#
#   Name:  main
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Asks user for shadow and dictionary file paths. Runs the dictionary-based attack.
#
###########################################################################################
def main():
    set_shadow()
    set_dictionary()
    set_users()

    dictionary_attack()

###########################################################################################
# FUNCTION (DRIVER)
#
#   Name:  main
#
#   Parameters:
#     None.
#
#   Returns:
#     None.
#
#   Description:
#     Calls the main function.
#
###########################################################################################
if __name__ == "__main__":
    main()
