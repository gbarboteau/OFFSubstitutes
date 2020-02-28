"""Handles the user authentification
User's username and password need to match
a MySQL's already created profile
(see the README for more info)
"""
class Auth:
    def __init__(self):
        self.user = ""
        self.password = ""