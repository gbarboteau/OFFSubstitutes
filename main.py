"""Launches the substitute finder program.
Let's you enter a username and a password
who match an existing MySQL account.
"""
import argparse
import getpass

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
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    if args.terminal:
        pr = ProgramTerminal(my_auth)
    else:
        pr = ProgramTerminal(my_auth)
    pr.launch()

main();