import folium # Map Module
from folium import plugins, GeoJson, IFrame # Required data in the Map Module
import pandas as pd # Module for Reading Excel File
from folium.plugins import MarkerCluster, MeasureControl
import requests
import json
import re

map_1 = folium.Map(location=[38.291916, 37.10466], zoom_start=6) # Map Start Position And Zoom There Scale

nufus=pd.read_excel(r"2021.xls") # 2021 Turkey Population Distribution by Provinces

geo=r"tr-cities.json" # json file with Provincial Coordinates of Turkey Map
file = open(geo, encoding="utf8")
text = file.read()

nufus.loc[nufus["Sehir"]=="Afyonkarahisar","Sehir"]="Afyon" # We changed the name of Afyonkarahisar in the text file to Afyon.

nufus.head()

r"""
def havaDurumu(self):
    city = self
    apiKey = ''
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}')
    weatherData = response.json()
    
    skyDescription = weatherData['weather'][0]['description']
    cityName = weatherData['name']
    skyTypes = ['clear sky', 'few clouds','overcast clouds', 'scattered clouds', 'broken clouds', 'shower rain', 'rain', 'thunderstorm','snow','mist']
    skyTypesTR = ['Güneşli', 'Az Bulutlu','Çok Bulutlu(Kapalı)', 'Alçak Bulutlu', 'Yer Yer Açık Bulutlu', 'Sağanak Yağmurlu', 'Yağmurlu', 'Gök Gürültülü Fırtına', 'Karlı', 'Puslu']
    for i in range(len(skyTypes)):
        if skyDescription == skyTypes[i]:
            skyDescription = skyTypesTR[i]

    temp = round((weatherData['main']['temp'] - 273.15), 2) #Genel sıcaklık
    feels_temp = round((weatherData['main']['feels_like'] - 273.15), 2) #hissedilen
    temp_min = round((weatherData['main']['temp_min'] - 273.15), 2) #Minimum
    temp_max = round((weatherData['main']['temp_max'] - 273.15), 2) #Maksimum

    havadurumudict = {
        "Şehir": cityName,
        "Gökyüzü": skyDescription,
        "Sıcaklık": temp,
        "Hissedilen": feels_temp,
        "Minimum": temp_min,
        "Maksimum": temp_max
    }

    return temp

with open('tr-cities.json', 'r', encoding='utf8') as f:
    json_data2 = json.load(f)
with open('temp.json', 'r', encoding='utf8') as f:
    json_data = json.load(f)
    for r in json_data:
        json_data2[r] = havaDurumu(r)

with open('tr-cities.json', 'w', encoding='utf8') as f:
    json.dump(json_data2, f)

"""

def TurkeycolorPicker(population):
    population = population.replace(' ','')
    population = int(population)
    if population < 200000:
        return 'green'
    elif population < 500000:
        return 'blue'
    elif population < 700000:
        return '#ffff00'
    elif population >= 700000 and population < 10000000:
        return '#ee7600'
    else:
        return '#ff0000'
    
GeoJson(text, name="Turkey Population", 
        style_function = lambda x: {'fillColor': TurkeycolorPicker(x['properties']['population'])},
        tooltip=folium.features.GeoJsonTooltip(
        fields=['number', 'population', 'temp'],
        aliases=['Plate Code:', 'Population:', 'Sıcaklık'], 
        labels=True, 
        sticky=True,
        toLocaleString=True
    ),show=False).add_to(map_1) # Adding Turkey's Borders to the Map.

def CountrycolorPicker(population):
    if population < 10000000:
        return 'green'
    elif population >= 10000000 and population < 500000000:
        return 'orange'
    else:
        return 'red'

folium.GeoJson(open('population.json', 'r', encoding='utf-8-sig').read(),
               name = 'Country Population',
               style_function = lambda x: {'fillColor': CountrycolorPicker(x['properties']['POP2005'])},
               tooltip = folium.GeoJsonTooltip(fields=('NAME', 'POP2005','Capital'),
                                               aliases=('Country','Population','Capital')),
               show = False).add_to(map_1)

mCluster_ele = MarkerCluster(name="Places to visit",show=False).add_to(map_1)

places = [(41.00856677915877, 28.9799818762614, 'Ayasofya Mosque','Places to visit', '', 'Ayasofya, formerly known as the Holy Wisdom Church and Ayasofya Museum, or today officially known as Ayasofya, is a mosque and former basilica, cathedral and museum located in Istanbul.'),
             (41.00656374582111, 28.975452183338238, 'Sultan Ahmet Mosque','Places to visit', '', 'Sultan Ahmet Mosque or Sultanahmed Mosque was built by the Ottoman Sultan Ahmed I between 1609 and 1617 on the historical peninsula in Istanbul, by the architect Sedefkar Mehmed Ağa.'),
             (41.03922764134289, 28.999531155758138, 'Dolmabahçe Palace','Places to visit', '', 'Dolmabahçe Palace is an Ottoman palace located on an area of 250.000 m² in Istanbul, Beşiktaş, between Dolmabahçe Street stretching from Kabataş to Beşiktaş and the Bosphorus.'),
             (41.01138103877113, 28.967596031268627, 'Grand Bazaar','Places to visit', '', 'The Grand Bazaar, located in the center of Istanbul, in the middle of Beyazıt, Nuruosmaniye and Mercan districts, is the worlds largest bazaar and one of the oldest covered bazaars. There are approximately 4,000 shops in the Grand Bazaar and the total number of employees in these shops is approximately 25,000.'),
             (41.10518882262468, 29.053135729192302, 'Emirgan district','Places to visit', '', 'Emirgan Grove is a horror located in the Emirgan district of Sarıyer district of Istanbul. It is spread over ridges and slopes on an area of 47.2 hectares on the shores of the Bosphorus.'),
             (41.02569038143965, 28.974107139165014, 'Galata tower','Places to visit', '', 'The Galata Tower, or the Galata Tower Museum, as it was called after it began to be used as a museum, is a tower located in the Beyoğlu district of Istanbul. It takes its name from the Galata district where it is located.'),
             (41.08489725896427, 29.056600153047246, 'Rumeli Fortress','Places to visit', '', 'Rumeli Fortress is the fortress located on the Bosphorus in the Sarıyer district of Istanbul, giving its name to the district it is located in.'),
             (41.05908551782065, 28.94924375819267, 'Miniatürk','Places to visit', '', 'Miniatürk or Miniature Turkey Park is the worlds largest miniature park, located on an area of 60,000 square meters in Beyoğlu, Istanbul, where models of various works in Turkey are exhibited. It is located in an old park area on the shore of the Golden Horn.'),
             (41.022064574496866, 29.00348801333903, 'Maidens Tower','Places to visit', 'https://i.sozcucdn.com/wp-content/uploads/2022/12/31/thumbs_b_c_fab7c43a6321040f570495d797829430-1.jpeg?w=210&h=130&mode=crop&scale=both', 'The Maidens Tower was built on a small islet off the coast of Salacak, close to the Sea of Marmara in the Bosphorus.'),
             (41.04268422587759, 28.94916213916554, 'Rahmi M. Koç Museum','Places to visit', '', 'Rahmi M. Koç Museum is an industrial museum in the Hasköy district of Istanbul, on the shores of the Golden Horn. The museum, which was opened in 1994 with the support of businessman Rahmi Koç, is the first important museum in Turkey dedicated to the history of industry, transportation, industry and communication.'),
             (41.013437399548934, 28.981456452660037, 'Gulhane Park','Places to visit', '', 'Gülhane Park is a historical park located in the Eminönü district of Fatih district of Istanbul. Alay Mansion is located between Topkapi Palace and Sarayburnu.'),
             (40.99052415961625, 29.02912838149403, 'Kadıköy Bull Statue','Places to visit', 'https://media.discordapp.net/attachments/953746693403320391/1113964755984584724/indir_1.png', 'The area where this bronze bull statue is a symbol of the Asian side of the city is a popular meeting point.')]

df = pd.DataFrame(places, columns=['LAT','LNG','NAME','CATEGORY', 'IMAGE','DESCRIPTION'])

for row in df.itertuples():
    #print(row)
    location = row[1], row[2]
    icon=folium.Icon(color='orange', icon='map-pin', prefix='fa')
    html = '''NAME: ''' + row[3] + '''<br>CATEGORY: ''' + row[4] + f'<img src="{row[5]}">' + row[6]
    iframe = folium.IFrame(html, width=260, height=200)
    popup = folium.Popup(iframe, max_width=260)
    marker = folium.Marker(location=location, popup=popup, icon=icon)
    if row[4] == 'Places to visit':
        mCluster_ele.add_child(marker)       


mCluster_ele2 = MarkerCluster(name="UNESCO world cultural heritage ",show=False).add_to(map_1)

places2 = [(39.37120967499756, 38.12171189677295, 'Divriği Great Mosque and hospice','UNESCO world cultural heritage', ''),
             (40.01594376292911, 34.61542305666845, 'Hattusa (Boğazköy) - Hittite Capital','UNESCO world cultural heritage', ''),
             (38.06413753620966, 38.74931670547676, 'Nemrut Mountain','UNESCO world cultural heritage', ''),
             (36.332056732994005, 29.289668552492145, 'Xanthos-Letoon ','UNESCO world cultural heritage', ''),
             (41.249614135343016, 32.68319543075201, 'Safranbolu City','UNESCO world cultural heritage', ''),
             (39.95770850556383, 26.23972926795965, 'Troy Ancient City','UNESCO world cultural heritage', ''),
             (41.678182729993395, 26.559197950314836, 'Edirne Selimiye Mosque','UNESCO world cultural heritage', ''),
             (37.666509368112884, 32.82574572829293, 'Çatalhöyük Neolithic City','UNESCO world cultural heritage', ''),
             (39.11848775904674, 27.17739025128647, 'Bergama Multilayered Cultural Landscape Area','UNESCO world cultural heritage', ''),
             (40.1780927518229, 29.169384767346106, 'Bursa and Cumalıkızık','UNESCO world cultural heritage', ''),
             (37.923101990760856, 40.258642048224715, 'Diyarbakir Castle and Hevsel Gardens','UNESCO world cultural heritage', ''),
             (37.940993889540195, 27.341597354853594, 'Efes ','UNESCO world cultural heritage', ''),
             (40.50619921916537, 43.57254301564587, 'Ani Archaeological Site','UNESCO world cultural heritage', ''),
             (37.712745151254516, 28.730059710650192, 'Afrodisias','UNESCO world cultural heritage', ''),
             (37.223294420255364, 38.922336794852946, 'Göbeklitepe','UNESCO world cultural heritage', ''),
             (38.381248195503076, 38.360935704701944, 'Arslantepe','UNESCO world cultural heritage', ''),
             (38.64375889598977, 34.82906061292531, 'Göreme National Park and Cappadocia','UNESCO world cultural heritage', ''),
             (37.915487140130864, 29.117540081660625, 'Pamukkale-Hierapolis','UNESCO world cultural heritage', '')]

df2 = pd.DataFrame(places2, columns=['LAT','LNG','NAME','CATEGORY', 'IMAGE'])

for row2 in df2.itertuples():
    #print(row2)
    location = row2[1], row2[2]
    icon=folium.Icon(color='purple', icon='map-pin', prefix='fa')
    html = '''NAME: ''' + row2[3] + '''<br>CATEGORY: ''' + row2[4] + f'<img src="{row2[5]}">'
    iframe = folium.IFrame(html, width=260, height=200)
    popup = folium.Popup(iframe, max_width=260)
    marker = folium.Marker(location=location, popup=popup, icon=icon)
    if row2[4] == 'UNESCO world cultural heritage':
        mCluster_ele2.add_child(marker)       


Earthquake_ele2 = MarkerCluster(name="Earthquake ",show=False).add_to(map_1)

with open('earthquake.json') as dosya:
    veriler = json.load(dosya)

for item in veriler:
    #print("ID:", item["ID"])
    #print("Time:", item["Time"])
    #print("Latitude:", item["Latitude"])
    #print("Longitude:", item["Longitude"])
    #print("Depth:", item["Depth"])
    #print("Region:", item["Region"])

    lat = re.sub(r'[^\d.]', '', item["Latitude"])
    long = re.sub(r'[^\d.]', '', item["Longitude"])
    
    location = lat, long
    icon=folium.Icon(color='purple', icon='house-crack', prefix='fa')
    html = f'''Earthquake ID: {item["ID"]} <br>Region: ''' + item["Region"] + f'''<br>Magnitude:  {item["Magnitude"]} ''' + f'''<br>Time:  {item["Time"]} <br>Depth: {item["Depth"]} ''' 
    iframe = folium.IFrame(html, width=260, height=200)
    popup = folium.Popup(iframe, max_width=260)
    marker = folium.Marker(location=location, popup=popup, icon=icon)
    Earthquake_ele2.add_child(marker)       

folium.TileLayer('cartodbdark_matter').add_to(map_1)

minimap = plugins.MiniMap() # Creating a Minimap
map_1.add_child(minimap) # Integrating a Mini Map in Our Map 

plugins.Geocoder().add_to(map_1)

base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
gy = folium.TileLayer(tiles='OpenStreetMap')
gy.add_to(base_map)
base_map.add_to(map_1)

folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='Satellite',
    name='Satellite',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(map_1)

def on_map_click(event):
    lat, lon = event.latlng
    marker = folium.Marker([lat, lon])
    marker.add_to(map_1)

map_1.add_child(folium.LatLngPopup()) # Bind the click event to the map
map_1.add_child(folium.ClickForMarker(popup=None))

folium.LayerControl().add_to(map_1) # Population Distribution

folium.plugins.MousePosition().add_to(map_1)

map_1.save("map3.html") # Creating a Map