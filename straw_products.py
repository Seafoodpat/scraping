import csv
import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def getProductInfo(filename, link, max_page):
    with open(filename + '.csv', 'w') as csvfile:
        fieldnames = ['sku', 'Category ID', 'Brand', 'Product Name', 'Option', 'Price', 'Description', 'image_name1', 'image_name2', 'image_name3', 'image_name4', 'image_name5']
        writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

        writer.writeheader()

        page = 1
        product_count = 1
        while page <= max_page:
            print("Getting " + str(page) + " out of " + str(max_page))
            html = link + str(page)
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
            page += 1

getProductInfo("skincare", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=1&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=999&page=", 11)
getProductInfo("makeup", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=2&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=146&page=", 2)
getProductInfo("haircare", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=4&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=297&page=", 4)
getProductInfo("cologne", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=5&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=148&page=", 2)
getProductInfo("perfume", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=6&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=292&page=", 4)
getProductInfo("mens-skincare", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=21&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=90&page=", 1)
getProductInfo("home-scents", "https://hk.strawberrynet.com/ajaxProdList.aspx?catgid=16&brandid=0&typeid=0&funcid=0&lineid=0&groupid=0&sort=popularity&viewtype=grid&type=productlist&othcatgid=0&totalPage=13&page=", 1)
