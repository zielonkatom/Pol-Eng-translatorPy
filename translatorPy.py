from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
from introLogoTranslator import logo

def link(word):
    url = "https://pl.bab.la/slownik/angielski-polski/{}".format(word)
    return url

def reqPage(url):
    '''
    Permission problems, need to change agent. Python's default agent is easily detectable. 
    '''
    req = Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req

logo()

reHref = re.compile(r'href="/slownik/polski-angielski/')

while True:
    toBeTrans = input("""By default it is English - > Polish.
If you wish to change the order input "lang".
What do you want to translate?\n""").strip()
    if toBeTrans =="lang":
        print("Changing translation order".center(45, "."))
        lang = input("""1: Polish -> English
2: English -> Polish\n""")
        if lang == "1":
            reHref = re.compile(r'href="/slownik/angielski-polski/')
        else:
            reHref = re.compile(r'href="/slownik/polski-angielski/')
        print(".")
        print(".")
        print("Changed..")
        print("".center(45, "."))
        toBeTrans = input("\nWhat do you want to translate?\n").strip()
        
    if toBeTrans == "":
        break
    toBeTransSplit = toBeTrans.split(" ")

    for word in toBeTransSplit:
        indexes = []
        url = link(word)
        f = urlopen(url).read()
        soup = BeautifulSoup(f, features="lxml")
        search = soup.find_all("a", attrs={"title":True, "href":True})
        for item in search:
            mo = reHref.search(str(item))
            if mo != None:
                indexes.append(search.index(item))
        print("\nWord \"{}\" can be translated to:\n".format(word))
        for i in indexes:
            if indexes.index(i)%2 == 0:
                print("-".rjust(6) + search[i].getText().ljust(25), end=" ")
            else:
                print("-".rjust(6) + search[i].getText().ljust(25), end="\n")


    print("\nAnything else?")
