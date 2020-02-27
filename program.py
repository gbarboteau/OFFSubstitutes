import database
from util import is_integer

class Program:
    def __init__(self, my_auth):
        self.dt = database.Database(my_auth)
        self.state = "LaunchScreen"
        self.currentCategory = ""
        self.currentProduct = ""
        self.currentSubstitute = ""
        self.currentAssociation = ""

class ProgramTerminal(Program):

    def launch(self):
        print("\n")

        user_input = ""

        while user_input.lower() != "q":
            """
            """
            if self.state == "LaunchScreen":
                """Quand le programme démarre ou qu'on retourne
                à l'écran d'accueil
                """
                print("Bienvenue sur OpenFoodSubstitute ! Cherchez-vous un aliment à substituer, ou un substitut déjà enregistré ?\n")
                user_input = input("Appuyez sur:\n1: Chercher un substitut\n2: Un aliment déjà enregistré\n3 : Quitter le programme\nVous pouvez quitter le programme à tout moment en entrant Q\n")
                if user_input.lower() == "1":
                    self.state = "SearchForCategory"
                elif user_input.lower() == "2":
                    self.state = "LookAtSubstitutes"
                if user_input.lower() == "3" or user_input.lower() == "q":
                    self.state = "Bye"

                

            if self.state == "SearchForCategory":
                """Le programme du choix de la 
                catégorie dans laquelle chercher l'aliment
                """
                print("Voici les substituts mis à votre disposition:\n")
                print (self.dt.all_categories_stringed)
                user_input = input("Entrez le chiffre correspondant à la catégorie désirée, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

                if is_integer(user_input):
                    if 1 <= int(user_input) <= len(self.dt.all_categories) +1:
                        self.currentCategory = self.dt.all_categories[int(user_input) - 1]
                        self.state = "SearchForAliment"
                    else:
                        print("Nombre invalide ! Réessayez\n")
                else:
                    if user_input.lower() == "q":
                        self.state = "Bye"
                    elif user_input.lower() == "r":
                        self.state = "LaunchScreen"
                    else:
                        print("Commande invalide, réessayez!\n")

            if self.state == "SearchForAliment":
                """Le programme du choix de l'aliment
                """
                self.dt.get_all_aliments_from_category(self.currentCategory)
                print("Bienvenue dans la catégorie " + self.currentCategory + "\n")
                print(self.dt.all_aliments_from_category_stringed)
                user_input = input("Entrez le chiffre correspondant au produit désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

                if is_integer(user_input):
                    if 1 <= int(user_input) <= len(self.dt.all_aliments_from_category) +1:
                        self.currentProduct = self.dt.all_aliments_from_category[int(user_input) - 1]
                        self.state = "SearchForSubstitute"
                    else:
                        print("Nombre invalide ! Réessayez\n")
                else:
                    if user_input.lower() == "q":
                        self.state = "Bye"
                    elif user_input.lower() == "r":
                        self.state = "SearchForCategory"
                    else:
                        print("Commande invalide, réessayez!\n")



            if self.state == "SearchForSubstitute":
                """Le programme qui affiche l'aliment
                et ses substituts
                """
                self.dt.get_aliment(self.currentProduct)
                print(self.dt.this_aliment_stringed + "\n\n")

                self.dt.get_all_substitutes(self.currentProduct, self.currentCategory, self.dt.this_aliment[4])
                print(self.dt.all_substitutes_stringed)
                user_input = input("Entrez le chiffre correspondant au substitut désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

                if is_integer(user_input):
                    if 1 <= int(user_input) <= len(self.dt.all_substitutes) +1:
                        self.currentSubstitute = self.dt.all_substitutes[int(user_input) - 1]
                        self.state = "OnFoundSubstitute"
                    else:
                        print("Nombre invalide ! Réessayez\n")
                else:
                    if user_input.lower() == "q":
                        self.state = "Bye"
                    elif user_input.lower() == "r":
                        self.state = "SearchForAliment"
                    else:
                        print("Commande invalide, réessayez!\n")



            if self.state == "OnFoundSubstitute":
                print("C'est gagné ! Aliment : " + self.currentSubstitute)
                self.dt.get_this_substitute(self.currentSubstitute, self.currentProduct)
                print(self.dt.this_substitute_stringed + "\n")
                user_input = input("Entrez S pour sauvegarder cette association, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

                if user_input.lower() == "q":
                    self.state = "Bye"
                elif user_input.lower() == "r":
                    self.state = "SearchForSubstitute"
                elif user_input.lower() == "s":
                    self.state = "SaveAssociation"
                else:
                    print("Commande invalide, réessayez!\n")


            if self.state == "SaveAssociation":
                self.dt.save_association(self.currentSubstitute, self.currentProduct)
                print("\nAssociation sauvegardée ! Vous pouvez la consulter depuis le menu principal.\n")
                user_input = input("Entrez M pour retourner au menu principal, R pour retourner à l'écran des substituts disponibles, ou Q pour quitter le programme\n")

                if user_input.lower() == "q":
                    self.state = "Bye"
                elif user_input.lower() == "r":
                    self.state = "SearchForSubstitute"
                elif user_input.lower() == "m":
                    self.state = "LaunchScreen"
                else:
                    print("Commande invalide, réessayez!\n")


            if self.state == "LookAtSubstitutes":
                self.dt.update_my_associations()
                print(self.dt.all_associations_stringed)
                user_input = input("Entrez le chiffre correspondant au substitut désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

                if is_integer(user_input):
                    if 1 <= int(user_input) <= len(self.dt.all_associations) +1:
                        self.currentAssociation = self.dt.all_associations[int(user_input) - 1]
                        self.state = "LookAtOneSubstitute"
                    else:
                        print("Nombre invalide ! Réessayez\n")
                else:
                    if user_input.lower() == "q":
                        self.state = "Bye"
                    elif user_input.lower() == "r":
                        self.state = "LaunchScreen"
                    else:
                        print("Commande invalide, réessayez!\n")


            if self.state == "LookAtOneSubstitute":
                alim1 = self.dt.get_product_by_id(self.currentAssociation[1])
                alim2 = self.dt.get_product_by_id(self.currentAssociation[2])
                alim1_stringed = self.dt.get_any_aliment_dict_to_string(alim1)
                alim2_stringed = self.dt.get_any_aliment_dict_to_string(alim2)
                print("L'aliment à substituer est:\n")
                print(alim1_stringed)
                print("Nous vous proposons à la place :\n")
                print(alim2_stringed)
                user_input = input("Entrez R pour retourner à l'écran précédent, S pour supprimer l'association, ou Q pour quitter le programme\n")

                if user_input.lower() == "q":
                    self.state = "Bye"
                elif user_input.lower() == "r":
                    self.state = "LookAtSubstitutes"
                elif user_input.lower() == "s":
                    self.state = "DeleteAssociation"
                else:
                    print("Commande invalide, réessayez!\n")


            if self.state == "DeleteAssociation":
                self.dt.delete_association(self.currentAssociation[0])
                print("Voilà qui est fait !\n")

                user_input = input("Entrez R pour retourner à l'écran des substituts, M pour le menu principal, ou Q pour quitter le programme\n")

                if user_input.lower() == "q":
                    self.state = "Bye"
                elif user_input.lower() == "r":
                    self.state = "LookAtSubstitutes"
                elif user_input.lower() == "m":
                    self.state = "LaunchScreen"
                else:
                    print("Commande invalide, réessayez!\n")


            if self.state == "Bye":
                pass