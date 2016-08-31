import csv
import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def getProductInfo(filename, link):
    with open(filename + '.csv', 'w') as csvfile:
        fieldnames = ['sku', 'Category ID', 'Brand', 'Product Name', 'Option', 'Price', 'Description', 'image_name1', 'image_name2', 'image_name3', 'image_name4', 'image_name5']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()


        product_count = 1

        html = link
        bsObj = BeautifulSoup(urlopen(html))
        products = bsObj.findAll("a", {"class": "productlistImg"})
        for product in products:
            productID = product["href"].split("/")
            #JONS link
            productJSON = "https://hk.strawberrynet.com/ajaxProdDetail.aspx?ProdId="+productID[4]+"&CurrId=HKD"
            response = urlopen(productJSON).read().decode('utf-8')
            responseJson = json.loads(response)
            index = 0
            while index < len(responseJson.get("Prods")):
                #Brand
                brand = responseJson.get("Brand").get("BrandLangName")
                #Category ID
                cate = responseJson.get("ProdCatgID")
                #Product Name
                product_name = responseJson.get("Prods")[index].get("ProdLangName")
                #Option Type and Value
                optType = responseJson.get("Prods")[index].get("OptionType")
                optValue = responseJson.get("Prods")[index].get("OptionValue")
                option = optType + str(optValue)
                #Price
                p = responseJson.get("Prods")[index].get("ShopPrice")
                intDigit = re.search('\>(\d+,?\d+)\<', p).group(1)
                decimalDigit = re.search('\>(\.\d+)\<', p).group(1)
                price = intDigit + decimalDigit
                #Description
                descriptionText = []
                descriptions = responseJson.get("Prods")[index].get("Description")
                for description in descriptions:
                    descriptionText.append(description.get("text"))
                #image_url
                imgURL = []
                imgs = responseJson.get("Prods")[index].get("ProductImages")
                for img in imgs:
                    imgURL.append(img.get("img700Src"))
                product_count += 1
                print(  "Product count: " + str(product_count) + '\n' +
                        "Brand: " + brand + '\n' +
                        "Product Name: "+ product_name + '\n' +
                        "Option: " + option + '\n')
                writer.writerow({   'sku': productID[4],
                                    'Category ID': cate,
                                    'Brand': brand,
                                    'Product Name': product_name,
                                    'Option': option,
                                    'Price': price,
                                    'Description': '"{}"'.format('\\n'.join(descriptionText)),
                                    'image_name1': '|'.join(imgURL).replace("https://simg1.strawberrynetmedia.com/images/products/l/", "")
                                    })
                index += 1

getProductInfo("bbcc", "https://hk.strawberrynet.com/makeup/bb-cc-cream/t/")
