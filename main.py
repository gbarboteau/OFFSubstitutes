"""Launches the substitute finder program.
Let's you enter a username and a password
who match an existing MySQL account.
"""
import argparse
import getpass

from program import ProgramTerminal
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
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    pt = ProgramTerminal(my_auth)
    pt.launch()

main();