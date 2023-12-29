import tkinter as tk
from tkinter import ttk
import csv

columns = [
    'Model', 'Brand', 'Price', 'Gear', 'Fuel', 'Engine Displacement', 'Transmission', 'Horsepower', 'Mortgage',
    'Confiscation', 'Inspection', 'Year', 'Km', 'Area of Use', 'Colour',
    'Top Speed', 'Luggage Volume', '0-100', 'Max Torque', 'Cylinder', 'Tank', 'Consumption', 'Valve']

def converting_csv_file():
    # Specify the encoding of your text file (e.g., 'utf-8', 'latin-1', etc.)
    file_encoding = 'utf-8'

    # Open the text file for reading with the specified encoding
    with open('output.txt', 'r', encoding=file_encoding) as txt_file:
        # Read the lines from the text file
        lines = txt_file.readlines()

    # Assuming your text data has some structure, for example, tab-separated values
    # Split each line into fields based on the separator (e.g., '\t' for tab-separated)
    data = [line.strip().split('\t') for line in lines]

    # Open a CSV file for writing
    with open('output.csv', 'w', newline='', encoding=file_encoding) as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write the data to the CSV file
        csv_writer.writerows(data)

def filter_data():
    selected_brand = brand_var.get()
    selected_model = model_var.get()
    selected_year = year_var.get()

    # Get entered minimum and maximum prices
    min_price_str = min_price_entry.get().replace('₺', '').replace('.', '').replace(',', '')
    max_price_str = max_price_entry.get().replace('₺', '').replace('.', '').replace(',', '')

    try:
        # Convert cleaned price strings to float
        min_price = float(min_price_str) if min_price_str else float('-inf')
        max_price = float(max_price_str) if max_price_str else float('inf')
    except ValueError:
        # Handle the case where the entered prices are not valid floats
        treeview.delete(*treeview.get_children())  # Clear the Treeview
        treeview.insert('', 'end', values=["Invalid price values"])
        return

    # Filter by selected brand, model, and price range
    if selected_year == "All":
        filtered_cars = [car for car in data if
                         car['brand'] == selected_brand and
                         car['model'] == selected_model and
                         min_price <= float(car['price'].replace('₺', '').replace('.', '').replace(',', '')) <= max_price]
    else:
        filtered_cars = [car for car in data if
                         car['brand'] == selected_brand and
                         car['model'] == selected_model and
                         car['year'] == selected_year and
                         min_price <= float(car['price'].replace('₺', '').replace('.', '').replace(',', '')) <= max_price]

    # Cleaning UI
    for i in treeview.get_children():
        treeview.delete(i)

    # Show filtered data in columns
    if filtered_cars:
        for car in filtered_cars:
            values = [car.get(col.replace(' ', '_').lower(), '') for col in columns]
            treeview.insert('', 'end', values=values)
    else:
        # If no matching data, show a message
        treeview.insert('', 'end', values=["No matching data found"])


# Reading data from text file and neatly creating dictionary
with open('output.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

data = []
for line in lines:
    parts = line.strip().split(';')

    car = {
        'model': parts[0],
        'brand': parts[1],
        'price': parts[2],
        'gear': parts[3],
        'fuel': parts[4],
        'engine_displacement': parts[5],
        'transmission': parts[6],
        'horsepower': parts[7],
        'mortgage': parts[8],
        'confiscation': parts[9],
        'inspection': parts[10],
        'year': parts[11],
        'km': parts[12],
        'area_of_use': parts[13],
        'colour': parts[14],
        'top_speed': parts[15],
        'luggage_volume': parts[16],
        '0-100': parts[17],
        'max_torque': parts[18],
        'cylinder': parts[19],
        'tank': parts[20],
        'consumption': parts[21],
        'valve': parts[22]
    }

    data.append(car)

# Creating a TKinter window
root = tk.Tk()
root.title("Second Hand Car App")
input_frame = tk.Frame(root)
input_frame.pack()

# Brand filtering
brand = list(set(car['brand'] for car in data))
brand_var = tk.StringVar(root)
brand_var.set(brand[0])  # Select first brand initially
brand_label = tk.Label(input_frame, text="Brand:")
brand_label.pack(side=tk.LEFT)

brand_dropdown = tk.OptionMenu(input_frame, brand_var, *brand)
brand_dropdown.pack(side=tk.LEFT)

# Model filtering
model = list(set(car['model'] for car in data))
model_var = tk.StringVar(root)
model_var.set(model[0])  # Select first model initially

model_label = tk.Label(input_frame, text="Model:")
model_label.pack(side=tk.LEFT)

model_dropdown = tk.OptionMenu(input_frame, model_var, *model)
model_dropdown.pack(side=tk.LEFT)

# Year dropdown
years = list(set(car['year'] for car in data))
years.insert(0, "All")  # Eklenen satır: Tüm yılları göster
year_var = tk.StringVar(root)
year_var.set("All")  # Değişen satır: Başlangıçta "All" seçili

year_label = tk.Label(input_frame, text="Filtering Year:")
year_label.pack(side=tk.LEFT)

year_dropdown = tk.OptionMenu(input_frame, year_var, *years)
year_dropdown.pack(side=tk.LEFT)

# Price Filtering
price_label = tk.Label(input_frame, text="Price Range:")
price_label.pack(side=tk.LEFT)

min_price_label = tk.Label(input_frame, text="Min:")
min_price_label.pack(side=tk.LEFT)

min_price_entry = tk.Entry(input_frame)
min_price_entry.pack(side=tk.LEFT)

max_price_label = tk.Label(input_frame, text="Max:")
max_price_label.pack(side=tk.LEFT)

max_price_entry = tk.Entry(input_frame)
max_price_entry.pack(side=tk.LEFT)

# Filtering button
filter_button = tk.Button(input_frame, text="Filter", command=filter_data)
filter_button.pack(side=tk.LEFT)

# Set the initial size of the window and make it nearly full-screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
initial_width = int(screen_width * 0.8)
initial_height = int(screen_height * 0.8)
initial_position_x = int((screen_width - initial_width) / 2)
initial_position_y = int((screen_height - initial_height) / 2)

root.geometry(f"{initial_width}x{initial_height}+{initial_position_x}+{initial_position_y}")

# Creating a data display widget (we will use Treeview)
treeview = ttk.Treeview(root, columns=columns, show='headings')

# Adjust column headers
for col in columns:
    treeview.heading(col, text=col)
    
# Make the Treeview widget expand to fill available space
treeview.pack(expand=True, fill=tk.BOTH)
root.mainloop()
