# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re #regex
import json
import urllib3
import pandas as pd 
import numpy as np 
from tqdm import tqdm
import requests

tqdm.pandas()

# First, find the race and classes
url = 'https://www.watersportverbond.nl/kalender/wedstrijden/zeilen' 

# setting https parser
content = requests.get(url)

# beautifulsoup extracting the tbody part
soup = BeautifulSoup(content.content, "html.parser")

print (soup)