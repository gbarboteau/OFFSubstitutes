SET NAMES utf8mb4;

DROP TABLE IF EXISTS Swap;
DROP TABLE IF EXISTS Aliment;
DROP TABLE IF EXISTS Category;

CREATE TABLE Category(
    id int unsigned NOT NULL AUTO_INCREMENT,
    category_name varchar(100) NOT NULL,
    category_url varchar(200) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY category_name (category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Aliment (
    id int unsigned NOT NULL AUTO_INCREMENT,
    product_name varchar(100) NOT NULL,
    product_description text,
    barcode varchar(20) NOT NULL,
    nutritional_score char(1) NOT NULL,
    stores varchar(200),
    product_category varchar(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_name (product_name),
    CONSTRAINT fk_product_category FOREIGN KEY (product_category) REFERENCES Category(category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Swap(
    id int unsigned NOT NULL AUTO_INCREMENT,
    aliment_id int unsigned NOT NULL,
    substitute_id int unsigned NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_aliment_id FOREIGN KEY (aliment_id) REFERENCES Aliment(id),
    CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id) REFERENCES Aliment(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO Category(category_name, category_url) VALUES
("Compotes", "https://fr.openfoodfacts.org/categorie/compotes"),
("Bonbons de chocolat", "https://fr.openfoodfacts.org/categorie/bonbons-de-chocolat"),
("Sodas", "https://fr.openfoodfacts.org/categorie/sodas"),
("Barres", "https://fr.openfoodfacts.org/categorie/barres"),
("Yaourts aux fruits", "https://fr.openfoodfacts.org/categorie/yaourts-aux-fruits"),
("Produits de la mer", "https://fr.openfoodfacts.org/categorie/produits-de-la-mer"),
("Produits a la viande", "https://fr.openfoodfacts.org/categorie/produits-a-la-viande"),
("Produits deshydrates", "https://fr.openfoodfacts.org/categorie/produits-deshydrates"),
("Jambons", "https://fr.openfoodfacts.org/categorie/jambons"),
("Cereales pour petit-dejeuner", "https://fr.openfoodfacts.org/categorie/cereales-pour-petit-dejeuner");