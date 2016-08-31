from PIL import Image
from urllib.request import urlopen

link = input('Input the img url: ')
im = Image.open(urlopen(link))
pix = im.load()
rgb = pix[im.size[0]/2,im.size[1]/2]
hexCode = "#%02x%02x%02x" % rgb
print(hexCode)


#https://simg1.strawberrynetmedia.com/images/products/color/09689880102.jpg
