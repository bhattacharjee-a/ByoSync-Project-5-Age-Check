# Welcome.py

import cv2
'''from .project_log import logger
from . import constants
from .model import Model
from .User_interface import User'''

from project_log import logger
from model import Model
from User_interface import User
import constants

class User_IF:


    @staticmethod
    def greet():
        print("**********************************************************")
        print("************* AGE CHECK WITH BOOLEAN PRIVACY *************")
        print("**********************************************************")

    @staticmethod
    def welcome_menu ():

        attempt = 0
        while attempt<constants.MAX_ATTEMPTS:

            ans = input("Choose An Option.\n1. Upload Image for Verification\n2. Exit:\n\nEnter choice:")

            if ans == "1":
                User.menu()
                return            

            elif ans == "2":
                break

            else: 
                logger.warning("Invalid Input! Try again.\n")

            attempt += 1
        return

    

    @staticmethod
    def farewell():
        
        print("**********************************************************")
        print("******* Thank You For Using AGE CHECK WITH BOOLEAN *******")
        print("**********************************************************")

