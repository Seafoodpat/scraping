import csv
import re
import requests
from bs4 import BeautifulSoup

def productsCost(filename, link, email, pw):
    with open(filename, 'w') as csvfile:
        fieldnames = ['sku', 'Cost']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()

        session = requests.Session()

        params = {'email': email, 'password': pw}
        s = session.post(link, params)
        bsObj = BeautifulSoup(s.text)
        nav = bsObj.find("ul", {"class": "navbar-nav"}).findAll("li", {"class": "dropdown"})

        for n in nav:
            link = n.find("a", {"class": "see-all"})['href']

            html01 = session.get(link)
            bsObj01 = BeautifulSoup(html01.text)
            sub = bsObj01.findAll("li", {"class": "ref-search-link"})
            for s in sub:
                subName = re.search('(.+) \(\d*\)', s.text).group(1)
                subLink = s.find("a")['href']

                html02 = session.get(subLink + "&limit=100")
                bsObj02 = BeautifulSoup(html02.text)
                items = bsObj02.find("div", {"id": "content"}).findAll("div", {"class": "product-thumb"})
                for item in items:
                    #Item Link
                    itemLink = item.find("a")['href']
                    #Item ID
                    itemID = re.search('product_id=(.+)&limit=100', itemLink).group(1)
                    #Item Cost
                    if not " " in item.find("div", {"class": "price"}).text.strip():
                        itemCost = item.find("div", {"class": "price"}).text.strip()
                    else:
                        itemCost = item.find("div", {"class": "price"}).find("span", {"class": "price-new"}).text.strip()
                    print(itemID + itemCost)
                    writer.writerow({   'sku': itemID,
                                        'Cost': itemCost
                                        })

productsCost('cost.csv' , "http://beautyavenueco.com/index.php?route=account/login", "acc", "pw")
