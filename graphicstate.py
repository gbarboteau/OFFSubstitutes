import sys
import tkinter as tk
from tkinter import font  as tkfont

import database
from util import is_integer
from statemachine import States


class GraphicStateMachine(tk.Frame):
    def __init__(self, my_auth, master=None):
        super().__init__(master)
        self.state = None
        self.currentCategory = ""
        self.currentProduct = ""
        self.currentSubstitute = ""
        self.currentAssociation = ""
        self.state = States.LaunchScreen
        self.master = master
        self.pack()
        self.dt = database.Database(my_auth)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.normal_font = tkfont.Font(family='Helvetica', size=12, weight="bold")

        self.container = tk.Frame(self, width=720, height=400)
        self.container.pack(side="top", fill="both", expand=True)


        self.frame = NewScreen(parent=self.container, controller=self)

        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.tkraise()
        self.widgetList = []

        self.state_launchscreen()

    def change_state(self, state_name):
        self.state = state_name
        print(self.state)
        for widget in self.widgetList:
            widget.destroy()
        self.widgetList = []
        if self.state == States.LaunchScreen:
            self.state_launchscreen()
        if self.state == States.SearchForCategory:
            self.state_searchforcategory()
        if self.state == States.SearchForAliment:
            self.state_searchforaliment()
        if self.state == States.SearchForSubstitute:
            self.state_searchforsubstitute()
        if self.state == States.OnFoundSubstitute:
            self.state_onfoundsubstitute()
        if self.state == States.SaveAssociation:
            self.state_saveassociation()
        if self.state == States.LookAtSubstitutes:
            self.state_lookatsubstitutes()
        if self.state == States.LookAtOneSubstitute:
            self.state_lookatonesubstitute()
        if self.state == States.DeleteAssociation:
            self.state_deleteassociation()
        if self.state == States.Bye:
            self.state_bye()

    def state_launchscreen(self):
        # for widget in self.widgetList:
        #     widget.destroy()
        search_for_category_button = tk.Button(self, text="Chercher un substitut",
                            command=lambda: self.change_state(States.SearchForCategory))
        search_for_aliment_button = tk.Button(self, text="Montrer les substituts déjà enregistrés",
                            command=lambda: self.change_state(States.LookAtSubstitutes))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        search_for_category_button.pack()
        search_for_aliment_button.pack()
        bye_button.pack()
        self.widgetList.extend([search_for_category_button, search_for_aliment_button, bye_button])

    def state_searchforcategory(self):
        # for widget in self.widgetList:
        #     widget.destroy()
        for category in range(0, len(self.dt.all_categories)):
            category_button = tk.Button(self, text=self.dt.all_categories[category],
                            command=lambda category=category : self.change_currentcategory(category, States.SearchForAliment))
            category_button.pack()
            self.widgetList.append(category_button)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: self.change_state(States.LaunchScreen))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([previous_screen_button, bye_button])

    def change_currentcategory(self, category, state_name):
        print(category)
        self.currentCategory = self.dt.all_categories[category]
        self.change_state(state_name)

    def state_searchforaliment(self):
        self.dt.get_all_aliments_from_category(self.currentCategory)
        for aliment in range(0, len(self.dt.all_aliments_from_category)):
            aliment_button = tk.Button(self, text=self.dt.all_aliments_from_category[aliment],
                            command=lambda aliment=aliment: self.change_currentproduct(aliment, States.SearchForSubstitute))
            aliment_button.pack()
            self.widgetList.append(aliment_button)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: self.change_state(States.SearchForCategory))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([previous_screen_button, bye_button])

    def change_currentproduct(self, product, state_name):
        print(product)
        self.currentProduct = self.dt.all_aliments_from_category[product]
        self.change_state(state_name)

    def state_searchforsubstitute(self):
        self.dt.get_aliment(self.currentProduct)
        self.dt.get_all_substitutes(self.currentProduct, self.currentCategory, self.dt.this_aliment[4])

        for substitute in range(0, len(self.dt.all_substitutes)):
            substitute_button = tk.Button(self, text=self.dt.all_substitutes[substitute],
                            command=lambda substitute=substitute: self.change_currentsubstitute(substitute, States.OnFoundSubstitute))
            substitute_button.pack()
            self.widgetList.append(substitute_button)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: self.change_state(States.SearchForAliment))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([previous_screen_button, bye_button])

    def change_currentsubstitute(self, substitute, state_name):
        print(substitute)
        self.currentSubstitute = self.dt.all_substitutes[substitute]
        self.change_state(state_name)

    def state_onfoundsubstitute(self):
        self.dt.get_this_substitute(self.currentSubstitute, self.currentProduct)
        label_text = (self.dt.this_substitute_stringed + "\n")
        label = tk.Label(self, text=label_text, font=self.normal_font)
        label.pack(side="top", fill="x", pady=10)

        save_association_button = tk.Button(self, text="Sauvegarder l'association",
                            command=lambda: self.change_state(States.SaveAssociation))
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: self.change_state(States.SearchForSubstitute))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        save_association_button.pack()
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([label, save_association_button, previous_screen_button, bye_button])

    def state_saveassociation(self):
        self.dt.save_association(self.currentSubstitute, self.currentProduct)

        label_text = ("Association sauvegardée, merci beaucoup !")
        label = tk.Label(self, text=label_text, font=self.normal_font)
        label.pack(side="top", fill="x", pady=10)

        launch_screen_button = tk.Button(self, text="Retourner au menu principal",
                            command=lambda: self.change_state(States.LaunchScreen))
        previous_screen_button = tk.Button(self, text="Retourner à l'écran des substituts",
                            command=lambda: self.change_state(States.SearchForSubstitute))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        launch_screen_button.pack()
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([label, launch_screen_button, previous_screen_button, bye_button])

    def state_lookatsubstitutes(self):
        self.dt.update_my_associations()
        for association in range(0, len(self.dt.all_associations)):
            association_button = tk.Button(self, text=self.dt.all_associations_list_stringed[association],
                            command=lambda association=association : self.change_currentassociation(association, States.LookAtOneSubstitute))
            association_button.pack()
            self.widgetList.append(association_button)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: self.change_state(States.LaunchScreen))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([previous_screen_button, bye_button])

    def change_currentassociation(self, association, state_name):
        print(association)
        self.currentAssociation = self.dt.all_associations[association]
        self.change_state(state_name)

    def state_lookatonesubstitute(self):
        alim1 = self.dt.get_product_by_id(self.currentAssociation[1])
        alim2 = self.dt.get_product_by_id(self.currentAssociation[2])
        alim1_stringed = self.dt.get_any_aliment_dict_to_string(alim1)
        alim2_stringed = self.dt.get_any_aliment_dict_to_string(alim2)

        label_1 = tk.Label(self, text=alim1_stringed, font=self.normal_font)
        label_1.pack(side="top", fill="x", pady=10)

        label_2 = tk.Label(self, text=alim2_stringed, font=self.normal_font)
        label_2.pack(side="top", fill="x", pady=10)

        delete_association_button = tk.Button(self, text="Supprimer l'association",
                            command=lambda: self.change_state(States.DeleteAssociation))
        previous_screen_button = tk.Button(self, text="Retourner à l'écran des substituts",
                            command=lambda: self.change_state(States.SearchForSubstitute))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        delete_association_button.pack()
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([label_1, label_2, delete_association_button, previous_screen_button, bye_button])

    def state_deleteassociation(self):
        self.dt.delete_association(self.currentAssociation[0])
        label_text = ("Association supprimée, merci beaucoup !")
        label = tk.Label(self, text=label_text, font=self.normal_font)
        label.pack(side="top", fill="x", pady=10)

        launch_screen_button = tk.Button(self, text="Retourner au menu principal",
                            command=lambda: self.change_state(States.LaunchScreen))
        previous_screen_button = tk.Button(self, text="Retourner à l'écran des substituts",
                            command=lambda: self.change_state(States.LookAtSubstitutes))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        launch_screen_button.pack()
        previous_screen_button.pack()
        bye_button.pack()
        self.widgetList.extend([label, launch_screen_button, previous_screen_button, bye_button])

    def state_bye(self):
        self.master.destroy()


class NewScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
