import csv
import pandas as pd
import obj.wire # import the wire class

# read the csv in as a dataframe
df = pd.read_csv('Wire Data Input.csv')
print(df)

# Access a column
f = df["Wire Number"]


