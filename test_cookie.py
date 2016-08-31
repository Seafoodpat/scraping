import urllib
import http.cookiejar

cookie = http.cookiejar.CookieJar()

handler=urllib.request.HTTPCookieProcessor(cookie)

opener = urllib.request.build_opener(handler)

response = opener.open('http://www.iherb.cn/Doctor-s-Best?noi=192/')
for item in cookie:
    print('Name = '+item.name)
    print('Value = '+item.value)
