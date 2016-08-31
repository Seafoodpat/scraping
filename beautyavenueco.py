import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

def productsInfo(filename, link):
    with open(filename, 'w') as csvfile:
        fieldnames = ['sku', 'Main Cate Name', 'Sub Cate Name', 'Brand', 'Product Name', 'Status', 'Selling Price', 'Cost', 'Description', 'Option',
                      'image_name1', 'image_name2', 'image_name3', 'image_name4', 'image_name5', 'image_name6',
                      'image_name7', 'image_name8', 'image_name9', 'image_name10', 'image_name11', 'image_name12']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()

        item_count = 0

        html = urlopen(link)
        bsObj = BeautifulSoup(html)
        nav = bsObj.find("ul", {"class": "navbar-nav"}).findAll("li", {"class": "dropdown"})
        for n in nav:
            mainName = n.find("a", {"class": "see-all"}).text.strip().replace("顯示所有 ", "")
            mainLink = n.find("a", {"class": "see-all"})['href']

            # Lv 01 Loop: Main Category -> Sub Category
            html01 = urlopen(mainLink)
            bsObj01 = BeautifulSoup(html01)
            sub = bsObj01.findAll("li", {"class": "ref-search-link"})
            for s in sub:
                subName = re.search('(.+) \(\d*\)', s.text).group(1)
                subLink = s.find("a")['href']

                # Lv 02 Loop: Sub Category -> Item List
                html02 = urlopen(subLink + "&limit=100")
                bsObj02 = BeautifulSoup(html02)
                items = bsObj02.find("div", {"id": "content"}).findAll("div", {"class": "product-thumb"})
                for item in items:
                    #Item Link
                    itemLink = item.find("a")['href']
                    #Item ID
                    itemID = re.search('product_id=(.+)&limit=100', itemLink).group(1)
                    #Item Name
                    itemName = item.find("a").text.strip()
                    #Item Price
                    if not " " in item.find("div", {"class": "price"}).text.strip():
                        itemPrice = item.find("div", {"class": "price"}).text.strip().replace('$', '')
                    else:
                        itemPrice = item.find("div", {"class": "price"}).find("span", {"class": "price-new"}).text.strip().replace('$', '')

                    # Lv 03 Loop: Item List -> Item Detail
                    html03 = urlopen(itemLink)
                    bsObj03 = BeautifulSoup(html03)
                    #Item Brand
                    itemBrand = bsObj03.find("h1").find_next('ul').find('a').text.strip()
                    #status
                    itemStatus = bsObj03.find("h1").find_next('ul').find_next('li').find_next('li').text.strip().replace("庫存狀態： ", "")
                    #Item Images
                    itemImage = []
                    images = bsObj03.find("ul", {"class": "thumbnails"}).findAll("a")
                    for image in images:
                        itemImage.append(image['href'])
                    #Item Description
                    itemDescription = '"{}"'.format(bsObj03.find("div", {"id": "tab-description"})).replace("\n", "").replace("\r", "")
                    if bsObj03.findAll("option"):
                        itemOption = []
                        options = bsObj03.findAll("option")
                        for option in options:
                            itemOption.append(option.text.strip())
                        itemOption.pop(0)
                    else:
                        itemOption = ""

                    item_count += 1
                    print("Product count: " + str(item_count) + '\n' +
                          "Product Name: "+ itemName)
                    writer.writerow({   'sku': 'ba-' + itemID,
                                        'Main Cate Name': mainName,
                                        'Sub Cate Name': subName,
                                        'Brand': itemBrand,
                                        'Product Name': itemName,
                                        'Status': itemStatus,
                                        'Selling Price': itemPrice,
                                        'Description': itemDescription,
                                        'Option': '|'.join(itemOption),
                                        'image_name1': '|'.join(itemImage)
                                        })
#第一行咩都有，之後only show option
productsInfo('korean_cos_enduser.csv' , "http://beautyavenueco.com/index.php?route=common/home")
