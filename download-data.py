import requests
import csv
from collections import OrderedDict  # for sorting the dictionary
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)
url = "http://www.comune.velletri.rm.it/elezioni/amministrative-2018/CCcandipersezione"

# the number of voting sections in Velletri,
# which appears to be also the Answer to the Ultimate Question of Life, the Universe and Everything
number_of_sections = 42

# the main data structure
section_data = {}

# loop through all the sections
for i in range(1, number_of_sections+1):
    current_url = "{}{}.html".format(url, i)
    # get the page
    r = requests.get(current_url)
    # soup it
    soup = BeautifulSoup(r.text, "html.parser")

    print(current_url)

    section_data[i] = {}

    # loop in the table structure
    for tr in soup.find_all('tr'):
        # print("current row: {}".format(tr))
        tds = tr.find_all('td')
        # print("current row: {}".format(tds))
        try:
            # get the name of the list
            list_name = tds[1].text

            # initialise our data structure
            # key: list name, value: number of votes
            try:
                section_data[i][list_name]
            except KeyError:
                section_data[i][list_name] = 0

            # get the number of votes
            try:
                list_votes = int(tds[3].text)
            except ValueError:
                list_votes = 0

            section_data[i][list_name] += list_votes
            # print("Lista: {}".format(list_name).encode('utf-8'))
            # print("Nome: {}".format(tds[2].text).encode('utf-8'))
            # print("Voti: {}".format(list_votes))
        except IndexError:
            pass
        # print("Lista: {}".format(tds[0]))
    # print(r.text)

    print("Sezione {}".format(i))
    pp.pprint(section_data[i])

    # sort the section data by vote
    ordered_section_data = OrderedDict(
        sorted(section_data[i].items(), key=lambda x: x[0], reverse=False))

    # save the dictionary as a csv
    with open("data/section_{}.csv".format(str(i).zfill(2)), "w") as f:
        w = csv.DictWriter(f, ordered_section_data.keys())
        w.writeheader()
        w.writerow(ordered_section_data)
