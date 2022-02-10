from ipaddress import AddressValueError
from os import link
import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Comment
import json


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


pharmacies=[]
for ville in open('href.txt','r'):
    print(ville)
    req=Request("https://www.annuaire-gratuit.ma"+ville.replace('\n',''), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    article=soup.find_all("article")
    for a in article:
       if a.get('class')[1]!='column_in_pub':
        name=a.h3.text
        adresse=a.find_all('p',{'itemprop':'streetAddress'})[0].text
        tel=a.find_all('span',{'itemprop':'telephone'})[0].a.get('href')
        quartier=a.find_all('span',{'itemprop':'addressLocality'})[0].text
        lien="https://www.annuaire-gratuit.ma"+a.find_all('a',{'itemprop':'url'})[0].get('href')
        
        req=Request(lien, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup=BeautifulSoup(webpage,'lxml')
        loc=soup.find_all("a",{'title':'Localiser'})
        if len(loc)!=0:
            loc=loc[0].get('href')
            try:
                cordonnee=loc.replace("http://maps.google.com/maps?q=","")
                x=cordonnee.find(',')
                b=float(cordonnee[:x])
            except:
                cordonnee=''    
        else :
            loc=''
        print(name+"==========>"+cordonnee)

        pharmacies.append([name,lien,quartier,adresse,cordonnee,tel])
df2 = pd.DataFrame(pharmacies,columns=['pharmacie', 'lien', 'quartier','adresse','coordonnee','telephone'])
out="["+df2.to_json(orient='records')[1:-1].replace('},{', '},{')+"]"
print(out)
output=open('data1.json', 'w')
with output as f:
    f.write(out)
