from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup

link = "https://www.amazon.com/GNC-Herbal-Plus-Bilberry-Capsules/dp/B00MG8S448/ref=sr_1_4_s_it?s=hpc&ie=UTF8&qid=1469604452&sr=1-4&keywords=gnc+lutein"
html = requests.get(link)
bsObj = BeautifulSoup(html.text)

imgs = bsObj.findAll("span", {"class": "a-list-item"})
print(bsObj)

'''
for img in imgs:
      html = "https://simg1.strawberrynetmedia.com/images/products/l/" + img
      try:
          urlretrieve(html, img)
          print("Downloading Image " + str(imgs.index(img)+1) + " : " + img)
      except urllib.error.HTTPError:
          error.append(img)
  print(error)
'''
