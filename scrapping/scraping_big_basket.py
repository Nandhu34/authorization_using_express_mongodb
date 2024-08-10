import os 
import json

import pymongo.mongo_client 
import config 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from bs4 import BeautifulSoup 
import pymongo 
from time import sleep 
import requests

class scrape_e_commerce:

    def __init__(self):
        # driver initialization 
        chromeoption = webdriver.ChromeOptions()
        # chromeoption.add_argument('--headless')
        # chromeoption.add_argument('--headless')
        chromeoption.add_argument('--disable-gpu')
        chromeoption.add_argument('--window-size=1920,1080')  # Simulate a typical screen size
        chromeoption.add_argument('--user-agent=Your Custom User-Agent String')
        self.driver= webdriver.Chrome(options= chromeoption)
        self.hover = ActionChains(self.driver)

        #mongodb initialization 
        conn = pymongo.MongoClient(config.db_connection_link )
        db = conn [ config.db_name]
        self.coll = db [ config.product_details_collection]
        self.total_main_link = db [config.main_link_collection]
        self.specific_link_collection = db [config.specific_product_link]
        self.final_specific_links = db [config.final_specific_links ]
        self.product_details = db[config.product_details]
        
        # variables to store 
        self.total_product_links =set()
        self.total_specific_links = set()

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

                



    def get_product_collect_data(self,data ):

        for each_data in data :
            try :
                self.infinite_scroll_get_page_source(each_data)
            except Exception as e:
                print(e)
    
    def infinite_scroll_get_page_source(self,page_link ):

        self.driver.get(page_link)
        sleep(2)
        length = 100 
        while True :
                length = length + 500
                self.driver.execute_script(f"window.scrollBy(0,{length});")
                sleep(3)
                actual_height = self.driver.execute_script(f"return document.body.scrollHeight")
                print(" actual height ,  full page height ")

                try :
                    print(" try block ")
                    check_footer = self.driver.find_element(By.XPATH,config.xpath_for_footer).is_displayed()
                    # print(check_footer)
                    if check_footer:
                        break 
                except :
                    print(" footer not found ")
    
    def find_links_by_link_modifying(self,page_link):

        for i in range(0,100):
            restriuctured_link = page_link + '&page='+str(i)
            print()

            sleep(2)
            # print(restriuctured_link)
            self.driver.get(restriuctured_link)
            # print(self.driver.page_source)
            try:
                check_something_wrong =     self.driver.find_element(By.XPATH,config.xpath_for_wrong_api).is_displayed()
                if check_something_wrong :
                    print( " wrong api achieved -----  exiting ")
                    break 
            except : 
                print("Data  GOT  Successfully  ")
                soup = BeautifulSoup(self.driver.page_source,'html.parser')
                # print(soup)
                # founded = soup.find_all(class_='PaginateItems___StyledLi-sc-1yrbjdr-0')
                # print(founded)
                sleep(1)
                a_tags = soup.select('.PaginateItems___StyledLi-sc-1yrbjdr-0.dDBqny a')

                # Print href and text for each <a> tag found
                for a_tag in a_tags:
                    link = a_tag['href']
                    print(link)
                    
                    self.total_specific_links.add(link)
                    check_presence = self.specific_link_collection.count_documents({"specific_prodict_links":link})
                    if check_presence == 0 :
                        
                        self.specific_link_collection.insert_one({"main_link":page_link,"pagination_link":restriuctured_link,"specific_prodict_links":link,"processed":False})
                    else:
                        print()
                        print(" present in db")
                        
    def collect_complete_data_from_link(self, specific_link_document):
        print(specific_link_document)
        data ={}
        main_link = specific_link_document['main_link']
        product_link = specific_link_document['specific_prodict_links']

        full_product_link = 'https://bigbasket.com'+product_link
        # full_product_link ='https://www.bigbasket.com/pd/10000273/fresho-mushrooms-button-1-pack/?nc=l2category&t_pos_sec=1&t_pos_item=2&t_s=Mushrooms+-+Button'
        # full_product_link = 'https://www.bigbasket.com/pd/10000273/fresho-mushrooms-button-1-pack/?nc=l2category&t_pos_sec=1&t_pos_item=2&t_s=Mushrooms+-+Button'
        self.driver.get(full_product_link)
        soup = BeautifulSoup(self.driver.page_source,'html.parser')

        category_details = soup.find(attrs={'class': "Breadcrumb___StyledDiv-sc-1jdzjpl-0 hlQOJm"}).text.split('/')

        main_category = category_details[1]

        sub_category = category_details[2]

        sub_sub_category = category_details[3]

        data ['category'] = main_category
        data['sub_category']=sub_category
        data['inner_category']= sub_sub_category

        print("main_cat:",main_category,"sub cat :",sub_category,"sub sub cat:",sub_sub_category)

        brand_name = soup.find(attrs={'class':'Description___StyledLink-sc-82a36a-1 gePjxR'}).text.strip()
        data['brand_name']=brand_name

        print("brand name :", brand_name)

        title_name = soup.find(attrs={'class':'Description___StyledH-sc-82a36a-2 bofYPK'}).text.strip()
        data['title_name']=title_name
        print("title name :",title_name)
        try:
            mrp_price_array  = soup.find(attrs={'class':'flex items-center mb-1 text-md text-darkOnyx-100 leading-md p-0'})
        

            mrp_price_array = mrp_price_array.find_all('td')[1].text.strip()
            data['mrp_price']=mrp_price_array
            print("mrp price :",mrp_price_array)
        except Exception as e:
            print(e)
            data['mrp_price']=""
        snapshot_list = soup.find(attrs={'class','thumbnail lg:h-94 xl:h-110.5 lg:w-17 xl:w-21'})
        # print(snapshot_list)
        image_links =[]
        if snapshot_list:
            img_tags = snapshot_list.find_all('img')
            # for img in img_tags:
            #     if 'src' in img.attrs:
            #         print(img['src'])
            #         sleep(3)
            image_links = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'].startswith('http')]

        data ['image_links'] = image_links
        # print(mrp_price_array.td)
        # for mrp_price in mrp_price_array:

        #     print(mrp_price.text)
        data['link'] = self.driver.current_url
        data['date_of_generation']= datetime.datetime.now()
        try :
            actual_price = soup.find(attrs={'class':'Description___StyledTd-sc-82a36a-4 fLZywG'}).text.replace('Price: ','')
            data['actual_price']=actual_price
            print("actual price : ",actual_price)
            data['out_of_stock']=False
        except :
            data['actual_price']=""
            data['out_of_stock']=True 
            return self.update_data_in_db(data,product_link)
             

        bracet_Content_near_mrp = soup.find(attrs={'class':'ml-1 text-darkOnyx-400 leading-md text-md p-0'}).text
        data['bracet_near_mrp']=bracet_Content_near_mrp

        print("bracet in mrp :",bracet_Content_near_mrp)
        try:
            percentage_price_drop = soup.find(attrs={'class':'flex items-center text-md text-appleGreen-700 font-semibold mb-1 leading-md p-0'})

            percentage_price_drop = percentage_price_drop.find_all('td')[1].text.strip()
            data['price_drop'] = percentage_price_drop
            print("percentage of price drop :",percentage_price_drop)
        except :
                data['price_drop'] = percentage_price_drop      

        description_title = soup.find(attrs={'class':'Brand___StyledH-sc-zi64kd-1 BNEST'}).text
        data['description_title'] = description_title
        print("description title :",description_title)

        description_product_details = soup.find(attrs={'class':'MoreDetails___StyledSection-sc-1h9rbjh-4 bnsJyy'})
        # print(description_product_details.text)
        
        title  = description_product_details.find_all(attrs={'class','Label-sc-15v1nk5-0 MoreDetails___StyledLabel-sc-1h9rbjh-2 gJxZPQ iNgmUl'})
        description = description_product_details.find_all(attrs={'class','bullets pd-4 leading-xss text-md'})
        extra_links = description_product_details.find(attrs={'class','Button-sc-1dr2sn8-0 MoreDetails___StyledButton2-sc-1h9rbjh-5 kYQsWi jFVeIl'})
        print(" after description  ")
        extra_links_present = bool(extra_links)  
        try :
            # print(soup)
            try:
                ele = soup.find(attrs={'class','para-1'})
                print(ele.text)
            except :
                ele = ""
            element = soup.find(attrs={'class', 'para-1 TemplateOne__ActivePara-sc-8p1tso-22 hlgARw'})
            
            print(element.text)
            
            extra_topic = ele.text+element.text
        except Exception as e:
            print(e)
            extra_topic =""

        print(" above extral ink ")
        data['extra_links_present'] =extra_links_present
        data['extra_topic'] = extra_topic


        
        for title,description in zip(title,description):
            title_text = title.get_text(strip=True)
            description_text = description.get_text(separator='\n', strip=True)
            data[ title_text] = description_text
        
        return self.update_data_in_db(data,product_link)

        
        
    def update_data_in_db(self,data,product_link):

        ins = self.product_details.insert_one(data)
        if ins.inserted_id:
            print(ins.inserted_id)
            # print(product_link)
            query_to_update = {"specific_prodict_links":product_link}
            update_query = {"$set":{"processed":True}}
            print(query_to_update)
            print(update_query)
            print(query_to_update)
            upd = self.final_specific_links.update_one(query_to_update,update_query )
            print(upd.matched_count)
            if upd.matched_count == 1:
                print(" data updated ")
            else:
                print(" not updated ")
        return True 




        

        #         title_for_each_title = total_data[0].text
        #         print(title_for_each_title)
        #         description_for_each_title= total_data[1].text
        #         print(description_for_each_title)
        #         # title_for_each_title = total_data.text
                # description_for_each_title= total_data[1].title


        '''
        try :
            detailed_product_details = {}
            for each_details in description_product_details:
                total_data = each_details.find_all('div')
                title_for_each_title = total_data[0].text
                # print(title_for_each_title)
                description_for_each_title= total_data[2].text
                # print(description_for_each_title)
                # title_for_each_title = total_data.text
                # description_for_each_title= total_data[1].title
                if title_for_each_title not in  detailed_product_details.keys():
                    # print(title_for_each_title)
                    if title_for_each_title == 'Specification':
                        splitted_data = description_for_each_title.split('\n')
                        
                        for each_split in splitted_data:
                            if each_split != '':
                                split_in_description = each_split.split(':')
                                # print(len(split_in_description))
                                # print(split_in_description)
                                if len(split_in_description) ==1:
                                    temp_title = split_in_description[0].strip()
                                    # print(temp_title)
                                    detailed_product_details['Package_Content'].append( temp_title )
                                if len(split_in_description) >= 2:

                                    temp_title = split_in_description[0].strip()
                                    temp_value = split_in_description[1].strip()

                                    detailed_product_details['Package_Content'] = []

                                    if temp_title == 'Package Content':
                                        # Append the value and break the loop
                                        detailed_product_details[temp_title.replace(' ','_').replace(',','_').replace('/','_')] = []
                                        
                                    else:
                                        # Add other specification details
                                        if temp_title not in detailed_product_details.keys():
                                            detailed_product_details[temp_title.replace(' ','_').replace(',','_').replace('/','_')] = temp_value
                                else:
                                    # print(len(split_in_description))
                                    # print(split_in_description[0])
                                    pass 
                    else :
                        detailed_product_details[title_for_each_title.replace(' ','_').replace(',','_').replace('/','_')] = description_for_each_title
                        # print('----')
                else:
                    print(" else block - main ")
        except Exception as e:
            detailed_product_details={}
            print(e)
        try :
            other_product_info = {}
            content_divs = soup.find_all('div', style="font-family: 'ProximaNova-Regular';font-size:13px;line-height: 18px;color:8f8f8f;")
            desired_content_div = content_divs[2] 
            key_value_details = {}

            for detail in desired_content_div.stripped_strings:
                if ':' in detail:
                    key, value = detail.split(':', 1)
                    other_product_info[key.strip().replace(' ','_').replace(',','_').replace('/','_')] = value.strip()
        except Exception as e :
            other_product_info={}
            print(e)



        contact_details = {}

        parts = other_product_info['For_Queries_Feedback_Complaints__Contact_our_Customer_Care_Executive_at'].split('|')
        # Loop through each part to extract the key and value
        # print(parts[1] )
        for part in parts:
            # print(part)

            key_value = part.split(':',1)  # Split on the first colon only
            # print(key_value)
            if len(key_value) == 2:
                key = key_value[0].strip()
                # print(key)
                


                if key == 'Address':
                    
                    value = key_value[1].split('Email')[0]
                    contact_details[key] = value
                    email_data = key_value[1].split('Email')[1].split(':')
                    # print(email_data)
                    email_value = email_data[1]
                    contact_details['Email']= email_value
                

                else:

                    value = key_value[1].strip()

                    contact_details[key] = value
        # print(contact_details)

        # Update the main object
        # other_product_info = {}
        other_product_info['For_Queries_Feedback_Complaints__Contact_our_Customer_Care_Executive_at'] = contact_details

        # for key, value in key_value_details.items():
        #     print(f'{key}: {value}')


        print(detailed_product_details)
        print(other_product_info)
        '''

                

            
        



obj = scrape_e_commerce()
# for getting all product categorie 
# obj.get_all_category()
# print(obj.total_product_links)
#collected  data 

# for i in data :
#     obj.total_main_link.insert_one({"link":i,"processed":False})

'''collect specific links '''

'''
data = obj.total_main_link.find({"processed":False},no_cursor_timeout=True, batch_size=1000)

for each_data  in data:
    link = each_data['link']
    
    obj.find_links_by_link_modifying(link)
    sleep(1)
    obj.total_main_link.update_one({"link":link},{"$set":{"processed":True }})


# with open("product_links.txt",'w')as f1:
#     for link in obj.total_specific_links:
#         f1.write(f"{link}\n")

# print(len(obj.total_specific_links))


'''




'''collect total data from links '''

load_specific_links = obj.final_specific_links.find({"processed":False})

for each_link in load_specific_links:
       obj.collect_complete_data_from_link(each_link)
       

       








'''

data = ['https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/audio-accessories/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-rice-other-rice/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/home-kitchen-appliances/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/intimate-wash-care/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/dry-shampoo-conditioner/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/herbs-seasonings/indian-exotic-herbs/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/hangers-clips-rope/?nc=nb', 'https://www.bigbasket.com/pc/beverages/health-drink-supplement/children-2-5-yrs/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/flavoured-greek-yogurt/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/tomato-ketchup-sauces/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/everyday-medicine/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/beauty-grooming-devices/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/marinades/marinated-meat/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/cookware-sets/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/skin-care/lip-care/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/chocolates-biscuits/crackers-digestive/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/skin-care/face-care/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/pet-feeding-support/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/buckets-mugs/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/condensed-powdered-milk/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/body-sprays-mists/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/frozen-veggies-snacks/frozen-non-veg-snacks/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/bakeware/baking-tools-brushes/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/juicer-mixer-grinders/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/masalas-spices/whole-spices/?nc=nb', 'https://www.bigbasket.com/pc/beverages/water/packaged-water/?nc=nb', 'https://www.bigbasket.com/pc/beverages/fruit-juices-drinks/juices/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/laundry-storage-baskets/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/pickles-chutney/other-veg-pickle/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/masalas-spices/blended-masalas/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/wet-wipe-pocket-tissues/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/masalas-spices/herbs-seasoning/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/crockery-cutlery/dinner-sets/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/crockery-cutlery/glassware/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/paneer-tofu-cream/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/gingelly-oil/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/poultry/turkey/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/car-shoe-care/car-polish-cleaners/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/salt-sugar-jaggery/salts/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/imported-cleaners/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/eggs/farm-eggs/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/gourmet-ice-cream/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/biscuits-cookies/cookies/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/kitchen-accessories/strainer-ladle-spatula/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/exotic-sugar-salt/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/dishwash-liquids-pastes/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/mops-brushes-scrubs/dust-cloth-wipes/?nc=nb', 'https://www.bigbasket.com/pc/paan-corner/smoking-supplies/quit-smoking-alternatives/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/cold-pressed-oil/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/sports-fitness/swimming/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/cloth-dryer-iron-table/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/gourmet-popcorn/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/seasonal-accessories/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/containers-sets/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/antiseptics-bandages/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/vermicelli/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/oral-care/toothbrush/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/floor-other-cleaners/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/dips-dressings/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/nachos-chips/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/soap-cases-dispensers/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/regular-white-vinegar/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/international-cheese/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/car-shoe-care/shoe-shiners-brushes/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/eggs/other-eggs/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/tools-accessories/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/chocolates-candies/mints-chewing-gum/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-buds/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/kitchen-glass-drain/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/baby-gear-outdoor/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/honey-maple-syrup/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/jams-marmalade-spreads/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/trail-cocktail-mixes/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/detergent-powder-liquid/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/flower-bouquets-bunches/roses/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/hair-styling/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/makeup-accessories/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/caps-balloons-candles/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/eau-de-cologne/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/fish-tuna/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/other-seafood/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cookies-rusk-khari/bakery-biscuits-cookies/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/biscuits-cookies/salted-biscuits/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/flavoured-other-oils/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dry-fruits/raisins/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/pen-pencils/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/apples-pomegranate/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/rice-rice-products/poha-sabudana-murmura/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/electronic-accessories/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/buttermilk-lassi/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/gardening/live-plants/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/chargers-accessories/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/yogurt-shrikhand/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/cocktail-mixes/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/balsamic-cider-vinegar/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cereals-breakfast/muesli-rice-cakes/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/rice-rice-products/basmati-rice/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/gift-sets/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/tomatoes-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/bathing-bars-soaps/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-bath/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/gourmet-breads/panini-focaccia-pita/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/breakfast-cereals/granola-cereal-bars/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/dry-fish/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-food-formula/organic-baby-food/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/masalas-spices/cooking-pastes/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/mothers-maternity/maternity-health-supplements/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/pet-meals-treats/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/shower-gel-body-wash/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/organic-fruits-vegetables/organic-fruits/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/feeding-nursing/sippers-bottles/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/garbage-bags/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/ghee-vanaspati/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/indian-mithai/tinned-packed-sweets/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/steel-utensils/copper-utensils/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/cup-noodles/?nc=nb', 'https://www.bigbasket.com/pc/beverages/energy-soft-drinks/non-alcoholic-drinks/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/bathing-accessories/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/chocolates-biscuits/marshmallow-candy-jelly/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/fabric-pre-post-wash/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/steel-utensils/steel-storage-containers/?nc=nb', 'https://www.bigbasket.com/pc/beverages/coffee/instant-coffee/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/erasers-sharpeners/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/breads-buns/buns-pavs-pizza-base/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/wine-rice-vinegar/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/disposable-cups-plates/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dry-fruits/cashews/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/hakka-noodles/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/pasta-soup-noodles/jasmine-sushi-rice/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/health-supplements/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/mayonnaise/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/fresh-water-fish/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/specialty/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/adult-diapers/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/games-calculators/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/blended-cooking-oils/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-powder/?nc=nb', 'https://www.bigbasket.com/pc/beverages/health-drink-supplement/men-women/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/chilli-soya-sauce/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/womens-deodorants/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-flours/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/mutton-lamb/fresh-mutton/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/flower-bouquets-bunches/other-flowers/?nc=nb', 'https://www.bigbasket.com/pc/apparel/mens-apparel/mens-bottom-wear/?nc=nb', 'https://www.bigbasket.com/pc/beverages/water/spring-water/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/cream-cheese-spreads/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/canola-rapeseed-oil/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/beans-brinjals-okra/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/decorations/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/ice-creams-desserts/ice-creams/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/gourmet-breads/gourmet-bread/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/cotton-ear-buds/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/frozen-veggies-snacks/frozen-indian-breads/?nc=nb', 'https://www.bigbasket.com/pc/apparel/womens-apparel/womens-accessories/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/mustard-cheese-sauces/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/instant-noodles/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/racks-holders/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cakes-pastries/doughnuts-mousses/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/sports-fitness/exercise-fitness/?nc=nb', 'https://www.bigbasket.com/pc/beverages/tea/leaf-dust-tea/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/diapers-wipes/diapers/?nc=nb', 'https://www.bigbasket.com/pc/beverages/energy-soft-drinks/sports-energy-drinks/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/colours-crayons/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/snacks-namkeen/chips-corn-snacks/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/gardening/gardening-tools/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/coffee-pre-mix/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/baking-accessories/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/gift-wraps-bags/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/deodorant/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/steel-utensils/bowls-vessels/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/pickles-chutney/lime-mango-pickle/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/aluminium-foil-clingwrap/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cookies-rusk-khari/khari-cream-rolls/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/sausages-bacon-salami/pork-ham/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/talcum-powder/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/skin-care/body-care/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/other-plastic-ware/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/descaler/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/baby-toys/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/perfume/?nc=nb', 'https://www.bigbasket.com/pc/beverages/energy-soft-drinks/icetea-non-aerated-drink/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/breakfast-cereals/oats-porridge/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/gourmet-tea-tea-bags/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/vinegar/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/atta-flours-sooji/rice-other-flours/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/mangoes/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dry-fruits/almonds/?nc=nb', 'https://www.bigbasket.com/pc/apparel/mens-apparel/mens-accessories/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/dolls-soft-toys/?nc=nb', 'https://www.bigbasket.com/pc/apparel/womens-apparel/womens-innerwear/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/bakery-snacks/breadcrumbs-croutons/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/fresheners-repellents/air-freshener/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/panty-liners/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/choco-nut-spread/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/lunch-boxes/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/chocolates-candies/toffee-candy-lollypop/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/chocolates-candies/chocolates/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/skin-care/eye-care/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/gourmet-juices-drinks/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/oral-care/floss-tongue-cleaner/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/other-edible-oils/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/oral-care/electric-toothbrush/?nc=nb', 'https://www.bigbasket.com/pc/beverages/fruit-juices-drinks/unsweetened-cold-press/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/poultry/frozen-chicken/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/sanitary-napkins/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/hand-wash-sanitizers/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/mops-brushes-scrubs/brooms-dust-pans/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/frozen-veggies-snacks/frozen-veg-snacks/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/indian-mithai/fresh-sweets/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/battery-power-bank/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/agarbatti-incense-sticks/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/cuts-sprouts/cut-fruit-tender-coconut/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/aerated-still-sparkling/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/oral-care/mouthwash/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/curry-paste-coconut-milk/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-masalas-spices/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-oil-shampoo/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/potato-onion-tomato/?nc=nb', 'https://www.bigbasket.com/pc/apparel/girls-wear/girls-innerwear/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/dustbins/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/dishwash-bars-powders/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/diapers-wipes/nappies-rash-cream/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/non-alcoholic-beer-wine/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/face-masks-safety-gears/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/sausages-bacon-salami/lamb/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/paper-napkin-tissue-box/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/shaving-care/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/nutrition-drink-mixes/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/atta-flours-sooji/atta-whole-wheat/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/bakery-snacks/puffs-patties-sandwiches/?nc=nb', 'https://www.bigbasket.com/pc/beverages/coffee/ground-coffee/?nc=nb', 'https://www.bigbasket.com/pc/apparel/boys-wear/boys-innerwear/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/kitchen-accessories/choppers-graters/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/dry-fruits-berries/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/feeding-nursing/bibs-napkins/?nc=nb', 'https://www.bigbasket.com/pc/beverages/fruit-juices-drinks/syrups-concentrates/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/bakeware/bakeware-accessories/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/books-magazines/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/kadai-fry-pans/?nc=nb', 'https://www.bigbasket.com/pc/beverages/energy-soft-drinks/cold-drinks/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/umbrella/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/meats-sausages/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-creams-lotions/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/soya-mustard-oils/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/wall-hooks-hangers/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cakes-pastries/muffins-cup-cakes/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dals-pulses/toor-channa-moong-dal/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/banana-sapota-papaya/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/thai-asian-sauces/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/sports-fitness/indoor-sports/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-food-formula/lactose-free-baby-food-formula/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/feeding-nursing/baby-dishes-utensils/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/jam-conserve-marmalade/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/chocolates-biscuits/international-chocolates/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/party-festive-needs/gifts/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/flavoured-soya-milk/?nc=nb', 'https://www.bigbasket.com/pc/apparel/mens-apparel/mens-innerwear/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/led-bulbs-battens/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/cards-party-games/?nc=nb', 'https://www.bigbasket.com/pc/beverages/tea/exotic-flavoured-tea/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/flower-bouquets-bunches/marigold/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/butter-margarine/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/masalas-spices/powdered-spices/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/canned-seafood/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/sports-fitness/outdoor-sports/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/shampoo-conditioner/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/steel-utensils/plates-tumblers/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-health/?nc=nb', 'https://www.bigbasket.com/pc/beverages/health-drink-supplement/glucose-powder-tablets/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/organic-fruits-vegetables/organic-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/mops-brushes-scrubs/toilet-other-brushes/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/breads-buns/milk-white-sandwich/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/gourd-pumpkin-drumstick/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/kids-deo/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/combos-gift-sets/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/marine-water-fish/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/drinks-beverages/health-drinks/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/instant-pasta/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/bath-salts-oils/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/metal-furniture-cleaner/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/cheese/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/papads-ready-to-fry/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/face/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/pasta-soup-noodles/pastas-spaghetti/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dry-fruits/mukhwas/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/pet-cleaning-grooming/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/bath-hand-wash/body-scrubs-exfoliants/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/leafy-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/sexual-wellness/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cakes-pastries/tea-cakes-slice-cakes/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/indian-mithai/chikki-gajjak/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/home-baking/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/rice-rice-products/raw-rice/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/gourmet-breads/bagels-baguette/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/pork-other-meats/fresh-frozen-pork/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/organic-cold-press-oil/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/talc/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/olive-canola-oils/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/dessert-mixes/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cakes-pastries/pastries-brownies/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/disinfectant-spray-cleaners/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/atta-flours-sooji/sooji-maida-besan/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/notebooks-files-folders/?nc=nb', 'https://www.bigbasket.com/pc/apparel/womens-apparel/womens-bottom-wear/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/exotic-fruits-veggies/exotic-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/milk/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/mens-deodorants/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/hair-scalp-treatment/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/gourmet-breads/croissants-bagels/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/hair-oil-serum/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/snacks-namkeen/namkeen-savoury-snacks/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/baking-cake-decorations/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/hummus-cheese-salsa-dip/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/moustache-beard-care/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/skin-care/aromatherapy/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/herbs-seasonings/lemon-ginger-garlic/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/bins-bathroom-ware/bath-stool-basin-sets/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/crockery-cutlery/cups-mugs-tumblers/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/crockery-cutlery/plates-bowls/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dals-pulses/urad-other-dals/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cakes-pastries/birthday-party-cakes/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/lips/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-gift-sets/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/eau-de-parfum/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/canned-food/?nc=nb', 'https://www.bigbasket.com/pc/paan-corner/smoking-supplies/hookah-needs/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-food-formula/baby-food/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/cooking-coconut-oil/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/fresheners-repellents/insect-repellent/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/flours-pre-mixes/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/pickles-chutney/non-veg-pickle/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/cotton-seed-oil/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/cuts-sprouts/fresh-salads-sprouts/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/gingelly-groundnut-oils/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/poultry/fresh-chicken/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/extra-virgin-olive-oil/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/mops-brushes-scrubs/mops-wipers/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/soups/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/nails/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/edible-oils-ghee/sunflower-rice-bran-oil/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-sugar-jaggery/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/kiwi-melon-citrus-fruit/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/pickles-chutney/chutney-powder/?nc=nb', 'https://www.bigbasket.com/pc/beverages/health-drink-supplement/kids-5yrs/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/beans-pulses/?nc=nb', 'https://www.bigbasket.com/pc/beverages/energy-soft-drinks/soda-cocktail-mix/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/bakery-snacks/cheese-garlic-bread/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/board-games-puzzles/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/butter-cream/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/feeding-nursing/nursing-tools/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/pet-toys/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/fresheners-repellents/mosquito-repellent/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-edible-oil-ghee/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/cooking-chocolate-cocoa/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/breakfast-cereals/kids-cereal/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/mutton-lamb/frozen-mutton/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/fruits-pulps/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/pasta-soup-noodles/imported-noodles/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/frozen-veggies-snacks/frozen-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/fresh-milk/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/gardening/fertilizers-pesticides/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/grills-toasters/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/herbs-seasonings-rubs/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/supplements-proteins/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cookies-rusk-khari/premium-cookies/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/exam-pads-pencil-box/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/tinned-processed-food/olive-jalapeno-gherkin/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cookies-rusk-khari/rusks/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/pressure-cookers/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/pet-food-accessories/pet-collars-leashes/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/ayurveda/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/chocolate-peanut-spread/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dals-pulses/cereals-millets/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/coffee-maker-kettles/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/healthy-baked-snacks/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/root-vegetables/?nc=nb', 'https://www.bigbasket.com/pc/beverages/water/flavoured-water/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/steel-utensils/steel-lunch-boxes/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/makeup-kits-gift-sets/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/lamp-lamp-oil/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/eau-de-toilette/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/learning-education/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/kitchen-accessories/lighters/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/snacks-dry-fruits-nuts/roasted-seeds-nuts/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/poultry/duck-goose/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/prawns-shrimps/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/cookies-rusk-khari/healthy-organic-cookies/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/hair-removal/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/breakfast-cereals/flakes/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/flask-casserole/casserole/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/pasta-soup-noodles/imported-soups/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/gardening/seeds-sapling/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/chocolates-candies/gift-boxes/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/bakeware/bakeware-moulds-cutters/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/flask-casserole/vacuum-flask/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/sauces-spreads-dips/salad-dressings/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/microwavable-cookware/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/tofu/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/cucumber-capsicum/?nc=nb', 'https://www.bigbasket.com/pc/beverages/health-drink-supplement/diabetic-drinks/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/fish-seafood/frozen-fish-seafood/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/seasonal-fruits/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/combs-brushes-clippers/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/cuts-sprouts/cut-peeled-veggies/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/gardening/pots-planters-trays/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/chocolates-biscuits/luxury-chocolates-gifts/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-dals-pulses/?nc=nb', 'https://www.bigbasket.com/pc/apparel/mens-apparel/mens-sports-active-wear/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/camphor-wicks/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cooking-baking-needs/quinoa-grains/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/battery-electrical/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/soothers-teethers/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-laundry/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/car-shoe-care/car-freshener/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cereals-breakfast/imported-oats-porridge/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/cook-and-serve/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/electronics-devices/computer-peripherals/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/stationery/scissor-glue-tape/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/appliances-electricals/air-fryers-rice-cookers/?nc=nb', 'https://www.bigbasket.com/pc/paan-corner/smoking-supplies/smoking-accessories/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/vehicle-action-toys/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/eggs/protein-eggs/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/diapers-wipes/baby-wipes/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/flower-bouquets-bunches/bouquets/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/bakery-snacks/bread-sticks-lavash/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/biscuits-cookies/marie-health-digestive/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/toys-games/baby-toddler-toys/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/crockery-cutlery/cutlery-spoon-fork/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cereals-breakfast/cereal-granola-bars/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/kitchen-accessories/kitchen-tools-other-accessories/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/heat-eat-ready-meals/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/detergent-bars/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-fruits/fruit-baskets/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/face-body/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/oral-care/toothpaste/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/salt-sugar-jaggery/sugarfree-sweeteners/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-accessories/other-baby-accessories/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/ready-to-cook-eat/breakfast-snack-mixes/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/all-purpose-cleaners/toilet-cleaners/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/feminine-hygiene/tampons-menstrual-cups/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/cuts-sprouts/fresh-juices-milkshakes/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/healthcare-devices/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/dry-fruits/other-dry-fruits/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/non-dairy/dairy-free-vegan/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/sausages-bacon-salami/turkey-duck/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-bath-hygiene/baby-oral-care/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/oils-vinegar/pure-pomace-olive-oil/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/biscuits-cookies/glucose-milk-biscuits/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/cereals-breakfast/gourmet-flakes/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/storage-accessories/water-fridge-bottles/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/kitchen-accessories/knives-peelers/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/baby-food-formula/infant-formula/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/pooja-thali-bells/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-millet-flours/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/rice-rice-products/boiled-steam-rice/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/breads-buns/brown-wheat-multigrain/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/chocolates-biscuits/cookies-biscotti-wafer/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/health-medicine/slimming-products/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/exotic-fruits-veggies/exotic-fruits/?nc=nb', 'https://www.bigbasket.com/pc/beverages/tea/green-tea/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/car-shoe-care/shoe-polish/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/organic-staples/organic-dry-fruits/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/gas-stove/?nc=nb', 'https://www.bigbasket.com/pc/kitchen-garden-pets/cookware-non-stick/tawa-sauce-pan/?nc=nb', 'https://www.bigbasket.com/pc/baby-care/mothers-maternity/maternity-personal-care/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/spreads-sauces-ketchup/honey/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/noodle-pasta-vermicelli/pasta-macaroni/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/hair-care-styling/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/eggs/country-eggs/?nc=nb', 'https://www.bigbasket.com/pc/bakery-cakes-dairy/dairy/curd/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/mens-grooming/bath-shower/?nc=nb', 'https://www.bigbasket.com/pc/apparel/mens-apparel/mens-top-wear/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/biscuits-cookies/cream-biscuits-wafers/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/candles-match-box/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/cuts-sprouts/recipe-packs/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/hair-care/hair-color/?nc=nb', 'https://www.bigbasket.com/pc/snacks-branded-foods/breakfast-cereals/muesli/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/fragrances-deos/attar/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/detergents-dishwash/imported-home-care/?nc=nb', 'https://www.bigbasket.com/pc/beauty-hygiene/makeup/eyes/?nc=nb', 'https://www.bigbasket.com/pc/eggs-meat-fish/sausages-bacon-salami/chicken-sausages/?nc=nb', 'https://www.bigbasket.com/pc/beverages/tea/tea-bags/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/mops-brushes-scrubs/utensil-scrub-pad-glove/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/toilet-paper/?nc=nb', 'https://www.bigbasket.com/pc/gourmet-world-food/dairy-cheese/milk-soya-drinks/?nc=nb', 'https://www.bigbasket.com/pc/fruits-vegetables/fresh-vegetables/cabbage-cauliflower/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/pooja-needs/other-pooja-needs/?nc=nb', 'https://www.bigbasket.com/pc/foodgrains-oil-masala/salt-sugar-jaggery/sugar-jaggery/?nc=nb', 'https://www.bigbasket.com/pc/cleaning-household/disposables-garbage-bag/kitchen-rolls/?nc=nb']



'''