import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def make_df():
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

    return df


def make_a_chart(df):
    """
    TODO
    """
    # Make a pivot df for charts
    df_copy = df.copy().T
    df_pivot = df_copy.pivot(index='City', columns='Industry', values='Average rating')

    # Make charts
    plt.figure()

    df_pivot.plot(kind="bar", figsize=(10, 6))

    plt.ylim(4, 5.35)
    plt.yticks([4, 5])

    plt.xlabel('Города')
    plt.ylabel('Средний рейтинг')
    plt.title('Средний рейтинг по городам и отраслям')
    plt.legend(title='Отрасли', loc='upper right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


def make_map(df, industry):

    coordinates = {
        'Budva': [42.289080, 18.843906],
        'Podgorica': [42.441228, 19.263141],
        'Bar': [42.098111, 19.095272],
        'Kotor': [42.425071, 18.768959],
        'Tivat': [42.429463, 18.698936]
    }

    for city, coordinates_list in coordinates.items():
        for column in df.columns:
            if df.loc['City', column] == city:
                df.loc['Latitude', column] = coordinates_list[0]
                df.loc['Longitude', column] = coordinates_list[1]

    df = df.T
    df['Average rating'] = pd.to_numeric(df['Average rating'])
    sub_df = df[df['Industry'] == industry]

    fig = px.scatter_mapbox(
        sub_df, lat='Latitude', lon='Longitude',
        hover_name='City', color='Average rating',
        size='Average rating', zoom=8.5, height=500,
        mapbox_style='open-street-map',
        color_continuous_scale=['green', 'yellow', 'red'],
        hover_data={
            'Average rating': True,
            'Latitude': False,
            'Longitude': False
        }
    )

    fig.show()


dataframe = make_df()
# make_a_chart(dataframe)
make_map(dataframe, 'cafe')
make_map(dataframe, 'barber')
make_map(dataframe, 'groceries')
