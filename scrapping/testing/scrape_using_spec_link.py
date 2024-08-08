from  selenium import webdriver 
from time import sleep
from selenium.webdriver.common.by import By 

driver = webdriver.Chrome()



link = 'https://www.bigbasket.com/pd/40322234/boat-stone-650-bluetooth-speaker-charcoal-black-1-pc/?nc=l3category&t_pos_sec=1&t_pos_item=1&t_s=Stone+650+Bluetooth+Speaker+-+Charcoal+Black'
driver.get(link )


sleep(3)


