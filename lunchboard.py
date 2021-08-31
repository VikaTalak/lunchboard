import streamlit as st
from streamlit_folium import folium_static
import folium

from geopy import distance
from geopy.geocoders import Nominatim

import pandas


# Inspired by
# - https://docs.streamlit.io/en/stable/tutorial/visualize_rent_prices_with_Streamlit.html
# - https://www.linkedin.com/pulse/rapidly-build-apps-using-streamlit-python-jack-smart

geolocator = Nominatim(user_agent="lunchboard")

@st.cache
def compute_location(address):

    normalized_address = address.replace("ß", "ss").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")

    return geolocator.geocode(normalized_address)

@st.cache
def read_csv(path):
    return pandas.read_csv(path, sep=";")

# center on *UM
location = compute_location("Grolmanstr. 40, 10623 Berlin")
UM = (location.latitude, location.longitude)

m = folium.Map(location=UM, zoom_start=15)

# add marker for *UM
popup = folium.Popup("<h4>*UM</h4>")
folium.Marker(UM, popup=popup, icon=folium.Icon(icon="rocket", prefix='fa')).add_to(m)


df = read_csv("restaurants_lunch.csv")
restaurants = df[["Name", "Address", "Tags"]].values.tolist()

tags = set()
for restaurant in restaurants:
    for entry in restaurant[2].split(","):
        tags.add(entry.strip())

st.sidebar.title("Select")
filter = st.sidebar.multiselect('Type of restaurant', sorted(tags), default=None)

for restaurant in restaurants:

    tags = [entry.strip() for entry in restaurant[2].split(",")]

    if set(filter).issubset(set(tags)):
        name = restaurant[0]
        address = restaurant[1]
        tags = restaurant[2]

        location = compute_location(address)
        if location:
            # print(f"Location for {name} at {address}: {location.latitude}, {location.longitude} .")
            distance_km = distance.distance(UM, (location.latitude, location.longitude)).km

            # for the padding trick, see  https://stackoverflow.com/a/26213863/179014
            html = f'<h4>{name}</h4><ul style="padding-left: 1.2em;"><li>{tags}</li><li>{distance_km:.2f} km</li></ul>'
            popup = folium.Popup(html)
            folium.Marker([location.latitude, location.longitude], popup=popup).add_to(m)
        else:
            print(f"Cannot compute location for {name} at {address}.")


st.title("Unbelievable Lunchboard")

# call to render Folium map in Streamlit
folium_static(m)

