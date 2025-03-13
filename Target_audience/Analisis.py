import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_cleaned_dataframe() -> pd.DataFrame:
    """
    This function cleans the table

    Returns:
        table (pd.DataFrame) : cleaned table
    """
    table = pd.read_excel('Downloaded_data/World_bank_stat.xls')

    # Clear the first two rows
    table = table.drop(table.index[0:2]).reset_index(drop=True)

    # Clear the first two columns
    table = table.drop(
        columns=[
            'Data Source',
            'World Development Indicators'
        ]
    )

    # Play a bit with columns
    table.columns = table.iloc[0]
    table.columns = table.columns.astype(str)
    for name in table.columns:
        if '.0' in name:
            new_name = name[:-2]
            table.rename(columns={name: new_name}, inplace=True)
    table = table.drop(table.index[0]).reset_index(drop=True)

    # Find only rows with unemployed:
    target_words = [
        'unemployment', 'employed', 'unemployed',
        'labour', 'labor'
    ]
    not_needed_indices = []
    for index, row in table.iterrows():
        yes = False
        for target in target_words:
            if target in row[0].lower():
                yes = True
        if not yes:
            not_needed_indices.append(index)
        else:
            # Clean from empty rows
            if row[2:].isna().all():
                not_needed_indices.append(index)

    table = table.drop(table.index[not_needed_indices]).reset_index(drop=True)

    return table


def get_info_on_row(table, row_index) -> list:
    """
    Prints out the description of the row. Purely for the programmer

    Args:
        table (pd.DataFrame) : the data frame where we took the index from
        row_index (int) : index of the target

    Returns:
        list : indicator name and description
    """

    # Get the ID_CODE
    id_code = table.loc[row_index, 'Indicator Code']

    # Load the table with descriptions
    table_def = pd.read_excel(
        io='Downloaded_data/World_bank_stat.xls',
        sheet_name='Metadata - Indicators'
    )

    table_def.set_index(table_def['INDICATOR_CODE'], inplace=True)

    return [
        str("INDICATOR NAME:" + table_def.loc[id_code, 'INDICATOR_NAME']),
        str("DESCRIPTION:" + table_def.loc[id_code, 'SOURCE_NOTE'])
    ]


def get_list_of_needed(dataframe) -> list:
    """
    This command finds the rows we need. There was a lot of manual work that
        was commented intentionally.

    Args:
        dataframe (pd.DataFrame) : the searching data frame

    Returns:
        list_of_needed (list) : list of needed indexes
    """

    """
    # Education
    for i in range(len(dataframe)):
        if 'education' in get_info_on_row(dataframe, i)[0]:
            print(i)
            print(get_info_on_row(dataframe, i)[0])
    """
    list_of_needed = [
        [3, 9, 16, 22, 28, 33],  # Education
        [4, 15, 19, 43, 44]  # Unemployment
    ]

    return list_of_needed


def make_small_df(dataframe, list_of_needed) -> pd.DataFrame:
    """
    This command finds the rows we need and makes a new data frame
        from them

    Args:
        dataframe (pd.DataFrame) : the searching data frame
        list_of_needed (list) : the list of indices we need

    Returns:
        table (pd.DataFrame) : small table
    """

    # Education
    table_1 = pd.DataFrame(
        columns=dataframe.columns
    )

    for index, row in dataframe.iterrows():
        if index in list_of_needed[0]:
            table_1.loc[len(table_1)] = row

    # Labour
    table_2 = pd.DataFrame(
        columns=dataframe.columns
    )

    for index, row in dataframe.iterrows():
        if index in list_of_needed[1]:
            table_2.loc[len(table_2)] = row

    table_1 = table_1.sort_values(by='Indicator Name', ascending=True)
    table_2 = table_2.sort_values(by='Indicator Name', ascending=True)
    table = pd.concat([table_1, table_2], ignore_index=True)

    return table


def make_charts(dataframe):
    """
    The function makes charts

    Args:
        dataframe (pd.DataFrame) : the data frame with the data (cleaned).
    """

    def make_bar_plot(number, index, name, legend=True):
        plt.subplot(2, 2, number)
        ticker = np.arange(2011, 2022)
        bar_width = 0.35
        plt.bar(
            ticker - bar_width / 2,
            dataframe.loc[index][-12:-1],
            bar_width,
            label='Employed',
            color='skyblue',
            edgecolor='black'
        )
        plt.bar(
            ticker + bar_width / 2,
            dataframe.loc[index+3][-12:-1],
            bar_width,
            label='Unemployed',
            color='blue',
            edgecolor='black'
        )
        plt.title(name)
        if legend:
            plt.legend(fontsize=8)

    make_bar_plot(number=1, index=0, name='Advanced education', legend=False)
    make_bar_plot(number=2, index=2, name='Intermediate education', legend=False)
    make_bar_plot(number=3, index=1, name='Basic education')

    # Last chart is a bit different
    plt.subplot(2, 2, 4)
    ticker = np.arange(3)
    categories = ['Advanced', 'Basic', 'Intermediate']
    plt.xticks(ticker, categories)
    bar_width = 0.35
    plt.bar(
        ticker - bar_width / 2,
        dataframe.iloc[0:3, -4],
        bar_width,
        label='Employed',
        color='skyblue',
        edgecolor='black'
    )
    plt.bar(
        ticker + bar_width / 2,
        dataframe.iloc[3:6, -4],
        bar_width,
        label='Unemployed',
        color='blue',
        edgecolor='black'
    )
    plt.title('2020')

    plt.tight_layout()
    plt.show()


df = get_cleaned_dataframe()
list_of_indices = get_list_of_needed(df)
small_df = make_small_df(df, list_of_indices)
make_charts(small_df)

# Save everything to Excel
with pd.ExcelWriter('Output_data/World_bank_data.xlsx') as writer:
    df.to_excel(writer, sheet_name='Cleaned', index=True)
    small_df.to_excel(writer, sheet_name='Small', index=True)
