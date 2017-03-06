import requests
from lxml import html

page = requests.get('https://www.google.ru/#newwindow=1&q=Toyota&*')
tree = html.fromstring(page.content)

buyers = tree.xpath('.//*[@id="rso"]/div[1]/div/div/h3/a')

print 'Link:', buyers
