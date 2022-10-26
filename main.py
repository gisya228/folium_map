import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

# generate map of Russia
russia_map = folium.Map(
    location = [64.6863136, 97.7453061],    # широта и долгота России
    zoom_start = 4
)

data = pd.read_csv('postomaty_pendosy.txt')
lat = data['LAT']
lon = data['LON']
loc = data['LOCATION']

russia_map = folium.Map(location=[48.1118011,-121.1110001], zoom_start = 6,tiles='Stamen Terrain')

for lat, lon, loc in zip(lat, lon, loc):
    folium.Marker(location=[lat,lon], popup = str(loc), icon=folium.Icon(color = 'gray')).add_to(russia_map)
    folium.CircleMarker(
    location=[lat, lon],
    radius=175,
    popup="зона покрытия постамата",
    color="#3186cc",
    fill=True,
    fill_color="#3186cc",
).add_to(russia_map)       # добавили окружность
# add a red marker to Saint Petersburg
# create a feature group
saint_petersburg = folium.map.FeatureGroup()

# style the feature group
saint_petersburg.add_child(
    folium.features.CircleMarker(
        [59.938732, 30.316229], radius = 5,    # широта и долгота Санкт-Петербурга
        color = 'red', fill_color = 'Red'
    )
)

# add the feature group to the map
russia_map.add_child(saint_petersburg)

# label the Marker (пометить маркер)
folium.Marker([59.938732, 30.316229],         # широта и долгота Санкт-Петербурга
popup = 'Санкт-Петербург, в разговорной речи - Пи́тер, сокр.- СПб').add_to(russia_map)


# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

#Distance to Palace Bridge  Дворцовый мост
coordinates = [
    [59.93876, 30.31623],           # координаты красного круглого маркера
    [59.94022, 30.30931]]           # координаты дворцового моста

lines=folium.PolyLine(locations=coordinates, weight=1)
russia_map.add_child(lines)
distance = calculate_distance(coordinates[0][0], coordinates[0][1],
                              coordinates[1][0], coordinates[1][1])
distance_circle = folium.Marker(
    [59.94022,30.30931],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#252526;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
russia_map.add_child(distance_circle)
russia_map.add_child(mouse_position)

# vvodim koordinaty i stavim marker s polem na tochke

# put marker onclick
russia_map.add_child(folium.ClickForMarker(popup="Новый постомат"))
# display russia map
russia_map.save("map.html")
