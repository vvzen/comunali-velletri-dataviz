import os
import re
import pandas as pd

# the starting dataframe
df = None


matching_folders = [f for f in os.listdir(
    "data") if re.match(r"section_\d{2}", f)]

# open the csv files with the coordinates
with open(os.path.join("data", "sections_coordinates.csv")) as c:
    section_coordinates = c.readlines()

print("Section coordinates: ")
print(section_coordinates[1])

# concatenate all of the 42 csv of each section in a single csv
for i, f in enumerate(matching_folders, start=1):
    print(f)
    # read all of the single csv files
    with open(os.path.join("data", f)) as fr:
        print(i)
        csv_data = fr.readlines()
        print(csv_data)

    if i == 1:
        columns_names = ["Nome sezione (come elencata da google places)"]
        columns_names.extend(csv_data[0].split(","))
        columns_names.append("lat")
        columns_names.append("lng")
        # add the columns to the dataframe
        df = pd.DataFrame(pd.np.empty((0, len(columns_names))))
        # print(columns_names)s
        df.columns = columns_names

    # read section name from the csv
    new_row = [str(section_coordinates[i].split(",")[1]).rstrip()]
    # read section votes from the csv
    new_row.extend([str(d).rstrip() for d in csv_data[1].split(",")])
    # set the lat and long for each section
    new_row.append(str(section_coordinates[i].split(",")[2]).rstrip())
    new_row.append(str(section_coordinates[i].split(",")[3]).rstrip())

    # append the new row from the csv
    df.loc[i] = new_row

# rename index column
df.index.names = ["Numero sezione"]
df.to_csv(os.path.join("data", "all_sections_votes.csv"), sep=",")
print(df)
