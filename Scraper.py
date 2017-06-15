from bs4 import BeautifulSoup
from urllib.request import urlopen



def download_coins(urls):

    coins = dict()
    for i in urls:
        response = urlopen(i)
        html     = response.read()
        soup     = BeautifulSoup(html,"html.parser")
        for link in soup.find_all('a'):
            #print(link.get('href'))
            string = link.get("href")
            if "coins" in string:
                try:
                    coin = string.split("/")[-1]
                    name = link.parent.findNext("td").contents[0]
                    if "<" not in str(coin)+str(name) and "info" not in str(coin)+str(name):
                        coins[name.lower()] = coin.lower()
                    
                except:
                    break
                
    return coins

#coins = download_coins(urls)
"""
#Write down all the symbols and names of cryptos in csv file
with open("crypto.txt", "w") as f:
    for i,j in coins.items():
        f.write(i.lower()+", "+j.lower()+"\n")

"""
