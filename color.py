import csv
from PIL import Image
from urllib.request import urlopen
import json


ids = [152497,
140015,
151739,
164423,
169624,
170698,
157852,
154561,
192740,
173510,
154033,
154566,
154459,
184124,
173509,
180133,
199983,
181948,
202442,
155493,
191821,
191515,
175389,
180170,
175594,
186437,
164420,
191828,
181919,
181955,
180172,
180131,
186877,
195846,
182805,
191569,
181958,
191070,
191463,
181824,
189047,
175590,
175593,
201285,
181825,
183273,
159553,
192574,
192576]
with open('color.csv', 'w') as csvfile:
    fieldnames = ['sku', 'Opt', 'color']
    writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

    writer.writeheader()

    for x in ids:
        productJSON = "https://hk.strawberrynet.com/ajaxProdDetail.aspx?ProdId=" + str(x) + "&CurrId=HKD"
        #productJSON = "https://hk.strawberrynet.com/ajaxProdDetail.aspx?ProdId=19679&CurrId=HKD"
        response = urlopen(productJSON).read().decode('utf-8')
        responseJson = json.loads(response)

        try:
            index = 0
            while index < len(responseJson.get("Prods")):
                if responseJson.get("Prods")[index].get("colorImg") != None or responseJson.get("Prods")[index].get("colorImg") != "":
                    optType = responseJson.get("Prods")[index].get("OptionType")
                    optValue = responseJson.get("Prods")[index].get("OptionValue")
                    option = optType + str(optValue)
                    link = responseJson.get("Prods")[index].get("colorImg")
                    im = Image.open(urlopen(link))
                    pix = im.load()
                    rgb = pix[im.size[0]/2,im.size[1]/2]
                    hexCode = "#%02x%02x%02x" % rgb
                    print(str(x) + option + ":" + hexCode)
                    writer.writerow({   'sku': x,
                                        'Opt': option,
                                        'color': hexCode})
                index += 1
        except ValueError:
            pass

#https://simg1.strawberrynetmedia.com/images/products/color/09689880102.jpg
