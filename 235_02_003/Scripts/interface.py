import os
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt


# Список для хранения истории действий
action_history = []


# Вывод авторов
def show_authors():
    """
    Функция для отображения информации об авторах программы

    author: Petrunina Maria
    """
    messagebox.showinfo("Авторы", "Авторы:\nМария Петрунина\n"
                                  "Ястребов Арсений\n"
                                  "Саушкин Николай")


# Загружаем таблицу при нажатии кнопки "Работа с таблицами"
def load_table():
    """
    Функция для загрузки таблицы из файла и отображения опций работы с таблицей

    author: Petrunina Maria
    """
    file_path = filedialog.askopenfilename(title="Выберите файл таблицы",
                                           filetypes=(("CSV files", "*.csv"), ("Excel files", "*.xlsx")))
    if file_path:
        try:
            # Попытка загрузить файл таблицы
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            # Показать сообщение о загрузке таблицы
            messagebox.showinfo("Загрузить таблицу", f"Файл {file_path} загружен")
            # Показать окно с кнопками для работы с таблицей
            show_table_options(df)
            # Добавить действие в историю
            action_history.append(load_table)
        except Exception as e:
            # В случае ошибки показать сообщение об ошибке
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")


# Кнопки, которые выводятся после загрузки таблицы
def show_table_options(df):
    """
    Функция для отображения окна с опциями работы с таблицей

    Parameters:
    - df: pandas.DataFrame
        Загруженная таблица данных

    author: Saushkin Nikolay
    """
    table_window = tk.Toplevel(root)
    table_window.title("Работа с таблицами")
    table_window.geometry(f"{app_width}x{app_height}+{x}+{y}")

    show_button = tk.Button(table_window, text="Вывести таблицу", command=lambda: show_table_content(df))
    show_button.place(x=125, y=50, width=140, height=35)

    edit_button = tk.Button(table_window, text="Изменить таблицу", command=lambda: edit_table(df))
    edit_button.place(x=125, y=150, width=140, height=35)

    plot_button = tk.Button(table_window, text="Построить график", command=lambda: show_graph_options(df.head(100)))
    plot_button.place(x=125, y=250, width=140, height=35)

    # Добавить кнопку "Назад"
    back_button = tk.Button(table_window, text="Назад", command=go_back)
    back_button.place(x=150, y=350, width=80, height=20)


# Функция для отображения содержимого таблицы
def show_table_content(df):
    """
    Функция для отображения содержимого таблицы в новом окне

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными

    author: Saushkin Nikolay
    """
    # Создание нового окна для отображения содержимого загруженной таблицы
    content_window = tk.Toplevel(root)
    content_window.title("Содержимое загруженной таблицы")
    content_window.geometry("900x900")

    # Создание виджета текста для отображения содержимого таблицы
    text_widget = tk.Text(content_window, wrap="none", width=100, height=30)
    text_widget.insert("end", df.to_string(index=False))
    text_widget.pack(expand=True, fill="both")
    # Отключение возможности редактирования текста
    text_widget.config(state="disabled")

    # Добавить кнопку "Назад"
    back_button = tk.Button(content_window, text="Назад", command=go_back)
    back_button.pack()

def save_edited_table(original_df, edited_text):
    """
    Функция для сохранения отредактированной таблицы в файл

    Parameters:
    - original_df: pandas.DataFrame
        Исходная таблица данных
    - edited_text: str
        Отредактированный текст таблицы

    author: Saushkin Nikolay
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(edited_text)
            messagebox.showinfo("Файл сохранен", f"Отредактированные данные были сохранены в:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


def edit_table(df):
    """
    Функция для отображения окна с опциями редактирования таблицы

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными

    author: Saushkin Nikolay
    """
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить таблицу")
    edit_window.geometry("300x200")

    button_select_country = tk.Button(edit_window, text="Фильтровать по стране", command=lambda: show_country_window(df, get_selected_country))
    button_select_country.pack()

    button_select_score_range = tk.Button(edit_window, text="Фильтровать по диапазону баллов", command=lambda: show_score_range_window(df))
    button_select_score_range.pack()

    button_select_year = tk.Button(edit_window, text="Фильтровать по году", command=lambda: show_year_window(df, get_selected_year))
    button_select_year.pack()

    button_full_edit = tk.Button(edit_window, text="Полное редактирование", command=lambda: show_full_edit_window(df))
    button_full_edit.pack()


def get_selected_country(filtered_df, country_listbox):
    """
    Функция для фильтрации данных по выбранной стране и сохранения отфильтрованных данных в файл

    Parameters:
    - filtered_df: pandas.DataFrame
        Таблица с данными
    - country_listbox: tkinter.Listbox
        Виджет списка стран

    author: Yastrebov Arseniy
    """
    selected_country_index = country_listbox.curselection()
    if selected_country_index:
        selected_country = country_listbox.get(selected_country_index[0])
        # Создаем папку, если ее нет
        folder_path = os.path.join(os.getcwd(), selected_country)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Формируем путь к файлу
        file_path = os.path.join(folder_path, f"{selected_country}.csv")
        # Сохраняем отфильтрованные данные в CSV файл
        filtered_df.to_csv(file_path, index=False)
        messagebox.showinfo("Файл сохранен", f"Отфильтрованные данные были сохранены в:\n{file_path}")
    else:
        messagebox.showinfo("Не выбрана страна", "Пожалуйста, выберите страну.")


def get_selected_year(df, year_listbox):
    """
    Функция для фильтрации данных по выбранному году и сохранения отфильтрованных данных в файл

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными
    - year_listbox: tkinter.Listbox
        Виджет списка годов

    author: Yastrebov Arseniy
    """
    selected_index = year_listbox.curselection()
    if selected_index:
        selected_year = year_listbox.get(selected_index[0])
        # Фильтруем данные по выбранному году
        filtered_df = df[df['year'] == int(selected_year)]
        if not filtered_df.empty:
            # Создаем папку, если ее нет
            folder_path = os.path.join(os.getcwd(), "Filtered Data")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # Формируем путь к файлу
            file_path = os.path.join(folder_path, f"data_{selected_year}.csv")
            # Сохраняем отфильтрованные данные в CSV файл
            filtered_df.to_csv(file_path, index=False)
            messagebox.showinfo("Файл сохранен", f"Отфильтрованные данные были сохранены в:\n{file_path}")
            print("Selected year:", selected_year)
        else:
            messagebox.showinfo("Пустые данные", "Нет данных для выбранного года")
    else:
        print("No year selected")

def show_country_window(df, callback_function):
    """
    Функция для отображения окна выбора страны для фильтрации данных

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными
    - callback_function: function
        Функция для применения фильтрации

    author: Yastrebov Arseniy
    """
    def apply_filter():
        selected_country_index = country_listbox.curselection()
        if selected_country_index:
            selected_country = country_listbox.get(selected_country_index[0])
            filtered_df = df[df['country'] == selected_country]
            callback_function(filtered_df, country_listbox)
        else:
            messagebox.showinfo("Нет выбора", "Пожалуйста, выберите страну.")

    country_window = tk.Toplevel(root)
    country_window.title("Выберите страну")

    country_label = tk.Label(country_window, text="Выберите страну:")
    country_label.pack()

    country_listbox = tk.Listbox(country_window)
    unique_countries = df['country'].unique()
    for country in unique_countries:
        country_listbox.insert(tk.END, country)
    country_listbox.pack()

    select_button = tk.Button(country_window, text="Выбрать", command=apply_filter)
    select_button.pack()

def show_full_edit_window(df):
    """
    Функция для отображения окна полного редактирования таблицы

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными

    author: Petrunina Maria
    """
    def save_changes():
        edited_text = text_widget.get("1.0", "end")
        save_edited_table(df, edited_text)

    full_edit_window = tk.Toplevel(root)
    full_edit_window.title("Полное редактирование таблицы")
    full_edit_window.geometry("400x300")

    text_widget = tk.Text(full_edit_window, wrap="none", width=60, height=15)
    text_widget.insert("end", df.to_string(index=False))
    text_widget.pack(expand=True, fill="both")

    save_button = tk.Button(full_edit_window, text="Сохранить изменения", command=save_changes)
    save_button.pack()



def show_score_range_window(df):
    """
    Функция для отображения окна выбора диапазона баллов для фильтрации данных

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными

    author: Petrunina Maria
    """
    score_range_window = tk.Toplevel(root)
    score_range_window.title("Выбор диапазона баллов")
    score_range_window.geometry("300x150")

    min_score_label = tk.Label(score_range_window, text="Минимальный балл:")
    min_score_label.pack()
    min_score_entry = tk.Entry(score_range_window)
    min_score_entry.pack()

    max_score_label = tk.Label(score_range_window, text="Максимальный балл:")
    max_score_label.pack()
    max_score_entry = tk.Entry(score_range_window)
    max_score_entry.pack()

    apply_button = tk.Button(score_range_window, text="Применить фильтр",
                             command=lambda: apply_score_filter(df, min_score_entry.get(), max_score_entry.get()))
    apply_button.pack()


def apply_score_filter(df, min_score, max_score):
    try:
        min_score = float(min_score)
        max_score = float(max_score)
        filtered_df = df[(df['score'] >= min_score) & (df['score'] <= max_score)]
        show_table_content(filtered_df)
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректные значения баллов")


def show_year_window(df, callback_function):
    """
    Функция для отображения окна выбора года для фильтрации данных

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными
    - callback_function: function
        Функция для применения фильтрации

    author: Petrunina Maria
    """
    year_window = tk.Toplevel()
    year_window.title("Select Year")

    year_label = tk.Label(year_window, text="Select a year:")
    year_label.pack()

    year_listbox = tk.Listbox(year_window)
    unique_years = df['year'].unique()  # Corrected variable name
    for year in unique_years:
        year_listbox.insert(tk.END, year)
    year_listbox.pack()

    select_button = tk.Button(year_window, text="Select", command=lambda: callback_function(df, year_listbox))
    select_button.pack()


def show_patents_window():
    # ...
    pass


# Функция для отображения окна с выбором графика
def show_graph_options(df):
    """
    Функция для отображения окна с опциями построения графиков

    Parameters:
    - df: pandas.DataFrame
        Таблица с данными

    author: Saushkin Nikolay
    """
    graph_window = tk.Toplevel(root)
    graph_window.title("Выбор типа графика")
    graph_window.geometry("400x300")

    clustered_button = tk.Button(graph_window, text="Clustered bar chart qual qual",
                                 command=lambda: plot_clustered_bar_chart(df))
    clustered_button.place(x=50, y=50, width=300, height=35)

    categorized_histogram_button = tk.Button(graph_window, text="Categorized histogram quant qual",
                                             command=lambda: plot_categorized_histogram(df))
    categorized_histogram_button.place(x=50, y=100, width=300, height=35)

    categorized_boxplot_button = tk.Button(graph_window, text="Categorized boxplot quality education by country",
                                           command=lambda: plot_categorized_boxplot(df))
    categorized_boxplot_button.place(x=50, y=150, width=300, height=35)

    unknown_graph1_button = tk.Button(graph_window, text="Average University Score by Country",
                                      command=lambda: plot_unknown_graph1(df))
    unknown_graph1_button.place(x=50, y=200, width=300, height=35)

    unknown_graph2_button = tk.Button(graph_window, text="Pie chart qual qual",
                                      command=lambda: plot_unknown_graph2(df))
    unknown_graph2_button.place(x=50, y=250, width=300, height=35)

    scatter_plot_button = tk.Button(graph_window, text="Scatter Plot",
                                    command=lambda: plot_scatter_plot(df))
    scatter_plot_button.place(x=50, y=300, width=300, height=35)

    # Добавить кнопку "Назад"
    back_button = tk.Button(graph_window, text="Назад", command=graph_window.destroy)
    back_button.place(x=150, y=350, width=80, height=20)


# Функции для построения различных видов графиков
def plot_clustered_bar_chart(df):
    plt.figure(figsize=(10, 6))
    df.groupby('country')['national_rank'].count().plot(kind='bar')
    plt.xlabel('Country')
    plt.ylabel('Number of Universities')
    plt.title('Clustered bar chart qual qual')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('clustered_bar_chart_qual_qual.png')
    plt.show()


def plot_categorized_histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['score'], bins=10, alpha=0.5, label='Score')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Categorized histogram quant qual')
    plt.legend()
    plt.tight_layout()
    plt.savefig('categorized_histogram_quant_qual.png')
    plt.show()


def plot_categorized_boxplot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['score'])
    plt.xlabel('Score')
    plt.ylabel('Score')
    plt.title('Categorized boxplot quality education by country')
    plt.xticks([1], ['Overall'])
    plt.tight_layout()
    plt.savefig('categorized_boxplot_quality_education_by_country.png')
    plt.show()


def plot_unknown_graph1(df):
    # Группировка данных по странам и вычисление среднего рейтинга в каждой стране
    average_score_by_country = df.groupby('country')['score'].mean()

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
    plt.savefig('Average_University_Score_by_Country.png')
    plt.show()


def plot_unknown_graph2(df):
    plt.figure(figsize=(8, 8))
    df['country'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, fontsize=8)
    plt.axis('equal')
    plt.title('Pie chart qual qual')
    plt.tight_layout()
    plt.savefig('pie_chart_qual_qual.png')
    plt.show()


def plot_scatter_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot([df[df['country'] == country]['score'] for country in df['country'].unique()],
                labels=df['country'].unique(), notch=True, patch_artist=True)
    plt.xlabel('Country')
    plt.ylabel('Score')
    plt.title('Scatter Plot')
    plt.xticks(rotation=90)
    plt.tick_params(axis='both', which='major', labelsize=5)
    plt.tight_layout()
    plt.savefig('scatter_plot.png')
    plt.show()


# Функция для возврата к предыдущему действию
def go_back():
    """
    Функция для возврата на предыдущий шаг в истории действий

    author: Saushkin Nikolay
    """
    if action_history:
        action = action_history.pop()
        action()


root = tk.Tk()
root.title("Python таблицы")

# Размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Размеры окна
app_width = 400
app_height = 400

# Расчет координат для центрирования окна
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2

root.geometry(f"{app_width}x{app_height}+{x}+{y}")

# Настройки кнопки "Авторы" на главном экране
authors_button = tk.Button(root, text="Авторы", command=show_authors)
authors_button.place(x=150, y=350, width=120, height=35)

# Настройки кнопки "Работа с таблицами"
table_button = tk.Button(root, text="Работа с таблицами", command=load_table)
table_button.place(x=125, y=150, width=170, height=35)

root.mainloop()


