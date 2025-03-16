# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KPZgATUAJ6jtRtYnHtJ05-7-5nbc6xat
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Financial_Model.xlsx'
timing = pd.read_excel(file_path, sheet_name='IS', skiprows=1, nrows=1, header=None)
data = pd.read_excel(file_path, sheet_name='IS', skiprows=37, nrows=3, header=None)
data = data.drop(data.columns[[0, 3, 4, 5]], axis=1)
timing = timing.drop(timing.columns[[0, 3, 4, 5]], axis=1)
df = pd.concat([timing, data], ignore_index=True)
print(df)

quarters = timing.iloc[0, 2:].tolist()
values_people = data.iloc[0, 2:].astype(float).tolist()

plt.figure(figsize=(16, 6))
plt.plot(quarters, values_people)
plt.xticks(rotation=45)
plt.title('Охват аудитории')
plt.xlabel('Период (квартал)')
plt.ylabel('Количество человек (млн.)')
plt.grid(True)
plt.show()

values_price = data.iloc[1, 2:].astype(float).tolist()

plt.figure(figsize=(16, 6))
plt.plot(quarters, values_price)
plt.xticks(rotation=45)
plt.title('Аппроксимированная цена курса на человека')
plt.xlabel('Период (квартал)')
plt.ylabel('Цена (€)')
plt.grid(True)
plt.show()

from matplotlib.ticker import FuncFormatter

values_returns = data.iloc[2, 2:].astype(float).tolist()

plt.figure(figsize=(16, 6))
plt.plot(quarters, values_returns)
plt.xticks(rotation=45)
# функция millions была использована с помощью чата GPT для того, чтобы
# можно было вывести значения не в десятках миллионов евро (по умолчанию)
# а просто в миллионах евро
def millions(x, pos):
    return f'{x/1e6:.1f}M'
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.title('Суммарная выручка')
plt.xlabel('Период (квартал)')
plt.ylabel('Миллионы евро (€)')
plt.grid(True)
plt.show()

data_2 = pd.read_excel(file_path, sheet_name='IS', skiprows=133, nrows=1, header=None)
data_2 = data_2.drop(data_2.columns[[0, 3, 4, 5]], axis=1)
df_2 = pd.concat([timing, data_2], ignore_index=True)
print(df_2)

values_expenses = data_2.iloc[0, 2:].astype(float).tolist()

plt.figure(figsize=(16, 6))
plt.plot(quarters, values_expenses)
plt.xticks(rotation=45)
# функция millions была использована с помощью чата GPT для того, чтобы
# можно было вывести значения не в десятках миллионов евро (по умолчанию)
# а просто в миллионах евро
def millions(x, pos):
    return f'{x/1e6:.1f}M'
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.title('Суммарные издержки')
plt.xlabel('Период (квартал)')
plt.ylabel('Миллионы евро (€)')
plt.grid(True)
plt.show()

data_3 = pd.read_excel(file_path, sheet_name='P&L', skiprows=14, nrows=1, header=None)
data_3 = data_3.drop(data_3.columns[[0, 3, 4, 5]], axis=1)
df_3 = pd.concat([timing, data_3], ignore_index=True)
print(df_3)

values_EBIT = data_3.iloc[0, 2:].astype(float).tolist()

plt.figure(figsize=(16, 6))
plt.plot(quarters, values_EBIT)
plt.xticks(rotation=45)
# функция millions была использована с помощью чата GPT для того, чтобы
# можно было вывести значения не в десятках миллионов евро (по умолчанию)
# а просто в миллионах евро
def millions(x, pos):
    return f'{x/1e6:.1f}M'
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.title('Значение EBIT')
plt.xlabel('Период (квартал)')
plt.ylabel('Миллионы евро (€)')
plt.grid(True)
plt.show()

data_4 = pd.read_excel(file_path, sheet_name='DCF', skiprows=17, nrows=1, header=None)
data_4 = data_4.drop(data_4.columns[[0, 3, 4, 5]], axis=1)
df_4 = pd.concat([timing, data_4], ignore_index=True)
print(df_4)

values_DCF_1 = data_4.iloc[0, 2:14].astype(float).tolist()
timing_1 = timing.iloc[0, 2:14].tolist()
colors = ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red',
          'red', 'green', 'green', 'green']

plt.figure(figsize=(16, 6))
bars = plt.bar(timing_1, values_DCF_1, color=colors)
plt.xticks(rotation=45)
plt.title('Значение Accumulated DCF, первый срок')
plt.xlabel('Период (квартал)')
plt.ylabel('Миллионы евро (€)')
plt.grid(True)
plt.show()

values_DCF_2 = data_4.iloc[0, 14:31].astype(float).tolist()
timing_2 = timing.iloc[0, 14:31].tolist()
colors = [ 'green', 'green', 'green', 'green', 'green', 'green', 'green',
           'green', 'green', 'green', 'green', 'green', 'green', 'green',
            'green', 'green', 'green', 'green']

plt.figure(figsize=(16, 6))
bars = plt.bar(timing_2, values_DCF_2, color=colors)
plt.xticks(rotation=45)
plt.title('Значение Accumulated DCF, второй срок')
plt.xlabel('Период (квартал)')
plt.ylabel('Десятки миллионов евро (€)')
plt.grid(True)
plt.show()