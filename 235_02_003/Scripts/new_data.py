# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:11:15 2024

@author: petrm
"""

import os
import pandas as pd


# Загрузка данных
dataset_directory = os.path.join('..', 'Data', 'cwurData.csv')

# 3 нф - заданная таблица data
data = pd.read_csv(dataset_directory)

# 2 нф 
# Создание таблицы Университетов (Universities)
universities = data[['institution', 'country', 'national_rank']].copy()

# Создание таблицы Рейтингов (Rankings)
rankings = data[['institution', 'world_rank', 'quality_of_education', 'alumni_employment',
                 'quality_of_faculty', 'publications', 'influence', 'citations',
                 'broad_impact', 'patents', 'score']].copy()

# Создание таблицы Стран (Countries)
countries = data[['country',
                  'quality_of_education', 
                  'alumni_employment', 
                  'score', 
                  'world_rank']].copy()

# 1 нф 
usiversities_country = universities[['institution', 'country']].copy()


usiversities_rank = universities[['national_rank', 'country']].copy()

# Сохранение таблиц в файлы CSV
df = {
    'countries.csv': countries,
    'universities.csv': universities,
    'rankings.csv': rankings,
    'usiversities_country.csv': usiversities_country,
    'usiversities_rank.csv': usiversities_rank
}

for filename, dataframe in df.items():
    dataframe.to_csv(os.path.join('..', 'Data', filename), index=False)


