import pandas as pd
import os

# Get absolute path of current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to data file
data_path = os.path.join(BASE_DIR, "..", "data", "sales_data.csv")

# Load data
df = pd.read_csv(data_path)

print("Sales Data Preview:")
print(df.head())
# ---------------------------
# STEP 4: Data Cleaning
# ---------------------------

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Check for missing values
print("\nMissing values:\n", df.isnull().sum())

# Add Total_Sales column
df['Total_Sales'] = df['Quantity'] * df['Price']

# Check data types
print("\nData Types:\n", df.dtypes)

# Preview cleaned data
print("\nCleaned Data Preview:")
print(df.head())
# ---------------------------
# STEP 5: KPI Calculations
# ---------------------------

# Total Revenue
total_revenue = df['Total_Sales'].sum()

# Total Orders
total_orders = df['Order_ID'].nunique()

# Average Order Value (AOV)
avg_order_value = total_revenue / total_orders

# Top-Selling Product
top_product = (
    df.groupby('Product')['Total_Sales']
    .sum()
    .sort_values(ascending=False)
    .idxmax()
)

print("\n--- KPI DASHBOARD ---")
print(f"Total Revenue: INR {total_revenue}")
print(f"Total Orders: {total_orders}")
print(f"Average Order Value: INR {avg_order_value:.2f}")
print(f"Top-Selling Product: {top_product}")
# ---------------------------
# STEP 6: Time Intelligence
# ---------------------------

# Extract Year and Month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
# Monthly sales trend
monthly_sales = (
    df.groupby(['Year', 'Month'])['Total_Sales']
    .sum()
    .reset_index()
)

print("\nMonthly Sales Trend:")
print(monthly_sales)
import matplotlib.pyplot as plt

plt.figure()
plt.plot(monthly_sales['Month'], monthly_sales['Total_Sales'], marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)

# Save chart
plt.savefig("output/monthly_sales_trend.png")
plt.show()
# ---------------------------
# STEP 7: Category Analysis
# ---------------------------

category_sales = (
    df.groupby('Category')['Total_Sales']
    .sum()
    .reset_index()
)

print("\nCategory-wise Sales:")
print(category_sales)
plt.figure()
plt.bar(category_sales['Category'], category_sales['Total_Sales'])
plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.grid(axis='y')

plt.savefig("output/category_sales.png")
plt.show()
# ---------------------------
# STEP 7: Region Analysis
# ---------------------------

region_sales = (
    df.groupby('Region')['Total_Sales']
    .sum()
    .reset_index()
)

print("\nRegion-wise Sales:")
print(region_sales)
plt.figure()
plt.bar(region_sales['Region'], region_sales['Total_Sales'])
plt.title("Region-wise Sales")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.grid(axis='y')

plt.savefig("output/region_sales.png")
plt.show()
# ---------------------------
# STEP 8: Export Dashboard-Ready Data
# ---------------------------

dashboard_data = (
    df.groupby(['Year', 'Month', 'Region', 'Category'])['Total_Sales']
    .sum()
    .reset_index()
)

print("\nDashboard-ready data preview:")
print(dashboard_data.head())
# Export aggregated data
dashboard_data.to_csv("output/dashboard_ready_data.csv", index=False)

print("\nDashboard-ready data exported to output/dashboard_ready_data.csv")



