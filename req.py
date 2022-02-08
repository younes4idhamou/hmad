from ipaddress import AddressValueError
from os import link
import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Comment
import json


class pharmacie:

    def __init__(self,nom="",ville="",adresse="",num="",cord=''):
        self.nom=nom
        self.adresse=adresse
        self.num=num
        self.cordonnee=cord
        self.ville=ville
    def getNom(self):
        return self.nom
    def getAdresse(self):
        return self.adresse
    def getNum(self):
        return self.num
    def getCordonnee(self):
        return self.cordonnee
    def getVille(self):
        return self.ville
    def __str__(self):
        return self.ville+": ["+self.nom+", "+self.adresse+", "+self.num+", "+self.cordonnee+"],"
    
pharmacies=[]
for ville in open('villes.txt','r'):
    print(ville.replace('\n','')+":")
    req=Request("https://www.telecontact.ma/services/pharmacies-de-garde/"+ville.replace('\n','')+"-Maroc", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    article=soup.find_all("article")
    for a in article:
        page=a.find_all('div',{'class':'btn-results-right'})
        if len(page)!=0:
            link=page[0].a.get('href')
            req=Request('https://www.telecontact.ma'+link, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup=BeautifulSoup(webpage,'html.parser')
            comment = soup.find(text=lambda text:isinstance(text, Comment))
        else:
            comment=''
        
        pharmacies.append([ville.replace('\n',''),a.a.text,a.find_all('span',{'itemprop':'streetAddress'})[0].span.text[2:],a.find_all('div',{'class':'tel'})[0].text[2:],comment])
df2 = pd.DataFrame(pharmacies,columns=['ville', 'nom', 'adresse','tel','cordonnee'])
out=df2.to_json(orient='records')[1:-1].replace('},{', '} {')
output=open('data.json', 'w')
output.write("[")
with output as f:
    f.write(out)
output=open('data.json', 'a').write("]")
print(output)
