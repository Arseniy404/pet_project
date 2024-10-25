import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def filter_data_and_save_by_country(df, country, output_filename):
    filtered_data = df[df['country'] == country]
    filtered_data.to_csv(output_filename, index=False)
    messagebox.showinfo("Success", f"Filtered data saved to {output_filename}")

def filter_data_and_save_by_score(df, min_score, max_score, output_filename):
    filtered_data = df[(df['score'] >= min_score) & (df['score'] <= max_score)]
    filtered_data.to_csv(output_filename, index=False)
    messagebox.showinfo("Success", f"Filtered data saved to {output_filename}")

def filter_data_and_save_by_year(df, year, output_filename):
    filtered_data = df[df['year'] == int(year)]
    filtered_data.to_csv(output_filename, index=False)
    return output_filename  # Return the filename instead

def get_selected_year(year_listbox):
    selected_year = year_listbox.get(tk.ACTIVE)
    output_filename = os.path.join(new_directory, f"{selected_year}_universities.csv")
    filtered_filename = filter_data_and_save_by_year(data, selected_year, output_filename)
    messagebox.showinfo("Success", f"Filtered data saved to {filtered_filename}")  # Show messagebox with filtered filename

def filter_data_and_save_by_patents(df, min_patents, max_patents, output_filename):
    filtered_data = df[(df['patents'] >= min_patents) & (df['patents'] <= max_patents)]
    filtered_data.to_csv(output_filename, index=False)
    messagebox.showinfo("Success", f"Filtered data saved to {output_filename}")

def create_gui():
    root = tk.Tk()
    root.title("Filter Data")

    button_select_country = tk.Button(root, text="Filter by Country", command=show_country_window)
    button_select_country.pack()

    button_select_score_range = tk.Button(root, text="Filter by Score Range", command=show_score_range_window)
    button_select_score_range.pack()

    button_select_year = tk.Button(root, text="Filter by Year", command=show_year_window)
    button_select_year.pack()

    button_select_patents = tk.Button(root, text="Filter by Patents", command=show_patents_window)
    button_select_patents.pack()

    root.mainloop()

def show_country_window():
    country_window = tk.Toplevel()
    country_window.title("Select Country")

    country_label = tk.Label(country_window, text="Select a country:")
    country_label.pack()

    country_listbox = tk.Listbox(country_window)
    unique_countries = data['country'].unique()
    for country in unique_countries:
        country_listbox.insert(tk.END, country)
    country_listbox.pack()

    select_button = tk.Button(country_window, text="Select", command=lambda: get_selected_country(country_listbox))
    select_button.pack()

def get_selected_country(country_listbox):
    selected_country = country_listbox.get(tk.ACTIVE)
    output_filename = os.path.join(new_directory, f"{selected_country}_universities.csv")
    filter_data_and_save_by_country(data, selected_country, output_filename)

def show_score_range_window():
    score_range_window = tk.Toplevel()
    score_range_window.title("Filter by Score Range")

    label_min_score = tk.Label(score_range_window, text="Min Score:")
    label_min_score.pack()

    entry_min_score = tk.Entry(score_range_window)
    entry_min_score.pack()

    label_max_score = tk.Label(score_range_window, text="Max Score:")
    label_max_score.pack()

    entry_max_score = tk.Entry(score_range_window)
    entry_max_score.pack()

    apply_button = tk.Button(score_range_window, text="Apply", command=lambda: apply_score_range_filter(entry_min_score, entry_max_score))
    apply_button.pack()

def apply_score_range_filter(entry_min_score, entry_max_score):
    min_score = float(entry_min_score.get())
    max_score = float(entry_max_score.get())
    output_filename = os.path.join(new_directory, f"Score_{min_score}_to_{max_score}.csv")
    filter_data_and_save_by_score(data, min_score, max_score, output_filename)

def show_year_window():
    year_window = tk.Toplevel()
    year_window.title("Select Year")

    year_label = tk.Label(year_window, text="Select a year:")
    year_label.pack()

    year_listbox = tk.Listbox(year_window)
    unique_years = data['year'].unique()
    for year in unique_years:
        year_listbox.insert(tk.END, year)
    year_listbox.pack()

    select_button = tk.Button(year_window, text="Select", command=lambda: get_selected_year(year_listbox))
    select_button.pack()

def show_patents_window():
    patents_window = tk.Toplevel()
    patents_window.title("Filter by Patents")

    label_min_patents = tk.Label(patents_window, text="Min Patents:")
    label_min_patents.pack()

    entry_min_patents = tk.Entry(patents_window)
    entry_min_patents.pack()

    label_max_patents = tk.Label(patents_window, text="Max Patents:")
    label_max_patents.pack()

    entry_max_patents = tk.Entry(patents_window)
    entry_max_patents.pack()

    apply_button = tk.Button(patents_window, text="Apply", command=lambda: apply_patents_filter(entry_min_patents, entry_max_patents))
    apply_button.pack()

def apply_patents_filter(entry_min_patents, entry_max_patents):
    min_patents = int(entry_min_patents.get())
    max_patents = int(entry_max_patents.get())
    output_filename = os.path.join(new_directory, f"Patents_{min_patents}_to_{max_patents}.csv")
    filter_data_and_save_by_patents(data, min_patents, max_patents, output_filename)

if __name__ == "__main__":
    new_directory = os.path.join('..', 'Ouput')
    dataset_directory = os.path.join('..', 'Data', 'cwurData.csv')

    # Load data
    data = pd.read_csv(dataset_directory)

    create_gui()
