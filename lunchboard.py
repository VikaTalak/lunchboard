import streamlit as st
from streamlit_folium import folium_static
import folium

from geopy import distance
from geopy.geocoders import Nominatim

import pandas
import random


# Inspired by
# - https://docs.streamlit.io/en/stable/tutorial/visualize_rent_prices_with_Streamlit.html
# - https://www.linkedin.com/pulse/rapidly-build-apps-using-streamlit-python-jack-smart

# application name 
st.title("Unbelievable Lunchboard")

geolocator = Nominatim(user_agent="lunchboard")

@st.cache
def compute_location(address):
    return geolocator.geocode(address)

@st.cache
def read_csv(path):
    return pandas.read_csv(path, sep=";")

# center on *UM
location = compute_location("Grolmanstr. 40, 10623 Berlin")
UM = (location.latitude, location.longitude)

m = folium.Map(location=UM, zoom_start=15)

# read in dataframe of restaurants
df = read_csv("restaurants_lunch.csv")
restaurants = df[["Name", "Address", "Tags", "Price", "Google Rating", "Type"]].values.tolist()

# compute list of tags
tags = set()

for restaurant in restaurants:
    for entry in restaurant[2].split(","):
        tags.add(entry.strip())

st.sidebar.title("Select")

selected_kind = st.columns(2)

kind1 = selected_kind[0].checkbox("Café", value=True)
kind2 = selected_kind[1].checkbox("Restaurant", value=True)

kinds = set()
if kind1:
    kinds.add("Café")
if kind2:
    kinds.add("Restaurant")

filter = st.sidebar.multiselect('Category of restaurant', sorted(tags), default=None)

sidebar_cols = st.sidebar.columns(3)

price1 = sidebar_cols[0].checkbox("€", value=True)
price2 = sidebar_cols[1].checkbox("€€", value=True)
price3 = sidebar_cols[2].checkbox("€€€", value=True)

prices = set()
if price1:
    prices.add("€")
if price2:
    prices.add("€€")
if price3:
    prices.add("€€€")
prices.add("??") 

ratings = st.sidebar.slider("Google rating", 0.0, 5.0, (0.0, 5.0), 0.1, format="%.1f")

random_selection = st.sidebar.checkbox("Random restaurant", value=False)
if random_selection:
    restaurants = random.sample(restaurants, 1)

count = 0

# Filter list of restaurants and plot markers on the map
for restaurant in restaurants:
    name = restaurant[0]
    address = restaurant[1]
    price = restaurant[3]
    kind = restaurant[5]
    print(price, pandas.isna(price))
    if pandas.isna(price) : price = "??"
    rating = float(restaurant[4].replace(',', '.'))

    if price in prices and ratings[0] <= rating <= ratings[1] and kind in kinds:
        tags = [entry.strip() for entry in restaurant[2].split(",")]

        if set(filter).issubset(set(tags)):
            tags_string = ", ".join(tags) + f", {price}"

            location = compute_location(address)
            if location:
                # print(f"Location for {name} at {address}: {location.latitude}, {location.longitude} .")
                distance_km = distance.distance(UM, (location.latitude, location.longitude)).km

                # for the padding trick, see  https://stackoverflow.com/a/26213863/179014
                html = f'<h4>{name}</h4><ul style="padding-left: 1.2em;"><li>{tags_string}</li><li>Rating: {rating}</li><li>{distance_km:.2f} km</li></ul>'
                popup = folium.Popup(html)
                folium.Marker([location.latitude, location.longitude], popup=popup).add_to(m)
               
                # count of restaurants
                count += 1
            else:
                print(f"Cannot compute location for {name} at {address}.")

# add marker for *UM
popup = folium.Popup("<h4>*UM</h4>")
folium.Marker(UM, popup=popup, icon=folium.Icon(icon="rocket", prefix='fa')).add_to(m)
st.text(f"Number of restaurants: {count}")

# call to render Folium map in Streamlit
folium_static(m)

