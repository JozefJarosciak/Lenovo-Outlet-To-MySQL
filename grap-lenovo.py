import requests as requests
from bs4 import BeautifulSoup
import re
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="products"
)

mycursor = mydb.cursor()

userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
searchURL = "https://www.lenovo.com/us/en/outletus/laptops/c/LAPTOPS?q=%3Aprice-desc&page="
soup = BeautifulSoup(requests.get(searchURL, headers=userAgent).text, 'html.parser')

# Get number of pages available on the Lenovo Outlet site
last_page = int(re.search('page=(.*)" rel=', str(soup.select_one('a:contains(»)'))).group(1))
print("Number of Pages: " + str(last_page))


# Get content from all Lenovo Outlet pages
for x in range(last_page+1):
    url = searchURL+str(x)
    soup = BeautifulSoup(requests.get(url, headers=userAgent).text, 'html.parser')
    print(url)

    # Gather the detail for each laptop deal found on the page
    laptop_name = soup.select('h3[class="facetedResults-title"]')
    buy_link = soup.select('a[class="button-called-out button-full facetedResults-cta"]')
    list_price = soup.select('dd[itemprop="listPrice"]')
    actual_price = soup.select('dd[itemprop="price"]')
    you_save_price = soup.select('dd[itemprop="youSave"]')
    stock = soup.select('span[class="rci-msg"]')
    laptop_config = soup.select('div[class="facetedResults-feature-list"]')



    # Print the details
    i = 0
    while i < len(laptop_name):
        print(laptop_name[i].text.strip())
        print("https://www.lenovo.com" + buy_link[i].get('href'))
        print(list_price[i].text.strip()[1:])
        print(actual_price[i].text.strip()[1:])
        print(you_save_price[i].text.strip()[1:])
        print(stock[i].text.strip())
        #print(str(laptop_config[i].text).replace('\n', '!'))
        part_number = re.search('number:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
        print(part_number)

        try:
            processor = re.search('Processor:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(processor)
        except:
            processor = ""

        try:
            operating_system = re.search('System:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(operating_system)
        except:
            operating_system = ""

        try:
            hard_drive = re.search('Drive:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(hard_drive)
        except:
            hard_drive = ""

        try:
            graphics = re.search('Graphics:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(graphics)
        except:
            graphics = ""

        try:
            warranty = re.search('Warranty:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(warranty)
        except:
            warranty = ""

        try:
            memory = re.search('Memory:!(.*)!!!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0]
            print(memory)
        except:
            memory = ""

        try:
            battery = re.search('Battery:!(.*)!', str(laptop_config[i].text).replace('\n', '!')).group(1).split("!!!", 1)[0][:-1]
            print(battery)
        except:
            battery = ""

        print ("-----------------------")



        sql = "INSERT INTO `products`.`lenovo_laptops` (`laptop_name`, `buy_link`, `list_price`, `actual_price`, `you_save_price`, `stock`, `part_number`, `processor`, `operating_system`, `hard_drive`, `graphics`, `warranty`, `memory`, `battery`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (str(laptop_name[i].text.strip()), str("https://www.lenovo.com" + buy_link[i].get('href')), str(re.sub(",", "", list_price[i].text.strip()[1:])), str(re.sub(",", "", actual_price[i].text.strip()[1:])), str(re.sub(",", "", you_save_price[i].text.strip()[1:])), str(stock[i].text.strip()), str(part_number), str(processor), str(operating_system), str(hard_drive), str(graphics), str(warranty), str(memory), str(battery))
        assert isinstance(mycursor, object)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        i += 1

# DB CREATE CODE
# CREATE TABLE `lenovo_laptops` (
#     `laptop_name` VARCHAR(150) NOT NULL,
#                                    `buy_link` VARCHAR(200) NULL DEFAULT NULL,
#                                                                         `list_price` FLOAT NULL DEFAULT NULL,
#                                                                                                         `actual_price` FLOAT NULL DEFAULT NULL,
#                                                                                                                                           `you_save_price` FLOAT NULL DEFAULT NULL,
#                                                                                                                                                                               `stock` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                 `part_number` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                         `processor` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                               `operating_system` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                            `hard_drive` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                                                                   `graphics` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                                                                                                        `warranty` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                                                                                                                                             `memory` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                `battery` VARCHAR(150) NULL DEFAULT NULL,
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    `timestamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       INDEX `laptop_name` (`laptop_name`)
# )
# ENGINE=InnoDB
# ;
