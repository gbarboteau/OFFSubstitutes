"""Fill the database with the data collected by
datacollecter.py
"""
import mysql.connector


class Filler:
    """Adds a set of data in the openfoodfacts
    database. Needs to be authentificated.
    """
    def __init__(self, my_data, my_auth):
        """Create an instance of Filler"""
        self.user = my_auth.user
        self.password = my_auth.password
        self.my_data = my_data

    def put_it_in_tables(self):
        """Put all the data given at the instance creation
        into the database.
        """
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor(buffered=True)
        for i in self.my_data:
            prod_name = i['product_name']
            try:
                add_aliment = ("INSERT INTO aliment "
                       "(product_name, product_description, barcode, nutritional_score, stores, product_category) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")
                data_aliment = (i['product_name'].replace("'", "''"), i['product_description'].replace("'", "''"), i['barcode'].replace("'", "''"), i['nutritional_score'].replace("'", "''"), i['stores'].replace("'", "''"), i['product_category'].replace("'", "''"))
                cursor.execute(add_aliment, data_aliment)
            except mysql.connector.IntegrityError:
                pass 
        my_connection.commit()
        cursor.close()
        my_connection.close()
        print("ok c'est fait")
