import os 
import json

import pymongo.mongo_client 
import config 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup 
import pymongo 


class scrape_e_commerce:

    def __init__(self):
        # driver initialization 
        chromeoption = webdriver.ChromeOptions()
        self.driver= webdriver.Chrome(options= chromeoption)

        #mongodb initialization 
        conn = pymongo.mongo_client(config.db_connection_link )
        db = conn [ config.db_name]
        coll = db [ config.collection_name]

    def get_all_category


obj = scrape_e_commerce()
