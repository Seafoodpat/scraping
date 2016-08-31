from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.hktvmall.com/hktv/en/fashion")
bsObj = BeautifulSoup(html)

main = bsObj.find("div", {"class": "subnav"}).find("ul").findAll("li")

for m in main:
    mainName = m.find("a").text.strip()
    print(mainName)
