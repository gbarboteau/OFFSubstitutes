import sys
import tkinter as tk
from tkinter import font  as tkfont

import database
from util import is_integer
from statemachine import States

class GraphicStateMachine(tk.Frame):
    def __init__(self, my_auth, master=None):
        super().__init__(master)
        self.state = ""
        self.currentCategory = ""
        self.currentProduct = ""
        self.currentSubstitute = ""
        self.currentAssociation = ""
        self.state = States.LaunchScreen
        self.master = master
        self.pack()
        # self.create_widgets()
        self.dt = database.Database(my_auth)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LaunchScreen, SearchForCategory, SearchForAliment):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_state("LaunchScreen")

    def show_state(self, state_name):
        '''Show a frame for the given page name'''
        frame = self.frames[state_name]
        frame.tkraise()

class NewScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)


class LaunchScreen(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        search_for_category_button = tk.Button(self, text="Chercher un substitut",
                            command=lambda: controller.show_state("SearchForCategory"))
        search_for_aliment_button = tk.Button(self, text="Montrer les substituts déjà enregistrés",
                            command=lambda: controller.show_state("SearchForAliment"))

        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        search_for_category_button.pack()
        search_for_aliment_button.pack()
        bye_button.pack()


class SearchForCategory(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # for category in controller.dt.all_categories:
        for category in range(0, len(controller.dt.all_categories)):
            category_button = tk.Button(self, text=controller.dt.all_categories[category],
                            command=lambda: controller.frames["SearchForAliment"].raise_screen(category))
            category_button.pack()
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("LaunchScreen"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()

    # def raise_screen(self):
    #     controller.dt.get_all_aliments_from_category(controller.currentCategory)
    #     tkraise()


class SearchForAliment(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("SearchForCategory"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()

    def raise_screen(self, category):
        print(category)
        self.controller.currentCategory = self.controller.dt.all_categories[category]
        print(self.controller.currentCategory)
        self.controller.dt.get_all_aliments_from_category(self.controller.currentCategory)
        print(self.controller.dt.all_aliments_from_category)
        for aliment in range(0, len(self.controller.dt.all_aliments_from_category)):
            aliment_button = tk.Button(self, text=self.controller.dt.all_aliments_from_category[aliment],
                            command=lambda: self.controller.show_state("SearchForSubstitute"))
            aliment_button.pack()
        self.controller.show_state("SearchForAliment")


class SearchForSubstitute(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("SearchForAliment"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()


class OnFoundSubstitute(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("SearchForSubstitute"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()


class SaveAssociation(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("OnFoundSubstitute"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()


class LookAtSubstitutes(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("LaunchScreen"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()


class LookAtOneSubstitute(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("LookAtSubstitutes"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()


class DeleteAssociation(NewScreen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        previous_screen_button = tk.Button(self, text="Retourner à l'écran précédent",
                            command=lambda: controller.show_state("LookAtOneSubstitute"))
        bye_button = tk.Button(self, text="Quitter l'application",
                            command= self.master.destroy)
        previous_screen_button.pack()
        bye_button.pack()



# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is the start page", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)

#         button1 = tk.Button(self, text="Go to Page One",
#                             command=lambda: controller.show_frame("PageOne"))
#         button2 = tk.Button(self, text="Go to Page Two",
#                             command=lambda: controller.show_frame("PageTwo"))
#         button1.pack()
#         button2.pack()



    # def create_widgets(self):
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")

    #     self.quit = tk.Button(self, text="QUIT", fg="red",
    #                           command=self.master.destroy)
    #     self.quit.pack(side="bottom")

    # def say_hi(self):
    #     print("hi there, everyone!")
