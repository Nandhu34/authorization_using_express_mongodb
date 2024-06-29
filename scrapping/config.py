test_url="https://chennaiangadi.com/pl/miniature-toys/111"
url = "https://www.bigbasket.com/pc/bakery-cakes-dairy/bakery-snacks/breadcrumbs-croutons/?nc=nb"
db_connection_link = 'mongodb://localhost:27017'
db_name = "scrapped_data"
collection_name ="product_details"
filter_xpath = "(//div[@class='relative h-full'])[4]"

final_product_link_xpath ="(//ul[@class='jsx-1259984711 w-56 px-2.5 bg-white text-darkOnyx-800 rounded-r-xs'])[2]"

category_x_path = "//ul[@class='jsx-1259984711 w-56 px-2.5 bg-darkOnyx-800 text-silverSurfer-100 rounded-l-xs']//li[@class='jsx-1259984711']"

xpath_for_sub_category = "(//ul[@class='jsx-1259984711 w-56 px-2.5 bg-silverSurfer-200 text-darkOnyx-800'])[2]//li[@class='jsx-1259984711']"

xpath_for_product = " (//ul[@class='jsx-1259984711 w-56 px-2.5 bg-white text-darkOnyx-800 rounded-r-xs'])[2]//li[@class='jsx-1259984711']//a"

xpath_to_get_final_product_link = "(//ul[@class='jsx-1259984711 w-56 px-2.5 bg-white text-darkOnyx-800 rounded-r-xs'])[2]//li[@class='jsx-1259984711']//a"