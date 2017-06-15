from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from Scraper import download_coins
import time
import re
import operator
#"https://www.cryptocoincharts.info/coins/info/1001"
urls = ["https://www.cryptocoincharts.info/coins/info",
        "https://www.cryptocoincharts.info/coins/info/101-to-1000"]

req = Request("http://boards.4chan.org/biz/catalog", headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
titles = []
tits = webpage.decode("utf8").split("\"")[:-1]

for i,t in enumerate(tits):
    if t == "sub":
        if tits[i+2] != "":
            titles.append(tits[i+2].replace("&#039;","\'").replace("\/","/"))
        else:
            titles.append("teaser: "+tits[i+6].replace("&#039;","\'").replace("\/","/").replace("&gt;",">"))



a =""
thread_numbers = []
img_count = []
b=0
for i in webpage.decode("utf8").split(":"):
    if '{"date"' in i:
        thread_numbers.append(a.split(",")[-1])
    if b == 1:
        img_count.append(int(i.split(",")[0]))
        b=0

    if '"i"' in i:
        b = 1

    a = i
all_urls = []    
for i,x in enumerate(thread_numbers):
    all_urls.append("http://boards.4chan.org/biz/thread/"+x.strip('"{'))
    #print("http://boards.4chan.org/biz/thread/"+x.strip('"'),titles[i], "\n Image count: ", img_count[i])
print(len(thread_numbers),len(titles), len(img_count))

coins = download_coins(urls)
list_coins=dict()
for i in all_urls:
    print("Searching in " + i)
    #time.sleep(1)
    req = Request(i, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup     = BeautifulSoup(webpage,"html.parser")

    for text in soup.find_all("blockquote"):
        t = text.text.lower()
        for name,symbol in coins.items():
            num = len(re.findall(name+" ", t))
            num2 = len(re.findall(" "+symbol+" ", t))
            if (num > 0 or num2 > 0):
                if name not in list_coins.keys():
                    list_coins[name] = num+num2
                else:
                    list_coins[name] += num+num2
                #if len(name) <= 3 :
                    #list_coins[name] /= 10
    print("Best ones so far: \n")
    for i,j in sorted(dict(sorted(list_coins.items(), key=operator.itemgetter(1), reverse=True)[:30]).items(), key = operator.itemgetter(1)):
        print(i,j)
    print("\n\n\n\n")
            
        
    
    
