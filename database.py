import mysql.connector

from util import list_to_num_string


class Database:
    def __init__(self, my_auth):
        self.user = my_auth.user
        self.password = my_auth.password
        self.all_categories = self.find_categories()
        self.all_categories_stringed = list_to_num_string(self.all_categories)
        self.all_aliments_from_category = []
        self.all_aliments_from_category_stringed = ""
        self.this_aliment = None
        self.this_aliment_stringed = ""
        self.all_substitutes = []
        self.all_substitutes_stringed = ""
        self.this_substitute = None
        self.this_substitute_stringed = ""
        self.all_associations = self.find_associations()
        self.all_associations_stringed = ""
        self.find_associations_string()

    def find_categories(self):
        my_categories = []
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT category_name FROM category ORDER BY id")
        cursor.execute(query)
        for category_name in cursor:
            my_categories.append(category_name[0])
        cursor.close()
        my_connection.close()
        return my_categories

    def get_all_aliments_from_category(self, category):
        self.all_aliments_from_category = []
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT product_name FROM Aliment WHERE product_category = %s ORDER BY id") % ("\'" + category + "\'")
        cursor.execute(query)
        for product_name in cursor:
            self.all_aliments_from_category.append(product_name[0])
        cursor.close()
        my_connection.close()
        self.all_aliments_from_category_stringed = list_to_num_string(self.all_aliments_from_category)

    def get_aliment(self, aliment):
        self.this_aliment = ""
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT * FROM Aliment WHERE product_name = %s") % ("\'" + aliment + "\'")
        cursor.execute(query)
        for product_name in cursor:
            self.this_aliment = product_name
        cursor.close()
        my_connection.close()
        self.this_aliment_stringed = self.get_any_aliment_dict_to_string(self.this_aliment)

    def get_any_aliment_dict_to_string(self, aliment_dict):
        """Take a dictionnary containing informations for
        a specific food, then turn it into a formatted 
        string for readability purposes.
        """
        string_to_return = "Produit: {}\nCatégorie: {}\nDescription: {}\nUrl: https://fr.openfoodfacts.org/produit/{}\nNutri-score: {}\nMagasins: {}\n".format(aliment_dict[1],
            aliment_dict[6], aliment_dict[2], aliment_dict[3], aliment_dict[4], aliment_dict[5])
        return string_to_return

    def get_product_by_id(self, id_aliment):
        """Get the informations for a specific
        product by consulting the OFF database.
        """
        product_by_id = ""
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT * FROM Aliment WHERE id = %s") % ("\'" + str(id_aliment) + "\'")
        cursor.execute(query)
        for category_name in cursor:
            product_by_id = category_name
        cursor.close()
        my_connection.close()
        return product_by_id

    def get_all_substitutes(self, aliment, category, nutriscore):
        self.all_substitutes = []
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT product_name FROM Aliment WHERE product_category = %s AND STRCMP(nutritional_score, %s) < 0 ORDER BY id") % ("\'" + category + "\'", "\'" + nutriscore + "\'")
        cursor.execute(query)
        for product_name in cursor:
            self.all_substitutes.append(product_name[0])
        cursor.close()
        my_connection.close()
        self.all_substitutes_stringed = list_to_num_string(self.all_substitutes)

    def get_this_substitute(self, aliment, alimentSubstitued):
        self.this_substitute = None
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT * FROM Aliment WHERE product_name = %s") % ("\'" + aliment + "\'")
        cursor.execute(query)
        for product_name in cursor:
            self.this_substitute = product_name
        cursor.close()
        my_connection.close()
        self.this_substitute_stringed = self.get_any_aliment_dict_to_string(self.this_substitute)

    def save_association(self, aliment, alimentSubstitued):
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        add_swap = ("INSERT INTO Swap "
               "(aliment_id, substitute_id) "
               "VALUES (%s, %s)")
        data_swap = (self.this_aliment[0], self.this_substitute[0])
        cursor.execute(add_swap, data_swap)
        my_connection.commit()
        cursor.close()
        my_connection.close()

    def find_associations(self):
        my_associations = []
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("SELECT * FROM Swap ORDER BY id")
        cursor.execute(query)
        for category_name in cursor:
            my_associations.append(category_name)
        cursor.close()
        my_connection.close()
        return my_associations

    def find_associations_string(self):
        self.all_associations_stringed = ""
        for i in range(1, len(self.all_associations) +1):
            aliment_string = self.get_product_by_id(self.all_associations[i-1][1])[1]
            substitude_string = self.get_product_by_id(self.all_associations[i-1][2])[1]
            self.all_associations_stringed = self.all_associations_stringed + str(i) + ") " + aliment_string + " / " + substitude_string + "\n"

    def update_my_associations(self):
        """Update the associations list after creating
        or deleting a food association.
        """
        self.all_associations = self.find_associations()
        self.find_associations_string()

    def delete_association(self, id_row_to_delete):
        """Delete an association between two aliments."""
        my_connection = mysql.connector.connect(user=self.user, password=self.password, database='openfoodfacts')
        cursor = my_connection.cursor()
        query = ("DELETE FROM Swap WHERE id = %s") % ("\'" + str(id_row_to_delete) + "\'")
        cursor.execute(query)
        my_connection.commit()
        cursor.close()
        my_connection.close()

    