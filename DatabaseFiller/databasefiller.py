"""The program filling the openfoodfacts database
with entries for its different categories.
"""
import argparse
import getpass
import mysql.connector

import datacollecter
import filler
import auth


def main():
    """Checks for a matching username/password
    combination, then fill the openfoodfacts database.
    """
    parser = argparse.ArgumentParser()
    my_auth = auth.Auth()
    parser.add_argument("user", help="is the user for the database")
    args = parser.parse_args()
    my_auth.user = args.user
    my_auth.password = getpass.getpass()
    try:
        my_connection = mysql.connector.connect(user=my_auth.user, password=my_auth.password, database='openfoodfacts')
        my_connection.close()
        dt = datacollecter.DataCollecter(my_auth)
        my_data = dt.my_data
        fil = filler.Filler(my_data, my_auth)
        fil.put_it_in_tables()
    except mysql.connector.errors.ProgrammingError:
        print("This user/password combination doesn't exist! Try another combination.")

main();
