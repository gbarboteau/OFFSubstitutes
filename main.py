import argparse
import getpass

from program import ProgramTerminal
import auth

def main():
    parser = argparse.ArgumentParser()
    my_auth = auth.Auth()
    parser.add_argument("user", help="is the user for the database")
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    pt = ProgramTerminal(my_auth)
    pt.launch()

main();