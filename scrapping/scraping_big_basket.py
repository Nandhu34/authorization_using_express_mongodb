import os 
import json

import pymongo.mongo_client 
import config 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup 
import pymongo 
from time import sleep 


class scrape_e_commerce:

    def __init__(self):
        # driver initialization 
        chromeoption = webdriver.ChromeOptions()
        self.driver= webdriver.Chrome(options= chromeoption)
        self.hover = ActionChains(self.driver)

        #mongodb initialization 
        conn = pymongo.MongoClient(config.db_connection_link )
        db = conn [ config.db_name]
        coll = db [ config.collection_name]
        # variables to store 
        self.total_product_links =set()

    def get_all_category(self):
        self.driver .get(config.url)
        sleep(2)
        self.driver.find_element(By.XPATH,config.filter_xpath).click()
        sleep(1)
        catogorie = self.driver.find_elements(By.XPATH,config.category_x_path)
        total_categorie_count = len(catogorie)
        total_categorie_count = int(total_categorie_count /2 )
       
        for each_category in range(15,total_categorie_count*2):
            xpath_to_locate = '('+config.category_x_path +')['+str(each_category)+']'
            # print(xpath_to_locate)
            self.hover.move_to_element(catogorie[each_category])
            self.hover.perform()
           
            sub_catogorie = self.driver.find_elements(By.XPATH , config.xpath_for_sub_category)
            for catog in sub_catogorie:
                self.hover.move_to_element(catog)
                self.hover.perform()
                product_links = self.driver.find_elements(By.XPATH,config.xpath_for_product)
                for product in product_links: 
                    # self.hover.move_to_element(product )
                    # self.hover.perform()
                    # print(product )
                    
                    link = product.get_attribute('href')
                    # print(link)
                    self.total_product_links.add(link)

                    sleep(1 )

                








obj = scrape_e_commerce()
obj.get_all_category()
print(obj.total_product_links)
# href="/cl/fruits-vegetables/?nc=nb"