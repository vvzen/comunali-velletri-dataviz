import requests
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup
import os
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

# load API key for Google Geocoding
with open("google-api.json") as f:
    GOOGLE_API_KEY = json.load(f)["geocoding-api"]

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode"
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/details"
COMUNE_VELLETRI_URL = "http://www.comune.velletri.rm.it/elezioni/2018/sezioni.html"

with open(os.path.join("data", "section_names_manually_cleaned.csv"), "r") as f:
    places = f.readlines()[1].split(",")

# read the addresses and names from the cleaned csv
df = pd.read_csv(os.path.join(
    "data", "section_names_manually_cleaned.csv"), sep=",", header=None)

df = df.transpose()
df.columns = ["section number", "section name"]

print(df)

# 1. loop in the csv
for i, place in enumerate(places):
    try:
        current_section_name = place

        # print("section name: {}".format(current_section_name))

        # remove double spaces
        re.sub(r"\s\s", " ", current_section_name)

        # format for query string
        current_section_name = re.sub(r"\s", "+", current_section_name)
        current_section_name.replace("'", "")

        current_section_address = "{},Velletri,IT".format(current_section_name)
        current_section_address = re.sub(r"\+{2}", "", current_section_address)
        # print(current_section_address)

        # 2. geocode the address to get the coordinates
        request_url = "{}/json?address={}&key={}".format(
            GOOGLE_GEOCODE_URL, current_section_address, GOOGLE_API_KEY)

        print("request url: {}".format(request_url))

        r = requests.get(request_url)

        coordinates = r.json()["results"][0]["geometry"]["location"]
        placeid = r.json()["results"][0]["place_id"]
        pp.pprint(coordinates)

        print("geocode")
        print("request url: {}".format(request_url))
        print("place id: {}".format(placeid))

        # ask google places the nice name of this place based on the place id
        request_url = "{}/json?placeid={}&fields=name,rating&key={}".format(
            GOOGLE_PLACES_URL, placeid, GOOGLE_API_KEY)
        rp = requests.get(request_url)

        print("places")
        print("request url: {}".format(request_url))

        try:
            place_nice_name = rp.json()["result"]["name"]
        except KeyError:
            place_nice_name = current_section_name
        df.loc[i, "section name"] = place_nice_name
        df.loc[i, "lat"] = coordinates["lat"]
        df.loc[i, "lng"] = coordinates["lng"]

    except IndexError:
        pass

print("-"*60)
print(df)
print("-"*60)
# # remove rows with the same address
# df.drop_duplicates(subset="section address", inplace=True, keep="last")
# df = df.drop("section number", 1)
# print(df)

# save the dataframe as a csv
df.to_csv(os.path.join("data", "sections_coordinates.csv"), sep=",", index=False)
