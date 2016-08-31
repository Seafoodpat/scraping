from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.sasa.com/")
bsObj = BeautifulSoup(html)

topBarItems = bsObj.findAll("div", {"class": "cat-text"})

firstLv = []
firstLvUrl = []
for item in topBarItems:
    firstLv.append(item.text)
    href = item.find("a").get('href')
    if not 'javascript' in href:
        firstLvUrl.append("http://www.sasa.com" + href)

print(firstLv)
print(firstLvUrl)

bsObjLv2 = BeautifulSoup(urlopen(firstLvUrl[0]))
sub = bsObjLv2.findAll("ul", {"class": "l_btwo"})
subcate = []
for s in sub:
    subcate.append(s.text.replace("\n", ""))

print(subcate)
