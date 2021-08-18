import streamlit as st
from streamlit_folium import folium_static
import folium

from geopy import distance
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="lunchboard")

@st.cache
def compute_location(address):
    return geolocator.geocode(address)


# center on *UM
location = compute_location("Grolmanstr. 40, 10623 Berlin")
UM = (location.latitude, location.longitude)

m = folium.Map(location=UM, zoom_start=16)

# add marker for *UM
popup = folium.Popup("<h4>*UM</h4>")
folium.Marker(UM, popup=popup, icon=folium.Icon(icon="rocket", prefix='fa')).add_to(m)


# list of restaurants
restaurants = [("Elephant", "Fasanenstraße 15, 10623 Berlin", ("Thai", "€€")),
               ("Café Bleibtreu", "Bleibtreustraße 45, 10623 Berlin", ("German", "€")),
               ("Berliner Kaffeerösterei", "Uhlandstraße 173/174, 10719 Berlin", ("Café", "€€"))]

for restaurant in restaurants:
    name = restaurant[0]
    address = restaurant[1]
    tags = ", ".join(entry for entry in restaurant[2])

    location = compute_location(address)
    distance_km = distance.distance(UM, (location.latitude, location.longitude)).km

    # for the padding trick, see  https://stackoverflow.com/a/26213863/179014
    html = f'<h4>{name}</h4><ul style="padding-left: 1.2em;"><li>{tags}</li><li>{distance_km:.2f} km</li></ul>'
    popup = folium.Popup(html)
    folium.Marker([location.latitude, location.longitude], popup=popup).add_to(m)


st.title("Unbelievable Lunchboard")

# call to render Folium map in Streamlit
folium_static(m)

