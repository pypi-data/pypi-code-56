from termcolor import colored
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import os
import json
import random
import string
import re


from utils import welcome

load_dotenv(dotenv_path='.env')

                
if __name__ == "__main__":
    welcome()
