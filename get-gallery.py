import sys
import requests_html
import urllib #possible relative parsing option in future

webpage = sys.argv[1]
classname = sys.argv[2]

img_url_list = []
img_types = [".jpg",".png",".gif",".jpeg"]

session = requests_html.HTMLSession()
r = session.get(webpage)

img_elements=r.html.find("."+classname+" img")

for i in img_elements:
    pic = i.attrs["src"]
    if pic not in img_url_list:
        img_url_list.append(pic)

print(img_url_list)

for ind,val in enumerate(img_url_list):
    for i in img_types:
        if i in val:
            fname = str(ind)+i
            with open(fname,'wb') as f:
                try:
                    f.write(session.get(val).content)
                except Exception as e:
                    pass
