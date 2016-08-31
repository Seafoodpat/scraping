import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

alphabet = 'abcdefghijklmnopqrstuvwxyz \'&'

html = urlopen("https://hk.strawberrynet.com/shop-by-brand/")
bsObj = BeautifulSoup(html)
brands = bsObj.findAll("div", {"class": "item"})

with open('brand.csv', 'w') as csvfile:
    fieldnames = ['Chinese', 'English']
    writer = csv.DictWriter(csvfile, delimiter='|', fieldnames=fieldnames)

    for brand in brands:
        title = brand.text.replace("\n", "")
        brand_eng = []
        brand_chi = []
        for c in title:
            if c.lower() in alphabet:
                brand_eng.append(c)
            else:
                brand_chi.append(c)

        print(''.join(brand_chi))
        print(''.join(brand_eng).title())
        writer.writerow({   'Chinese': ''.join(brand_chi),
                            'English': ''.join(brand_eng).title()})
