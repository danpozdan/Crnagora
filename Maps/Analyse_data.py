import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

excel_file = pd.ExcelFile('Output_files/Stats.xlsx')
sheet_dict = {sheet_name: excel_file.parse(sheet_name) for sheet_name in excel_file.sheet_names}

df = pd.DataFrame()

for sheet_name, sheet_df in sheet_dict.items():
    city, industry = sheet_name.split('_')
    df.loc["City", sheet_name] = city
    df.loc["Industry", sheet_name] = industry
    df.loc["Number of reviews", sheet_name] = np.sum(sheet_df["Number"])
    rating_to_number = 0
    for index, row in sheet_df.iterrows():
        add_to_rating = row["Number"]*row["Stars"]
        rating_to_number += add_to_rating
    average_rating = rating_to_number / np.sum(sheet_df["Number"])
    df.loc["Average rating", sheet_name] = average_rating

df.to_excel('Output_files/Analysed_stats.xlsx')

# Make charts
plt.figure()
# TODO
plt.tight_layout()
plt.show()
