from flask import Flask, render_template, request
import pandas as pd
import re

# Initialize the Flask app
app = Flask(__name__)

# Load the dataset
df = pd.read_csv('house_rent_mumbai.csv')

# Function to convert price strings to numeric
def convert_price(price_str):
    # Remove commas
    price_str = price_str.replace(',', '')
    
    # Convert lakhs to numeric
    if 'L' in price_str:
        return float(price_str.replace('L', '').strip()) * 100000  # 1 Lakh = 100,000
    
    # Convert crores to numeric
    if 'Cr' in price_str:
        return float(price_str.replace('Cr', '').strip()) * 10000000  # 1 Crore = 10,000,000
    
    # If it's just a number, return it as float
    return float(price_str)

# Apply the conversion to the 'price' column
df['price'] = df['price'].apply(convert_price)

# Clean and process the dataset
df['area'] = pd.to_numeric(df['area'], errors='coerce')  # Convert area to numeric
df['size'] = pd.to_numeric(df['size'], errors='coerce')  # Convert size (BHK) to numeric

# Remove any rows with missing values in important columns
df.dropna(subset=['size', 'price', 'area', 'location'], inplace=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Get user input from the form
    size = int(request.form['bhk'])  # Using 'size' instead of 'BHK'
    location = request.form['location']
    price_range = int(request.form['price'])
    area_range = int(request.form['area'])

    # Define price ranges
    if price_range == 1:
        price_min, price_max = 0, 20000
    elif price_range == 2:
        price_min, price_max = 20000, 40000
    else:
        price_min, price_max = 40000, float('inf')

    # Define area ranges
    if area_range == 1:
        area_min, area_max = 0, 500
    elif area_range == 2:
        area_min, area_max = 500, 1000
    else:
        area_min, area_max = 1000, float('inf')

    # Filter the dataset based on user input
    filtered_houses = df[
        (df['size'] == size) &
        (df['location'].str.contains(location, case=False)) &
        (df['price'] >= price_min) & (df['price'] <= price_max) &
        (df['area'] >= area_min) & (df['area'] <= area_max)
    ]

    # If no matches found, show a message
    if filtered_houses.empty:
        return "<h2>No houses match your criteria.</h2>"

    # Pass the filtered data to the template
    html_table = filtered_houses.to_html(classes='styled-table', index=False).strip()

    return render_template('results.html', tables=html_table)

if __name__ == '__main__':
    app.run(debug=True)
