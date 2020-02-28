import sys
import tkinter as tk

import terminalstate
import graphicstate
from statemachine import States


class Program:
    """Parent class of ProgramTerminal.
    Not used for now as ProgramGraphic isn't
    implemented yet.
    """
    def __init__(self, my_auth):
        """The constructor is common to ProgramTerminal
        and ProgramGraphic.
        """
        # self.dt = database.Database(my_auth)
        self.state = "LaunchScreen"
        self.sm = None


class ProgramTerminal(Program):
    """Allow to launch and use the program 
    in a terminal window.
    """
    def __init__(self, my_auth):
        super().__init__(my_auth)
        self.sm = terminalstate.TerminalStateMachine(my_auth)
        self.sm.state = ""
        self.sm.currentCategory = ""
        self.sm.currentProduct = ""
        self.sm.currentSubstitute = ""
        self.sm.currentAssociation = ""
        self.sm.state = States.LaunchScreen

    def launch(self):
        """Launch the program in a terminal window.
        Checks for inputs and current state, and changes
        what's is displayed according to these.
        """
        print("\n")
        user_input = ""
        while 1:
            if self.sm.state == States.LaunchScreen:
                self.sm.state_launchscreen()
            if self.sm.state == States.SearchForCategory:
                self.sm.state_searchforcategory()
            if self.sm.state == States.SearchForAliment:
                self.sm.state_searchforaliment()
            if self.sm.state == States.SearchForSubstitute:
                self.sm.state_searchforsubstitute()
            if self.sm.state == States.OnFoundSubstitute:
                self.sm.state_onfoundsubstitute()
            if self.sm.state == States.SaveAssociation:
                self.sm.state_saveassociation()
            if self.sm.state == States.LookAtSubstitutes:
                self.sm.state_lookatsubstitutes()
            if self.sm.state == States.LookAtOneSubstitute:
                self.sm.state_lookatonesubstitute()
            if self.sm.state == States.DeleteAssociation:
                self.sm.state_deleteassociation()
            if self.sm.state == States.Bye:
                self.sm.state_bye()
