import argparse
import getpass

import datacollecter
import filler
import auth

def main():
	parser = argparse.ArgumentParser()
    my_auth = auth.Auth()
    parser.add_argument("user", help="is the user for the database")
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    dt = datacollecter.DataCollecter(my_auth)
    my_data = dt.my_data
    fil = filler.Filler(my_data, my_auth)
    fil.put_it_in_tables()

main();
