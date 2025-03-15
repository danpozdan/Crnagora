from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def get_all_links(link):
    """
    TODO
    """

    # First, initialise webdriver
    driver = webdriver.Chrome()

    # Go to the link
    driver.get(link)

    # Wait some time for me to be able to scroll :)
    # Input, so I choose when to stop
    cont = input("Stop? ")

    df_ = pd.DataFrame()

    # Get links
    el_with_links = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    row = 0
    for el in el_with_links:
        df_.loc[row, "Links"] = el.get_attribute("href")
        row += 1

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
            .replace(',', '.')
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
