from ipaddress import AddressValueError
from os import link
import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Comment
import json

def extract_garde(url):
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'lxml')
    article=soup.find_all("table",{"class":"pharma_history"})
    tr=article[0].find_all('tr')
    k=tr[-1].find_all('td')[-1].text.replace('Garde ',"")
    return k



def extract_lat_long_via_address(address_or_zipcode,url):
    lat=None
    lng=None
    api_key = 'AIzaSyB1HHWZSfNNL778mo6GlsBeYJ8HFm7ktuU' 
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup=BeautifulSoup(webpage,'lxml')
        adresse=soup.find_all("address")
        cord=adresse[0].a.get('href').replace("http://maps.google.com/maps?q=","")
        try:
            b=float(cord[0:cord.find(",")])
            print(cord)
            return str(cord)
        except:
            return "0.00000, 0.000000"
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return str(lat)+", "+str(lng)

    
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
        adresse=a.find_all('p',{'itemprop':'streetAddress'})[0].text
        tel=a.find_all('span',{'itemprop':'telephone'})[0].a.get('href').replace('tel:',"")
        quartier=a.find_all('span',{'itemprop':'addressLocality'})[0].text
        lien="https://www.annuaire-gratuit.ma"+a.find_all('a',{'itemprop':'url'})[0].get('href')
        cordonnee=extract_lat_long_via_address(name,lien)
        etat=extract_garde(lien)
        if cordonnee!="0.00000, 0.000000":
            if cordonnee!="None, None":
                pharmacies.append([name,lien,quartier,adresse,cordonnee,tel,etat,cle])
            else:
                 req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                 webpage = urlopen(req).read()
                 soup=BeautifulSoup(webpage,'lxml')
                 adresse=soup.find_all("address")
                 cord=adresse[0].a.get('href').replace("http://maps.google.com/maps?q=","")
                 try:
                    b=float(cord[0:cord.find(",")])
                    print(cord)
                    pharmacies.append([name,lien,quartier,adresse,cord,tel,etat,cle])
                 except:
                    pharmacies.append([name,lien,quartier,adresse,"0.00000, 0.000000",tel,etat,cle])
            
        else:
            print('hello')
df2 = pd.DataFrame(pharmacies,columns=['pharmacie', 'lien', 'quartier','adresse','coordonnee','telephone','etat','cle'])
out="["+df2.to_json(orient='records')[1:-1].replace('},{', '},{')+"]"
output=open('data1.json', 'w')
with output as f:
    f.write(out)

