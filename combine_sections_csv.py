import os
import re
import pandas as pd

# the starting dataframe
df = None


matching_folders = [f for f in os.listdir(
    "data") if re.match(r"section_\d{2}", f)]

# concatenate all of the 42 csv of each section in a single csv
for i, f in enumerate(matching_folders, start=1):
    print(f)
    with open(os.path.join("data", f)) as fr:
        print(i)
        data = fr.readlines()
        print(data)
        if i == 1:
            columns_names = data[0].split(",")
            # add the columns to the dataframe
            df = pd.DataFrame(pd.np.empty((0, len(columns_names))))
            print(columns_names)
            df.columns = columns_names

        df.loc[i] = data[1].split(",")

df.to_csv(os.path.join("data", "all_sections_votes.csv"), sep=",")
print(df)
