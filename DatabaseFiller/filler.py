import mysql.connector

class Filler:
    def __init__(self, my_data, my_auth):
        self.user = my_auth.user
        self.password = my_auth.password
        self.my_data = my_data

    def put_it_in_tables(self):
        for i in self.my_data:
            print(i)
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')

        cursor = my_connection.cursor()

        for i in self.my_data:

            add_aliment = ("INSERT INTO aliment "
                   "(product_name, product_description, barcode, nutritional_score, stores, product_category) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")

            data_aliment = (i['product_name'], i['product_description'], i['barcode'], i['nutritional_score'], i['stores'], i['product_category'])

            cursor.execute(add_aliment, data_aliment)

        my_connection.commit()

        cursor.close()
        my_connection.close()
        print("ok c'est fait")
