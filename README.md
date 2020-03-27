Open Food Facts Substitutes

*1 - Create the database*

In MySQL, create database name "openfoodfacts". Create a user for this database (give them the username and the password you want).
Then, launch the DatabaseFiller/create_database.sql script.

CREATE DATABASE openfoodfacts;
USE openfoodfacts;
SOURCE Documents/OFFSubstitutes/DatabaseFiller/create_database.sql;


*2 - Fill the database*

Launch the python script DatabaseFiller/databasefiller.py. Add the username of the MySQL account you'll use (password will be asked later).

python DatabaseFiller/databasefiller.py user


*3 - Use the software*

Launch the main.py script. You need to add the argument -t or -g (to use the program with a text or a graphic interface), and the username of the MySQL account you'll use (password will be asked later).

python main.py -t user