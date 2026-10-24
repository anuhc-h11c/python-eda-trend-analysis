import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create folders for results
Path("output").mkdir(exist_ok=True)

# 1. Create a sample sales dataset
data = {
    "Date": [
        "2026-01-05", "2026-01-12", "2026-01-18",
        "2026-02-03", "2026-02-10", "2026-02-17",
        "2026-03-02", "2026-03-11", "2026-03-20",
        "2026-04-04", "2026-04-15", "2026-04-22"
    ],
    "Product": [
        "Laptop", "Phone", "Tablet", "Laptop", "Phone", None,
        "Tablet", "Laptop", "Phone", "Tablet", "Laptop", "Phone"
    ],
    "Region": [
        "North", "South", "East", "West", "North", "South",
        "East", "West", None, "North", "South", "East"
    ],
    "Sales": [
        50000, 25000, 18000, 55000, None, 22000,
        20000, 60000, 28000, 21000, 65000, 30000
    ],
    "Quantity": [2, 3, 2, 2, 4, 2, 3, 2, 4, 3, 2, 4]
}

df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])

print("=== ORIGINAL DATA ===")
print(df)

# 2. Check dataset information
print("\n=== DATASET INFORMATION ===")
df.info()

# 3. Check missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# Save missing-value summary
df.isnull().sum().to_csv("output/missing_values_summary.csv")

# 4. Clean missing values
df["Product"] = df["Product"].fillna("Unknown")
df["Region"] = df["Region"].fillna("Unknown")
df["Sales"] = df["Sales"].fillna(df["Sales"].median())

print("\n=== CLEANED DATA ===")
print(df)

# 5. Summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(df[["Sales", "Quantity"]].describe())

# 6. Analyze sales by product
product_sales = df.groupby("Product")["Sales"].sum().sort_values(
    ascending=False
)
print("\n=== SALES BY PRODUCT ===")
print(product_sales)
product_sales.to_csv("output/sales_by_product.csv")

# 7. Analyze monthly sales trends
monthly_sales = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()
monthly_sales.index = monthly_sales.index.astype(str)

print("\n=== MONTHLY SALES TRENDS ===")
print(monthly_sales)
monthly_sales.to_csv("output/monthly_sales_trend.csv")

# 8. Visualize monthly sales trends
monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/monthly_sales_trend.png")
plt.show()

# 9. Visualize sales by product
product_sales.plot(kind="bar", title="Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/sales_by_product.png")
plt.show()

# 10. Save cleaned dataset
df.to_csv("output/cleaned_sales_data.csv", index=False)

print("\nEDA completed successfully!")
print("Check the output folder for reports and charts.")