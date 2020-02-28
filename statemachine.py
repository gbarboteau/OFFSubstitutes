from enum import Enum

class States(Enum):
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