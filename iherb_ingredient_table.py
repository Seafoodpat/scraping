import csv
import re
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getProductInfo(filename, brand, max_page):
    with open(filename, 'w') as csvfile:
        fieldnames = ['sku', 'Ingredient']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()

        num = 1
        cookies = {'iher-pref1': 'ctd=www&sccode=CN&lan=zh-CN&scurcode=HKD&lchg=1&ifv=1&wh=77&noitmes=192&chkdc=5'}
        html = requests.get("http://www.iherb.cn/" + brand + "?p=7", cookies=cookies)
        bsObj = BeautifulSoup(html.text)

        products = bsObj.findAll("div", {"class": "product"})
        for product in products:
            #sku (lv1)
            pid = product['id'].replace("_", "/")
            sku = pid.replace("pid/", "")
            #product link (lv1)
            link = "http://www.iherb.cn/" + pid
            bsItemObj = BeautifulSoup(urlopen(link))
            try:
                #Ingredient (lv2)
                if bsItemObj.find("div", {"class": "supplement-facts-container"}).find("table") == None:
                    ingred = "N/A"
                else:
                    ingred = bsItemObj.find("div", {"class": "supplement-facts-container"}).find("table")

                print("Processing: " + str(num))
                num += 1
                writer.writerow({   'sku': sku,
                                    'Ingredient': str(ingred).replace("\n", "/n").replace("\r", ""),
                                    })
            except AttributeError:
                pass


#getProductInfo("Doctor-s-Best.csv", "Doctor-s-Best", 1)
#getProductInfo("Nature-Made.csv", "Nature-Made", 1)
#getProductInfo("New-Chapter.csv", "New-Chapter", 1)
#getProductInfo("Natrol.csv", "Natrol", 1)
#getProductInfo("Nature-s-Bounty.csv", "Nature-s-Bounty", 1)
#getProductInfo("Jarrow-Formulas2.csv", "Jarrow-Formulas", 2)
#getProductInfo("Nature-s-Way3.csv", "Nature-s-Way", 3)
#getProductInfo("Source-Naturals4.csv", "Source-Naturals", 4)
getProductInfo("Now-Foods7.csv", "Now-Foods", 7)


#Reference:
#http://blog.csdn.net/pipisorry/article/details/47905781
