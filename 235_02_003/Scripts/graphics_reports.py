import pandas as pd
import matplotlib.pyplot as plt
import os

new_directory = os.path.join('..', 'Graphics')
dataset_directory = os.path.join('..', 'Data', 'cwurData.csv')

# Загрузка данных
data = pd.read_csv(dataset_directory)
countries_full = pd.read_csv(os.path.join('..', 'Data', 'countries.csv'))
universities_full = pd.read_csv(os.path.join('..', 'Data', 'universities.csv'))
rankings_full = pd.read_csv(os.path.join('..', 'Data', 'rankings.csv'))
usiversities_country = pd.read_csv(os.path.join('..', 'Data', 'usiversities_country.csv'))
usiversities_rank = pd.read_csv(os.path.join('..', 'Data', 'usiversities_rank.csv'))



# Первые 100 элементов таблицы, топ 100 вузов
universities = universities_full.head(100)
rankings = rankings_full.head(100)
countries = countries_full.head(100)


def clustered_bar_chart_qual_qual(universities_subset, 
                                  atrib_1, 
                                  atrib_2):
    """
    Функция для создания кластеризованной столбчатой диаграммы
    для пары качественный - качественный

    Parameters:
    - universities_subsete: pandas.DataFrame
        Таблица с данными 
    - atrib_1: str
        Первый качественный атрибут
    -  atrib_2: str
        Второй качественный атрибут
    
    Returns:
    - clustered_bar_chart: png
        Новая диаграмма
    author: Saushkin Nikolay
    """
    plt.figure(figsize=(10, 6))
    universities_subset.groupby(atrib_1)[atrib_2].count().plot(kind='bar')
    plt.xlabel(f'{atrib_1}')
    plt.ylabel('Number of Universities')
    plt.title(f'Number of Universities by {atrib_1}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'clustered_bar_chart.png'))
    plt.show()


def pie_chart_qual_qual(universities_subset):
    """
    Функция для создания круговой диаграммы
    
    Parameters:
    - universities_subsete: pandas.DataFrame
        Таблица с данными 
    
    Returns:
    - pie_chart: png
        Новая диаграмма
    author: Arseniy Yastrebov
    """
    plt.figure(figsize=(8, 8))
    universities_subset['country'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, fontsize=8)
    plt.axis('equal')
    plt.title('Distribution of Universities by Country', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'pie_chart.png'))
    plt.show()


def categorized_histogram_quant_qual(rankings_subset):
    """
    Функция для создания категоризированный гистограммы
    для пары количественный - качественный

    Parameters:
    - rankings_subset: pandas.DataFrame
        Таблица с данными 
        
    Returns:
    - categorized_histogram: png
        Новая гистограмма
    author: Petrunina Maria
    """
    plt.figure(figsize=(10, 6))
    plt.hist(rankings_subset['score'], bins=10, alpha=0.5, label='Score')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Histogram of Scores')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'categorized_histogram.png'))
    plt.show()


def categorized_boxplot_quality_education_by_country(universities_subset):
    """
    Функция для создания категоризированный гистограммы
    для пары количественный - качественный

    Parameters:
    - universities_subset: pandas.DataFrame
        Таблица с данными (вся таблица) 
        
    Returns:
    - categorized_boxplot_quality_education_by_country: png
        Новый график
    author: Petrunina Maria
    """
    data.boxplot(column='quality_of_education', by='country', figsize=(16,10), rot=90)
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('Quality of Education', fontsize=10)
    plt.title('Boxplot of Quality of Education by Country', fontsize=12)
    plt.xticks(rotation=90)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'categorized_boxplot_quality_education_by_country.png'))
    plt.show()


def categorized_scatterplot(rankings_subset):
    """
    Функция для создания категоризированной диаграммы рассеивания
    для двух количественных и одного качественного
    Точка представляет собой университет, цвет страны
    Parameters:
    - rankings_subset: pandas.DataFrame
        Таблица с топ 100 вузов
        
    Returns:
    - categorized_scatterplot: png
        Новый график зависимости: 
            quality_of_education_vs_alumni_employment_by_country
    author: Saushkin Nikolay
    """
    plt.figure(figsize=(10, 6))
    colors = pd.factorize(rankings_subset['country'])[0]  # Цветовая кодировка для каждой страны
    plt.scatter(rankings_subset['quality_of_education'], rankings_subset['alumni_employment'], c=colors, cmap='viridis', alpha=0.5)
    plt.xlabel('Quality of Education')
    plt.ylabel('Alumni Employment')
    plt.title('Categorized Scatterplot: Quality of Education vs Alumni Employment by Country')
    plt.colorbar(label='Country')
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'categorized_scatterplot.png'))
    plt.show()


def average_university_score_by_country(data):
    """
    Функция для создания столбчатого графика зависимости среднего рейтинга вузов по странам 
    
    Parameters:
    - data: pandas.DataFrame
        Таблица с топ 100 вузов
        
    Returns:
    - Average_University_Score_by_Country: png
        Новый график зависимости
    author: Petrunina Maria
    """
    # Группировка данных по странам и вычисление среднего рейтинга в каждой стране
    average_score_by_country = data.groupby('country')['score'].mean()
    # Вычисление минимального и максимального среднего
    min_score = average_score_by_country.min() * 0.9
    max_score = average_score_by_country.max() * 1.1
    plt.figure(figsize=(12, 6))
    plt.ylim(min_score, max_score)  # Установка пределов по оси y, для лучшей видимости, можно убрать
    average_score_by_country.plot(kind='bar', color='skyblue')
    plt.title('Average University Score by Country')
    plt.xlabel('Country')
    plt.ylabel('Average Score')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(new_directory, 'Average_University_Score_by_Country.png'))
    plt.show()


def scatter_plot(rankings_subset):
    """
    Функция для создания категоризированной диаграммы рассеивания 
    Завимисоть: мировой рейтинг и место
    
    Parameters:
    - rankings_subset: pandas.DataFrame
        Таблица со странами
        
    Returns:
    - scatter_plot: png
        Новый график зависимости
    author: Arseniy Yastrebov
    """
    plt.figure(figsize=(10, 6))
    for country in rankings_subset['country'].unique():
        subset = rankings_subset[rankings_subset['country'] == country]
        plt.scatter(subset['world_rank'], subset['score'], label=country, alpha=0.7)
    plt.xlabel('World Rank')
    plt.ylabel('Score')
    plt.title('Scatter Plot of World Rank vs Score by Country')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(new_directory, 'scatter_plot.png'))
    plt.show()


def clustered_bar_citations(first_country, second_country):
    """
    Функция для создания кластеризованной столбчатой диаграммы
    для пары качественный атрибут — качественный атрибут
    
    Parameters:
    - first_country: str
        Страна для сравнения из основного data.frame
    - second_country: str
        Вторая страна для сравнения из основного data.frame
        
    Returns:
    - clustered_bar_citations: png
        Новый график зависимости
    author: Saushkin Nikolay
    """
    data_subset_2 = data[data['country'].isin([first_country, second_country])]
    citations_count_first = data_subset_2[data_subset_2['country'] == first_country]['citations'].sum()
    citations_count_second = data_subset_2[data_subset_2['country'] == second_country]['citations'].sum()
    plt.figure(figsize=(12, 8))
    plt.bar([first_country, second_country], [citations_count_first, citations_count_second], color=['orange', 'green'])
    plt.xlabel('Country')
    plt.ylabel('Number of Citations')
    plt.title(f'Number of Citations by {first_country} and {second_country}')
    plt.savefig(os.path.join(new_directory, 'clustered_bar_citations.png'))
    plt.show()


clustered_bar_chart_qual_qual(universities, 'country', 'national_rank')
pie_chart_qual_qual(universities)
categorized_histogram_quant_qual(rankings)
categorized_boxplot_quality_education_by_country(countries_full)
categorized_scatterplot(countries)
average_university_score_by_country(data)
scatter_plot(countries)
clustered_bar_citations("Estonia", "Turkey")
