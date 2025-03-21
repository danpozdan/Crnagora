from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def get_all_links(link) -> pd.DataFrame:
    """
    The function goes through a webpage, waits until the user scrolls down manually
        and gets all the valuable information.

    Args:
        link (str) : the link on Google Maps

    Returns:
        df_ (pd.DataFrame) : the data frame with results
    """

    # First, initialise webdriver
    driver = webdriver.Chrome()

    # Go to the link
    driver.get(link)

    # Wait some time for me to be able to scroll :)
    # Input, so I choose when to stop
    cont = input("Stop? ")

    df_ = pd.DataFrame()

    # Get stars
    el_with_st = driver.find_elements(By.CLASS_NAME, "MW4etd")
    row = 0
    for el in el_with_st:
        df_.loc[row, "Stars"] = float(el.text)
        row += 1

    # Number of reviews
    el_with_num = driver.find_elements(By.CLASS_NAME, "UY7F9")
    row = 0
    for el in el_with_num:
        df_.loc[row, "Number"] = float(
            el
            .text
            .replace('(', '')
            .replace(')', '')
            .replace(',', '')
        )
        row += 1

    driver.quit()

    return df_


# Unpack source links
source_links = {}
with open('Source_links.txt', encoding='utf-8') as file:
    for line in file:
        name, url = line.split('|')
        source_links[name] = url

# Manually go through all the links
with pd.ExcelWriter('Output_files/Stats.xlsx') as writer:
    for s_name, s_link in source_links.items():
        df = get_all_links(s_link)
        df.to_excel(writer, sheet_name=s_name)
