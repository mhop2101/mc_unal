from bs4 import BeautifulSoup
from pandas import read_csv
import googlemaps
import openpyxl
import requests
import random
import json
import xlwt
import os

class ScrapeDetails():

    def __init__(self,LOG_FOLDER,headers,frame,geocoding):

        #Log folder path instance
        self.LOG_FOLDER = LOG_FOLDER

        # Headers instance
        self.headers = headers

        # Set googlemaps api
        self.gmaps = googlemaps.Client(key='AIzaSyCuORg0sZFB_hEBVrNPieRnLgqyA8jrlIw')

        # Set the dataframe instance
        self.df = read_csv(frame)

        try:
            self.df = self.df.drop(['Unnamed: 0'],axis=1)
        except:
             pass

        # Set geocoding
        self.geocoding = geocoding


    def GetDetails(self,url):
        request = requests.get(url, headers=random.choice(self.headers))
        content = request.content
        soup = BeautifulSoup(content,"html.parser")
        title_container = soup.find("h1",{"class":"H1-xsrgru-0 jdfXCo mb-2 card-title"})
        upper_details_container = soup.select('div.Card-sc-18qyd5o-0.gWLCMY.sc-eqIVtm.kXSKZs.sc-cHGsZl.jfOGar')[0].find_all("h2",class_='H2-kplljn-0')
        lower_details_container = soup.select('div.Card-sc-18qyd5o-0.gWLCMY.sc-eqIVtm.kXSKZs.sc-kjoXOD')[0].find_all("div",{"class":"Col-sc-14ninbu-0"})
        try:
            characteristics_container = soup.select('div.Card-sc-18qyd5o-0.gWLCMY.sc-eqIVtm.kXSKZs.sc-cJSrbW.kSOVev.featureacordion')[0].find_all("div",{"class":"Card-sc-18qyd5o-0"})
            characteristics = True
        except:
            try:
                characteristics_container = soup.select("div.Card-sc-18qyd5o-0.gWLCMY.sc-eqIVtm.kXSKZs.sc-cJSrbW.kSOVev.mb-5.sc-cJSrbW.kSOVev.mb-5.card-features.card")[0].find_all("div",{"class":"Card-sc-18qyd5o-0"})
                characteristics = True
            except:
                characteristics = True





        json_container = soup.find("script",{"id":"__NEXT_DATA__"})
        coordinates = json.loads(str(json_container).replace("</script>","").replace('<script id="__NEXT_DATA__" type="application/json">',""))
        interior_char = ''
        exterior_char = ''
        zone_char = ''
        sector_char = ''



        address = str()
        proyect = False

        # Determine dwether the current listing is a proyect
        if 'Proyecto' in title_container.text:
            proyect = True

        # Extract the listing's title
        try:
            title = title_container.text
            if proyect:
                title = 'PROYECTO '+title
        except:
            title = ''

        # extract the bath_count
        try:
            baths = ''
            for detail in upper_details_container:
                try:
                    if "Baños" in detail.text.replace("\n",'').replace('\t','').replace(' ',''):
                        baths = detail.text.replace("\n",'').replace('\t','').replace(' ','').replace("Baños",'').replace('A','-')
                        break
                except:
                    pass
        except:
            baths = ''

        # extract the garages_count
        try:
            garages = ''
            for detail in upper_details_container:
                try:
                    if "Parqueaderos" in detail.text.replace("\n",'').replace('\t','').replace(' ',''):
                        garages = detail.text.replace("\n",'').replace('\t','').replace(' ','').replace("Parqueaderos",'').replace('A','-')
                        break
                except:
                    pass
        except:
            garages = ''

        if garages == '':
            # Extract the garages from the bottom
            try:
                garages = ''
                for detail in lower_details_container:
                    try:
                        if detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ','') == "Parqueaderos":
                            garages = detail.find("p").text.replace("\n",'').replace('\t','').replace(' ','')
                            break
                    except:
                         pass
            except:
                garages = ''


        # extract the area
        try:
            area = ''
            for detail in upper_details_container:
                try:
                    if "Áreaconstruida" in detail.text.replace("\n",'').replace('\t','').replace(' ',''):
                        area = detail.text.replace("\n",'').replace('\t','').replace(' ','').replace("Áreaconstruida",'').replace("m²",'').replace('Desde-Hasta','')
                        break
                except:
                    pass
        except:
            area = ''

        # extract the room_no
        try:
            rooms = ''
            for detail in upper_details_container:
                try:
                    if "Habitaciones" in detail.text.replace("\n",'').replace('\t','').replace(' ',''):
                        rooms = detail.text.replace("\n",'').replace('\t','').replace(' ','').replace("Habitaciones",'').replace('A','-')
                        break
                except:
                    pass
        except:
            rooms = ''

        # extract the social_status
        try:
            status = ''
            for detail in upper_details_container:
                try:
                    if "Estrato" in detail.text.replace("\n",'').replace('\t','').replace(' ',''):
                        status = detail.text.replace("\n",'').replace('\t','').replace(' ','').replace('Estrato','')
                        break
                except:
                    pass
        except:
            status = ''

        # Extract the 'barrio catastral'
        try:
            true_hood = ''
            for detail in lower_details_container:
                try:
                    if detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ','') == "Barriocatastral":
                        true_hood = detail.find("p").text.replace("\n",'').replace('\t','')
                        break
                except:
                     pass
        except:
            true_hood = ''

        # Extract the 'barrio catastral'
        try:
            hood = ''
            for detail in lower_details_container:
                try:
                    if detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ','') == "Barriocomún":
                        hood = detail.find("p").text.replace("\n",'').replace('\t','')
                        break
                except:
                     pass
        except:
            hood = ''

        # Extract the priv_area
        try:
            priv_area = ''
            for detail in lower_details_container:
                try:
                    if "Áreaprivada" in detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ',''):
                        priv_area = detail.find("p").text.replace("\n",'').replace('\t','').replace("m²",'').replace('/','-')
                        break
                except:
                     pass
        except:
            priv_area = ''

        # Extract the antiqueness
        try:
            antiqueness = ''
            for detail in lower_details_container:
                try:
                    if "Antigüedad" in detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ',''):
                        antiqueness = detail.find("p").text.replace("\n",'').replace('\t','')
                        break
                except:
                     pass
        except:
            antiqueness = ''

        # Extract the price
        try:
            price = ''
            for detail in lower_details_container:
                try:
                    if "Precio" in detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ',''):
                        price = detail.find("p").text.replace("\n",'').replace('\t','').replace('/','-')
                        break
                except:
                     pass
        except:
            price = ''

        # Extract the price
        try:
            lease = ''
            for detail in lower_details_container:
                try:
                    if "arriendo" in detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ',''):
                        lease = detail.find("p").text.replace("\n",'').replace('\t','').replace('/','-')
                        break
                except:
                     pass
        except:
            lease = ''

        # extract webcode
        try:
            webcode = ''
            for detail in lower_details_container:
                try:
                    if "inmueble" in detail.find("h3").text.replace("\n",'').replace('\t','').replace(' ',''):
                        webcode = detail.find("p").text.replace("\n",'').replace('\t','').replace('/','-')
                        break
                except:
                     pass
        except:
            webcode = ''

        try:
            longitude = coordinates['props']['initialState']['realestate']['basic']['coordinates']['lon']
            latitude = coordinates['props']['initialState']['realestate']['basic']['coordinates']['lat']
        except:
            longitude = ''
            latitude = ''


        # Get the address only if there are current long and lat values
        if longitude == '':
            address == ''
        else:
            if self.geocoding == True:
                try:
                    reverse_geocode_result = self.gmaps.reverse_geocode((float(latitude), float(longitude)))
                    address = reverse_geocode_result[0]['formatted_address']
                except:
                    address = ''
            else:
                address = ''

        if characteristics:
            for characteristic in characteristics_container:
                if characteristic.find('span').text == 'Interiores':
                    values = characteristic.find_all('p')
                    for value in values :
                        interior_char += value.text + '@'
                if characteristic.find('span').text == 'Exteriores':
                    values = characteristic.find_all('p')
                    for value in values :
                        exterior_char += value.text + '@'
                if characteristic.find('span').text == 'Zonas comunes':
                    values = characteristic.find_all('p')
                    for value in values :
                        zone_char += value.text + '@'
                if characteristic.find('span').text == 'Del sector':
                    values = characteristic.find_all('p')
                    for value in values :
                        sector_char += value.text + '@'
        else:
            sector_char = ""
            zone_char = ""
            exterior_char = ""
            interior_char = ""

        # append the record and write to the file
        self.df.loc[len(self.df)] = [webcode,title,hood,true_hood,price,lease,area,priv_area,status,rooms,garages,baths,antiqueness,interior_char,exterior_char,zone_char,sector_char,longitude,latitude,address,url]
        self.df.to_csv(os.path.join(self.LOG_FOLDER,'frame.csv'))
