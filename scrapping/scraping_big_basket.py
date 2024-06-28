import os 
import json

import pymongo.mongo_client 
import config 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from bs4 import BeautifulSoup 
import pymongo 
from time import sleep 


class scrape_e_commerce:

    def __init__(self):
        # driver initialization 
        chromeoption = webdriver.ChromeOptions()
        self.driver= webdriver.Chrome(options= chromeoption)

        #mongodb initialization 
        conn = pymongo.MongoClient(config.db_connection_link )
        db = conn [ config.db_name]
        coll = db [ config.collection_name]

    def get_all_category(self):
        self.driver .get(config.url)
        sleep(2)
        self.driver.find_element(By.XPATH,config.filter_xpath).click()
        sleep(1)
        



obj = scrape_e_commerce()
obj.get_all_category()
# href="/cl/fruits-vegetables/?nc=nb"