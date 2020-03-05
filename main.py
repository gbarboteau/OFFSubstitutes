"""Launches the substitute finder program.
Let's you enter a username and a password
who match an existing MySQL account.
"""
import argparse
import getpass
import mysql.connector

from program import ProgramGraphic, ProgramTerminal
from auth import Auth


def main():
    """Checks for a matching username/password
    combination, then launches the program.
    The user needs to enter his username as an
    argument, then the password afterwards.
    """
    parser = argparse.ArgumentParser()
    my_auth = Auth()
    parser.add_argument("user", help="is the user for the database")
    parser.add_argument("-t", "--terminal", help="Launches the program in terminal mode", action="store_true")
    parser.add_argument("-g", "--graphic", help="Launches the program in graphic mode", action="store_true")
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    try:
        my_connection = mysql.connector.connect(user=my_auth.user, password=my_auth.password, database='openfoodfacts')
        my_connection.close()
        if args.terminal:
            pr = ProgramTerminal(my_auth)
        elif args.graphic:
            pr = ProgramGraphic(my_auth)
        else:
            pr = ProgramGraphic(my_auth)
        pr.launch()
    except mysql.connector.errors.ProgrammingError:
        print("This user/password combination doesn't exist! Try another combination.")
    

main();