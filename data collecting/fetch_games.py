import requests
import json


session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'})

api_key = '43cc9ef1247b109ad02c635466113bfe763b109b'

count = 0
offset = 100
for x in range(450):
    count = count + offset
    response = session.get(
        'https://www.giantbomb.com/api/games/?api_key=43cc9ef1247b109ad02c635466113bfe763b109b&format=json&sort=date_added:desc&offset='+str(x*offset+29900))
    filename = str(x+300)+'.json'
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(json.JSONDecoder().decode(response.content.decode("utf-8")), outfile, indent=4, separators=(',', ': '))
