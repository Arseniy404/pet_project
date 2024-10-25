# -*- coding: utf-8 -*-
"""
Created on Sat May 4 13:09:45 2024

@author: petrm
"""
import os
import pandas as pd
import numpy as np

dataset_directory = os.path.join('..', 'Data', 'cwurData.csv')
new_directory = os.path.join('..', 'Output')
data = pd.read_csv(dataset_directory)


def get_universities_with_highest_ranking(data_frame, country):
    """
    Функция для определения университетов с самым высоким рейтингом из определенной страны

    Parameters:
    - data_frame: pandas.DataFrame
        Исходная таблица с данными об университетах
    - country: str
        Название страны
    
    Returns:
    - universities_df: pandas.DataFrame
        Новая таблица с данными об университетах страны
    author: Petrunina Maria
    """
    top_universities = []

    for index, row in data_frame.iterrows():
        if row['country'] == country:
            if row['institution'] not in top_universities:
                top_universities.append(row['institution'])

    universities_df = pd.DataFrame({f'Score_by_{country}': range(1, len(top_universities) + 1),
                                    'institution': top_universities})
    universities_df.to_csv(os.path.join(new_directory, f'uni_score_{country}.csv'), 
                           index=False)
    return universities_df

#Пример использования
get_universities_with_highest_ranking(data, 'Germany')


def most_popular_country_function(data_frame):
    """
    Функция для определения самой популярной страны с университетами

    Parameters
    data_frame : pandas.DataFrame
        Исходная таблица с данными об университетах

    Returns
    result_df : pandas.DataFrame
        Новая таблица с данными об университетах самой популярной страны
    author: Saushkin Nikolay
    """
    # Считаем количество упоминаний стран в файле
    place_counts = data_frame['country'].value_counts()

    result_df = pd.DataFrame({'country':
                              place_counts.index.values,
                              'count': place_counts.values})
    result_df.to_csv((os.path.join(new_directory, 'most_popular.csv')), 
                     index=False)

    return result_df

#Пример использования
most_popular_country_function(data)


def score_most_popular_country(data_frame):
    """
    Функция для определения общего рейтинга для каждой страны

    Parameters
    data_frame : pandas.DataFrame
        Исходная таблица с данными об университетах
    
    Returns
    top_country_ratings : pandas.DataFrame
        Новая таблица с данными об общем рейтинге для каждой страны
    author: Saushkin Nikolay
    """
    country_ratings = {}

    for i in range(len(data_frame)):
        country = data_frame.at[i, 'country'] 
        score = data_frame.at[i, 'score'] 

        if country in country_ratings:
            country_ratings[country] += score
        else:
            country_ratings[country] = score

    top_country_ratings = pd.DataFrame(list(country_ratings.items()), 
                                       columns=['country', 'total_score'])

    top_country_ratings = top_country_ratings.sort_values(by='total_score', ascending=False)

    top_country_ratings.to_csv((os.path.join(new_directory, 'top_country_ratings.csv')), 
                               index=False)
    
    return top_country_ratings

#Пример использования
score_most_popular_country(data)



def get_top_institutions(data_frame, column_name, number):
    """
    Функция для поиска топового заданного числа университетов по заданному критерию
    Parameters:
    - data_frame: pandas.DataFrame
        Исходная таблица с данными об университетах
    - column_name: str
        Название столбца по которому происходит разделение
    - n: int
        Количество университетов

    Returns:
    - sorted_universities: pandas.DataFrame
        Новая таблица с данными университетах по критерию
    author: Arseniy Yastrebov
    """
    sorted_universities = data_frame.sort_values(by=column_name, ascending=False)
    sorted_universities = sorted_universities.head(number)
    sorted_universities.to_csv((os.path.join(new_directory, 
                                                     f'top_{number}_with_{column_name}.csv')), 
                                       index=False)
    return sorted_universities

#Пример использования
print(get_top_institutions(data, column_name='year', number=5))


#Функция, в которой используются неравенства
def get_filtered_with_scores(df, min_score, max_score):
    """
    Функция для определения университетов с рейтингом между минимальным и максимальным, 
    которые вводит пользователь

    Parameters:
    - df: pandas.DataFrame
        Исходная таблица с данными об университетах
    - min_score: int
        Минимальный рейтинг
    - max_score: int
        Максимальный рейтинг

    Returns:
    - uni_with_score_filter: pandas.DataFrame
        Новая таблица с университетом с заданным диапазоном по рейтингу
    author: Petrunina Maria
    """
    uni_with_score_filter = df[(df['score'] >= min_score) & (df['score'] <= max_score)]
    uni_with_score_filter.to_csv((os.path.join(new_directory,  
                                                   f'score_between_{min_score}_{max_score}.csv')), 
                                     index=False)
    return uni_with_score_filter

#Пример использования
get_filtered_with_scores(data, 10, 15)


#Аналогичная функция для лет
def get_filtered_with_years(df, min_year, max_year):
    """
    Функция для определения университетов с годами между

    Parameters:
    - df: pandas.DataFrame
        Исходная таблица с данными об университетах
    - min_year: int
        Минимальный год
    - max_year: int
        Максимальный год

    Returns:
    - uni_with_score_filter: pandas.DataFrame
        Новая таблица с данными об университетах между заданными годами
    author: Saushkin Nikolay
    """
    uni_with_year_filter = df[(df['year'] >= min_year) & (df['year'] <= max_year)]
    uni_with_year_filter.to_csv((os.path.join(new_directory,  
                                                   f'year_between_{min_year}_{max_year}.csv')), 
                                     index=False)
    return uni_with_year_filter

#Пример использования
get_filtered_with_years(data, 2012, 2014)


# Создание сводной таблицы
def new_pivot_table(df, index_row, columns_row, values, aggfunc):
    """
    Функция создает сводную таблицу на основе указанных столбцов и функции, 
    которая может принимать список функций

    Parameters:
    - data: pandas.DataFrame
        Исходная таблица с данными об университетах
    - index_row: str
        Название столбца для индексов сводной таблицы
    - columns_row: str
        Название столбца для колонок сводной таблицы
    - values: str
        Название столбца для значений сводной таблицы
    - aggfunc: str or function
        Удобная функция для сводной таблиц

    Returns:
    - pivot_table: pandas. Dataframe
    author: Petrunina Maria
    """
    table = pd.pivot_table(df, values=values, index=index_row, columns=columns_row, aggfunc=aggfunc)
    numerics = table.select_dtypes(include="number")
    table.loc[:, numerics.columns] = np.round(numerics, 2)
    table.to_csv(os.path.join(new_directory, 
                                    f'pivtab_{index_row}_{columns_row}_{aggfunc}_{values}'),
                 index = False)
    return table

#Построение сводной таблицы по среднему рейтингу университетов по странам и годам
pivot_table = new_pivot_table(data, 'country', 'year', 'score', 'mean')
print(pivot_table)
