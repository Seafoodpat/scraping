import csv
import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getProductInfo(filename, brand, max_page):
    with open(filename, 'w') as csvfile:
        fieldnames = ['sku', 'Brand', 'Product Name', 'Price', 'Description', 'Way to Use', 'Ingredient', 'image_1', 'image_2']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()

        num = 1
        cookies = {'iher-pref1': 'ctd=www&sccode=CN&lan=zh-CN&scurcode=HKD&lchg=1&ifv=1&wh=77&noitmes=192&chkdc=5'}
        html = requests.get("http://www.iherb.cn/" + brand + "?p=7", cookies=cookies)
        bsObj = BeautifulSoup(html.text)

        products = bsObj.findAll("article", {"class": "product"})
        #try:
        for product in products:
            #sku (lv1)
            pid = product['id'].replace("_", "/")
            sku = pid.replace("pid/", "")
            #Brand (lv1)
            brand = bsObj.find("div", {"id": "breadCrumbs"}).find("a", {"class": "last"}).text
            #Product Name (lv1)
            product_name = product.span.text
            #Price (lv1)
            price = product.find("span", {"itemprop": "price"})['content']
            #product link (lv1)
            link = "http://www.iherb.cn/" + pid
            bsItemObj = BeautifulSoup(urlopen(link))
            #Description (lv2)
            if bsItemObj.find("div", {"itemprop": "description"}) == None:
                description = "N/A"
            else:
                description = bsItemObj.find("div", {"itemprop": "description"}).text.replace('\n', "<br>").replace('\r', "")
            #Way to use (lv2)
            if bsItemObj.find("div", {"class": "prodOverviewDetail"}) == None:
                way_to_use = "N/A"
            else:
                way_to_use = bsItemObj.find("div", {"class": "prodOverviewDetail"}).text.replace('\n', "<br>").replace('\r', "")
            #Ingredient (lv2)
            if bsItemObj.find("div", {"class": "prodOverviewIngred"}) == None:
                ingred = "N/A"
            else:
                ingred = bsItemObj.find("div", {"class": "prodOverviewIngred"}).text.replace('\n', "<br>").replace('\r', "")
            #image_name/link (lv2)
            imgURL = []
            imgs = bsItemObj.findAll("img", {"alt": product_name})
            for img in imgs:
                imgURL.append(img.get('src'))

            print("Processing: " + str(num))
            num += 1
            writer.writerow({   'sku': sku,
                                'Brand': brand,
                                'Product Name': product_name,
                                'Price': price,
                                'Description': description,
                                'Way to Use': way_to_use,
                                'Ingredient': ingred,
                                'image_1': '|'.join(imgURL)
                                })


#getProductInfo("Doctor-s-Best.csv", "Doctor-s-Best", 1)
#getProductInfo("Nature-Made.csv", "Nature-Made", 1)
#getProductInfo("New-Chapter.csv", "New-Chapter", 1)
#getProductInfo("Natrol.csv", "Natrol", 1)
#getProductInfo("Nature-s-Bounty.csv", "Nature-s-Bounty", 1)
#getProductInfo("Jarrow-Formulas.csv", "Jarrow-Formulas", 2)
#getProductInfo("Nature-s-Way3.csv", "Nature-s-Way", 3)
#getProductInfo("Source-Naturals4.csv", "Source-Naturals", 4)
getProductInfo("Now-Foods7.csv", "Now-Foods", 7)


#Reference:
#http://blog.csdn.net/pipisorry/article/details/47905781
