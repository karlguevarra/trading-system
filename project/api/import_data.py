import pandas as pd
from django.contrib.auth.models import User
from . models import Stock, Trade, StockInventory

# Read CSV file into a DataFrame
csv_file_path = 'csv/test.csv'
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame
for index, row in df.iterrows():
    stock_id = row['stock_id']
    quantity = row['quantity']
    is_buy = row['is_buy']
    