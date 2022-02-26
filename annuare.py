from ipaddress import AddressValueError
from os import link
import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Comment
import json
import googlemaps 

def extract_garde(url):
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    article=soup.find_all("table",{"class":"pharma_history"})
    tr=article[0].find_all('tr')
    k=tr[-1].find_all('td')[-1].text.replace('Garde ',"")
    return k
def extract_lat_long_via_address(address_or_zipcode,lien):
    lat=None
    lng=None
    gmaps_key = googlemaps.Client(key="AIzaSyB1HHWZSfNNL778mo6GlsBeYJ8HFm7ktuU")
    g = gmaps_key.geocode(address_or_zipcode)
    try:
        lat = g[0]
        lat=lat["geometry"]["location"]["lat"]
        lng = g[0]
        lng=lng["geometry"]["location"]["lng"]
        return str(lat)+','+str(lng)
    except IndexError:
        req=Request(lien, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup=BeautifulSoup(webpage,'lxml')
        adresse=soup.find_all("address")
        try:
            cord=adresse[0].a.get('href').replace("http://maps.google.com/maps?q=","")
        except:
            cord='1.11111111, 1.111111111'
        return cord
    
class pharmacie:

    def __init__(self,nom="",quartier="",adresse="",num="",cord='',lien=''):
        self.nom=nom
        self.adresse=adresse
        self.num=num
        self.cordonnee=cord
        self.quartier=quartier
        self.lien=lien
    def getNom(self):
        return self.nom
    def getAdresse(self):
        return self.adresse
    def getNum(self):
        return self.num
    def getCordonnee(self):
        return self.cordonnee
    def getlien(self):
        return self.lien
    def getQuartier(self):
        return self.quartier
    def __str__(self):
        return self.quartier+": ["+self.nom+", "+self.adresse+", "+self.num+", "+self.cordonnee+"],"

cle='AIzaSyBnN118yXQmI6PseuR6rsSRJNZCOkiNJKQ'
pharmacies=[]
for ville in open('href.txt','r'):
    req=Request("https://www.annuaire-gratuit.ma"+ville.replace('\n',''), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    article=soup.find_all("article")
    for a in article:
       if a.get('class')[1]!='column_in_pub':
        name=a.h3.text
        adresse=str(a.find_all('p',{'itemprop':'streetAddress'})[0].text)
        tel=a.find_all('span',{'itemprop':'telephone'})[0].a.get('href').replace('tel:',"")
        quartier=a.find_all('span',{'itemprop':'addressLocality'})[0].text
        try:
            ville=a.find_all('span',{'itemprop':'addressLocality'})[1].text
        except:
            ville=""
        lien="https://www.annuaire-gratuit.ma"+a.find_all('a',{'itemprop':'url'})[0].get('href')
        addlink=a.find_all('a',{'title':'Localiser'})[0].get('href').replace("http://maps.google.com/maps?q=","")
        cordonnee=extract_lat_long_via_address(ville+" "+quartier+" "+name,lien)
        etat=extract_garde(lien)
        pharmacies.append([name,lien,quartier,adresse,cordonnee,tel,etat,cle])
df2 = pd.DataFrame(pharmacies,columns=['pharmacie', 'lien', 'quartier','adresse','coordonnee','telephone','etat','cle'])
out="["+df2.to_json(orient='records')[1:-1].replace('},{', '},{')+"]"
output=open('data1.json', 'w')
with output as f:
    f.write(out)

