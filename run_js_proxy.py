import requests
from bs4 import BeautifulSoup
import random

# for rendering the javascript
import execjs


res = requests.get('https://www.proxynova.com/proxy-server-list/country-ph/')
soup = BeautifulSoup(res.content, "html.parser")

proxies  = []
for row in soup.select("table#tbl_proxy_list tbody tr"): 
    r = execjs.compile(row.select_one("td script").text.replace('document.write', 'var result = '))
    
    proxies.append(f'{r.eval("result")}:{int(row.select("td")[1].text)}')
    print(proxies[-1])



def scraping_request(url):
    ip = random.choice(proxies)
    try:
        response = requests.get(url, proxies={"http": ip, "https": ip})
        if response.status_code == 200:
            print(f"Proxy currently being used: {ip}")

        return response.json()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


scraping_request("http://www.wikipedia.com")

