"""A state machine with every different state
of the program. 
"""
from enum import Enum


class States(Enum):
    """An enumeration of every possible state."""
    LaunchScreen = "LaunchScreen"
    SearchForCategory = "SearchForCategory"
    SearchForAliment = "SearchForAliment"
    SearchForSubstitute = "SearchForSubstitute"
    OnFoundSubstitute = "OnFoundSubstitute"
    SaveAssociation = "SaveAssociation"
    LookAtSubstitutes = "LookAtSubstitutes"
    LookAtOneSubstitute = "LookAtOneSubstitute"
    DeleteAssociation = "DeleteAssociation"
    Bye = "Bye"
    