import pandas as pd
import os
import matplotlib.pyplot as plt

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "..", "data", "sales_data.csv")
output_dir = os.path.join(BASE_DIR, "..", "output")

# Create output folder if not exists
os.makedirs(output_dir, exist_ok=True)

# LOAD DATA
df = pd.read_csv(data_path)

print("Sales Data Preview:")
print(df.head())

# STEP 4: DATA CLEANING

df['Date'] = pd.to_datetime(df['Date'])
df['Total_Sales'] = df['Quantity'] * df['Price']

print("\nMissing values:\n", df.isnull().sum())
print("\nData Types:\n", df.dtypes)

# STEP 5: KPI CALCULATIONS

total_revenue = df['Total_Sales'].sum()
total_orders = df['Order_ID'].nunique()
avg_order_value = total_revenue / total_orders

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

# STEP 6: TIME INTELLIGENCE

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

monthly_sales = (
    df.groupby(['Year', 'Month'])['Total_Sales']
    .sum()
    .reset_index()
)

print("\nMonthly Sales Trend:")
print(monthly_sales)


# STEP 7: CATEGORY & REGION ANALYSIS

category_sales = (
    df.groupby('Category')['Total_Sales']
    .sum()
    .reset_index()
)

region_sales = (
    df.groupby('Region')['Total_Sales']
    .sum()
    .reset_index()
)

print("\nCategory-wise Sales:")
print(category_sales)

print("\nRegion-wise Sales:")
print(region_sales)

# DASHBOARD: ALL GRAPHS TOGETHER


plt.figure(figsize=(15, 8))

# 1️ Monthly Sales Trend
plt.subplot(2, 2, 1)
plt.plot(monthly_sales['Month'], monthly_sales['Total_Sales'], marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)

# 2️ Category-wise Sales
plt.subplot(2, 2, 2)
plt.bar(category_sales['Category'], category_sales['Total_Sales'])
plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Total Sales")

# 3️ Region-wise Sales
plt.subplot(2, 2, 3)
plt.bar(region_sales['Region'], region_sales['Total_Sales'])
plt.title("Region-wise Sales")
plt.xlabel("Region")
plt.ylabel("Total Sales")

plt.tight_layout()

# Save combined dashboard
plt.savefig(os.path.join(output_dir, "sales_dashboard.png"))

# Show all charts at once
plt.show()

# STEP 8: EXPORT DASHBOARD-READY DATA

dashboard_data = (
    df.groupby(['Year', 'Month', 'Region', 'Category'])['Total_Sales']
    .sum()
    .reset_index()
)

print("\nDashboard-ready data preview:")
print(dashboard_data.head())

dashboard_data.to_csv(
    os.path.join(output_dir, "dashboard_ready_data.csv"),
    index=False
)

print("\nDashboard-ready data exported to output/dashboard_ready_data.csv")
