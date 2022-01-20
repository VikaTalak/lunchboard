import pandas

from geopy.geocoders import Nominatim
from geopy import distance

geolocator = Nominatim(user_agent="lunchboard")


def compute_location(address):
    return geolocator.geocode(address)


def read_csv(path):
    return pandas.read_csv(path, sep=";")


location = compute_location("Grolmanstr. 40, 10623 Berlin")
UM = (location.latitude, location.longitude)

df = read_csv("restaurants_lunch.csv")
restaurants = df[["Name", "Address", "Tags", "Price", "Google Rating", "Type"]].values.tolist()

restaurants_out = []

for restaurant in restaurants:
    name = restaurant[0]
    address = restaurant[1]
    price = "€??" if pandas.isna(restaurant[3]) else restaurant[3]
    rating = float(restaurant[4].replace(',', '.'))

    location = compute_location(address)
    if location:
        distance_km = distance.distance(UM, (location.latitude, location.longitude)).km

        restaurant_out = restaurant
        restaurant_out[3] = price
        restaurant_out[4] = rating
        restaurant_out.extend([location.latitude, location.longitude, distance_km])
        print(restaurant_out)

        restaurants_out.append(restaurant_out)

df_out = pandas.DataFrame(restaurants_out,
                          columns=["Name", "Address", "Tags", "Price", "Google Rating",
                                   "Type", "Latitude", "Longitude", "Distance"])

df_out.to_csv("restaurants.csv")
