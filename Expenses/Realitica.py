import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re


def make_real_estate_data_frame() -> pd.DataFrame:
    """
    The function parses data from the Realitica website.

    Returns:
        df_realitica (pd.DataFrame) : the data frame with the statistics (uncleaned).
    """

    # Create the df
    df_realitica = pd.DataFrame(
        columns=['Page', 'Metres', 'Cost (€)', 'City', 'Cost per meter']
    )

    # The URL of our page that we will parse
    url = 'https://www.realitica.com/prodaja/poslovnih+prostora/Crna-Gora/'

    # List of desirable cities
    cities = ['Budva', 'Bar', 'Nercg Novi', 'Kotor', 'Tivat']

    pages = 0
    previous_block_len = 0
    row = 0
    while True:
        # Make the soup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all div blocks
        blocks_html = soup.find_all('div')

        # Filter the blocks
        if (len(blocks_html) != 22) or (len(blocks_html) != previous_block_len):
            previous_metres = None
            previous_cost = None
            for div in blocks_html:
                # Which city?
                city = [city for city in cities if str(city) in str(div.text)]
                if ("m2" in div.text) and ("€" in div.text) and (len(city) > 0):
                    # Take the main parameters
                    metres = re.search(r'(\d+.\d+|\d+) m2', str(div.text))
                    cost = re.search(r'€(\d+.\d+.\d+|\d+.\d+|\d+)', str(div.text))
                    city = city[0]
                    if metres and cost:
                        current_metres = float(metres.group(1).replace(',',  '').replace('.',  ''))
                        current_cost = float(cost.group(1).replace(',',  '').replace('.',  ''))
                        if (current_metres != previous_metres) or (current_cost != previous_cost):
                            previous_metres = current_metres
                            previous_cost = current_cost
                            df_realitica.loc[row, 'Page'] = pages
                            df_realitica.loc[row, 'Metres'] = current_metres
                            df_realitica.loc[row, 'Cost (€)'] = current_cost
                            df_realitica.loc[row, 'City'] = city
                            df_realitica.loc[row, 'Cost per meter'] = current_cost / current_metres
                            row += 1

            pages += 1
            previous_block_len = len(blocks_html)
            url = f'https://www.realitica.com/?cur_page={pages}&type=Commercial&for=Prodaja&lng=hr&pZpa=Crna+Gora'
        else:
            break

    return df_realitica


def clean_real_estate_data_frame(df_uncleaned_to_func) -> pd.DataFrame:
    """
    The function clears the data on real estate

    Args:
        df_uncleaned_to_func (pd.DataFrame) : the data frame with the statistics (uncleaned).

    Returns:
        df_realitica (pd.DataFrame) : the data frame with the statistics (cleaned).
    """

    df_realitica = pd.DataFrame(
        columns=['Page', 'Metres', 'Cost (€)', 'City', 'Cost per meter']
    )

    for index, row in df_uncleaned_to_func.iterrows():
        # If check will remain True we will add the row
        check = True

        # Check that the price is not too low (sometimes they load the rent price)
        if row['Cost (€)'] < 20000:
            check = False

        # Check that the number of metres isn't too high
        if row['Metres'] > 2000:
            check = False

        if check:
            df_realitica.loc[len(df_realitica)] = row

    return df_realitica


def make_charts_and_stats(df_cleaned_to_func) -> pd.DataFrame:
    """
    The function makes charts and some statistics

    Args:
        df_cleaned_to_func (pd.DataFrame) : the data frame with the data (cleaned).

    Returns:
        df_stat (pd.DataFrame) : the data frame with the summaries
    """

    # First summarise by category:
    df_stat = df_cleaned_to_func.groupby('City').agg({
        'Cost (€)': ['mean', 'median', 'count'],
        'Metres': ['mean', 'median'],
        'Cost per meter': ['mean', 'median']
    })

    df_stat.columns = ['_'.join(col) for col in df_stat.columns]

    # Now we'll switch to charts
    # The dependence of metres to price
    plt.subplot(2, 2, 1)
    plt.scatter(df_cleaned_to_func['Metres'], df_cleaned_to_func['Cost per meter'])
    plt.title('Metres - Price per meter (€)')
    ls = np.linspace(start=52, stop=1600, num=100000)
    plt.plot(ls, (50000 / (ls-50)) + 1800, color='red', alpha=0.5)

    plt.tight_layout()
    plt.show()

    return df_stat


df_uncleaned = make_real_estate_data_frame()
df_cleaned = clean_real_estate_data_frame(df_uncleaned)
df_summary = make_charts_and_stats(df_cleaned)

# Save everything to Excel
with pd.ExcelWriter('Data/Realitica.xlsx') as writer:
    df_uncleaned.to_excel(writer, sheet_name='Uncleaned', index=False)
    df_cleaned.to_excel(writer, sheet_name='Cleaned', index=False)
    df_summary.to_excel(writer, sheet_name='Summary', index=True)
