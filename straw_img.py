import csv
from urllib.request import urlretrieve

def downloadImg(filename):
    imgs = []
    error = []
    with open(filename, newline='') as csvFile:
        csvReader = csv.reader(csvFile, delimiter='|')
        for row in csvReader:
            imgs += row

    for img in imgs:
        html = "https://simg1.strawberrynetmedia.com/images/products/l/" + img
        try:
            urlretrieve(html, img)
            print("Downloading Image " + str(imgs.index(img)+1) + " : " + img)
        except urllib.error.HTTPError:
            error.append(img)
    print(error)

downloadImg("cologne.csv")
downloadImg("haircare.csv")
downloadImg("home-scents.csv")
downloadImg("makeup.csv")
downloadImg("mens-skincare.csv")
downloadImg("perfume.csv")
downloadImg("skincare.csv")
