"""Handle the different state of the program
when it's launched in terminal mode.
"""
import sys

import database
from util import is_integer
from statemachine import States


class TerminalStateMachine:
    """Create an instance of a state machine
    handling states in terminal mode.
    """
    def __init__(self, my_auth):
        """Initialize the instance.
        The strings are what is shown in terminal,
        we update them as we change states.
        """
        self.dt = database.Database(my_auth)
        self.state = ""
        self.currentCategory = ""
        self.currentProduct = ""
        self.currentSubstitute = ""
        self.currentAssociation = ""
        self.state = States.LaunchScreen

    def state_launchscreen(self):
        """The menu screen. Appears when the
        program is launched or when you get back
        to it.
        """
        print("Bienvenue sur OpenFoodSubstitute ! Cherchez-vous un aliment à substituer, ou un substitut déjà enregistré ?\n")
        user_input = input("Appuyez sur:\n1: Chercher un substitut\n2: Un aliment déjà enregistré\n3 : Quitter le programme\nVous pouvez quitter le programme à tout moment en entrant Q\n")
        if user_input.lower() == "1":
            self.state = States.SearchForCategory
        elif user_input.lower() == "2":
            self.state = States.LookAtSubstitutes
        if user_input.lower() == "3" or user_input.lower() == "q":
            self.state = States.Bye

    def state_searchforcategory(self):
        """Show the screen allowing the user
        to choose a category of food.
        """
        print("Voici les substituts mis à votre disposition:\n")
        print (self.dt.all_categories_stringed)
        user_input = input("Entrez le chiffre correspondant à la catégorie désirée, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")
        if is_integer(user_input):
            if 1 <= int(user_input) <= len(self.dt.all_categories) +1:
                self.currentCategory = self.dt.all_categories[int(user_input) - 1]
                self.state = States.SearchForAliment
            else:
                print("Nombre invalide ! Réessayez\n")
        else:
            if user_input.lower() == "q":
                self.state = States.Bye
            elif user_input.lower() == "r":
                self.state = States.LaunchScreen
            else:
                print("Commande invalide, réessayez!\n")

    def state_searchforaliment(self):
        """Show the screen allowing the user
        to choose a food from a category.
        """
        self.dt.get_all_aliments_from_category(self.currentCategory)
        print("Bienvenue dans la catégorie " + self.currentCategory + "\n")
        print(self.dt.all_aliments_from_category_stringed)
        user_input = input("Entrez le chiffre correspondant au produit désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")
        if is_integer(user_input):
            if 1 <= int(user_input) <= len(self.dt.all_aliments_from_category) +1:
                self.currentProduct = self.dt.all_aliments_from_category[int(user_input) - 1]
                self.state = States.SearchForSubstitute
            else:
                print("Nombre invalide ! Réessayez\n")
        else:
            if user_input.lower() == "q":
                self.state = States.Bye
            elif user_input.lower() == "r":
                self.state = States.SearchForCategory
            else:
                print("Commande invalide, réessayez!\n")

    def state_searchforsubstitute(self):
        """Show the screen allowing the user
        to choose a substitute for a specific
        food.
        """
        self.dt.get_aliment(self.currentProduct)
        print(self.dt.this_aliment_stringed + "\n\n")
        self.dt.get_all_substitutes(self.currentProduct, self.currentCategory, self.dt.this_aliment[4])
        print(self.dt.all_substitutes_stringed)
        user_input = input("Entrez le chiffre correspondant au substitut désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")
        if is_integer(user_input):
            if 1 <= int(user_input) <= len(self.dt.all_substitutes) +1:
                self.currentSubstitute = self.dt.all_substitutes[int(user_input) - 1]
                self.state = States.OnFoundSubstitute
            else:
                print("Nombre invalide ! Réessayez\n")
        else:
            if user_input.lower() == "q":
                self.state = States.Bye
            elif user_input.lower() == "r":
                self.state = States.SearchForAliment
            else:
                print("Commande invalide, réessayez!\n")


    def state_onfoundsubstitute(self):
        """Show the screen allowing the user
        to examine a substitute for a specific
        food, then save it.
        """
        print("C'est gagné ! Aliment : " + self.currentSubstitute)
        self.dt.get_this_substitute(self.currentSubstitute, self.currentProduct)
        print(self.dt.this_substitute_stringed + "\n")
        user_input = input("Entrez S pour sauvegarder cette association, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")

        if user_input.lower() == "q":
            self.state = States.Bye
        elif user_input.lower() == "r":
            self.state = States.SearchForSubstitute
        elif user_input.lower() == "s":
            self.state = States.SaveAssociation
        else:
            print("Commande invalide, réessayez!\n")


    def state_saveassociation(self):
        """Show the screen indicating a substitute
        for a specific food has been saved.
        """
        self.dt.save_association(self.currentSubstitute, self.currentProduct)
        print("\nAssociation sauvegardée ! Vous pouvez la consulter depuis le menu principal.\n")
        user_input = input("Entrez M pour retourner au menu principal, R pour retourner à l'écran des substituts disponibles, ou Q pour quitter le programme\n")

        if user_input.lower() == "q":
            self.state = States.Bye
        elif user_input.lower() == "r":
            self.state = States.SearchForSubstitute
        elif user_input.lower() == "m":
            self.state = States.LaunchScreen
        else:
            print("Commande invalide, réessayez!\n")

    def state_lookatsubstitutes(self):
        """Show the screen listing every
        combination of food/substitute
        previously registered.
        """
        self.dt.update_my_associations()
        print(self.dt.all_associations_stringed)
        user_input = input("Entrez le chiffre correspondant au substitut désiré, R pour retourner à l'écran précédent, ou Q pour quitter le programme\n")
        if is_integer(user_input):
            if 1 <= int(user_input) <= len(self.dt.all_associations) +1:
                self.currentAssociation = self.dt.all_associations[int(user_input) - 1]
                self.state = States.LookAtOneSubstitute
            else:
                print("Nombre invalide ! Réessayez\n")
        else:
            if user_input.lower() == "q":
                self.state = States.Bye
            elif user_input.lower() == "r":
                self.state = States.LaunchScreen
            else:
                print("Commande invalide, réessayez!\n")

    def state_lookatonesubstitute(self):
        """Show the screen of a specific
        food/substitue combination, and allow
        the user to delete it.
        """
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
            self.state = States.Bye
        elif user_input.lower() == "r":
            self.state = States.LookAtSubstitutes
        elif user_input.lower() == "s":
            self.state = States.DeleteAssociation
        else:
            print("Commande invalide, réessayez!\n")

    def state_deleteassociation(self):
        """Confirm the suppression of a former
        food/substitute association.
        """
        self.dt.delete_association(self.currentAssociation[0])
        print("Voilà qui est fait !\n")

        user_input = input("Entrez R pour retourner à l'écran des substituts, M pour le menu principal, ou Q pour quitter le programme\n")

        if user_input.lower() == "q":
            self.state = States.Bye
        elif user_input.lower() == "r":
            self.state = States.LookAtSubstitutes
        elif user_input.lower() == "m":
            self.state = States.LaunchScreen
        else:
            print("Commande invalide, réessayez!\n")

    def state_bye(self):
        """Quit the program"""
        sys.exit()
