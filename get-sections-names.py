import requests
import csv
import re  # for getting numbers of the sections from the string
from bs4 import BeautifulSoup
from collections import OrderedDict  # for sorting the dictionary
import pprint

pp = pprint.PrettyPrinter(indent=4)

# main url
url = "http://www.comune.velletri.rm.it/elezioni/amministrative-2018/CCcandipersezione.html"

# data structure holding the names and numbers of each section
section_names = {}

# get the page
r = requests.get(url)

print(r.text)

# soup it
soup = BeautifulSoup(r.text, "html.parser")

# loop in the table structure
for tr in soup.find_all('tr'):
    splitted_row = tr.text.split("-")
    # print(splitted_row)
    if len(splitted_row) > 1:
        section_number = re.findall(r"\d+", splitted_row[0])
        if len(section_number) > 0:
            section_number = section_number[0]
        section_name = splitted_row[1]
        try:
            section_name = "{}{}".format(splitted_row[1], splitted_row[2])
        except IndexError:
            pass
        section_name = section_name.rstrip().lower()
        section_names[str(section_number).zfill(2)] = section_name
        print("section number: {}".format(section_number))
        print("section name  : {}".format(section_name))

pp.pprint(section_names)

# sort the section data by name
ordered_section_names = OrderedDict(
    sorted(section_names.items(), key=lambda x: x[0]))

# save the dictionary as a csv
with open("data/section_names_numbers.csv", "w") as f:
    w = csv.DictWriter(f, ordered_section_names.keys())
    w.writeheader()
    w.writerow(ordered_section_names)
