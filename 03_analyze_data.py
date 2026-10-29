"""
Step 3: Analyze the data and answer the 5 key business questions.
Produces summary tables printed to console.
"""

import pandas as pd
import numpy as np

print("=" * 70)
print("  STEP 3: SALES DATA ANALYSIS — KEY BUSINESS QUESTIONS")
print("=" * 70)

df = pd.read_csv("data/cleaned_sales_data.csv", parse_dates=["Order Date", "Ship Date"])

# ═══════════════════════════════════════════════════════════════════════════════
# Q1: Which products and categories sell best?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("Q1: BEST-SELLING PRODUCTS & CATEGORIES")
print("─" * 70)

# By Category
cat_summary = df.groupby("Category").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Order_Count=("Order ID", "nunique"),
    Avg_Profit_Margin=("Profit Margin (%)", "mean"),
).sort_values("Total_Revenue", ascending=False)
cat_summary["Revenue_Share_%"] = round(cat_summary["Total_Revenue"] / cat_summary["Total_Revenue"].sum() * 100, 1)
print("\n📊 Category Performance:")
print(cat_summary.to_string())

# Top 10 Products by Revenue
top_products = df.groupby("Sub-Category").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Avg_Unit_Price=("Unit Price", "mean"),
    Total_Quantity=("Quantity", "sum"),
).sort_values("Total_Revenue", ascending=False).head(10)
print("\n📊 Top 10 Products (Sub-Categories) by Revenue:")
print(top_products.to_string())

# ═══════════════════════════════════════════════════════════════════════════════
# Q2: Which months have the highest revenue?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("Q2: MONTHLY REVENUE TRENDS")
print("─" * 70)

monthly = df.groupby(["Year", "Month", "Month Name"]).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
).reset_index()

# Average by month across years
avg_monthly = df.groupby(["Month", "Month Name"]).agg(
    Avg_Revenue=("Revenue", "sum"),
    Avg_Profit=("Profit", "sum"),
).reset_index()
# Divide by number of years
n_years = df["Year"].nunique()
avg_monthly["Avg_Revenue"] = round(avg_monthly["Avg_Revenue"] / n_years, 2)
avg_monthly["Avg_Profit"] = round(avg_monthly["Avg_Profit"] / n_years, 2)
avg_monthly = avg_monthly.sort_values("Month")
print("\n📊 Average Monthly Performance (across all years):")
print(avg_monthly.to_string(index=False))

# Year-over-Year
yoy = df.groupby("Year").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
).reset_index()
print("\n📊 Year-over-Year Summary:")
print(yoy.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════════════
# Q3: Which regions perform well?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("Q3: REGIONAL PERFORMANCE")
print("─" * 70)

region_summary = df.groupby("Region").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Avg_Order_Value=("Revenue", "mean"),
    Order_Count=("Order ID", "nunique"),
    Avg_Profit_Margin=("Profit Margin (%)", "mean"),
).sort_values("Total_Revenue", ascending=False)
region_summary["Revenue_Share_%"] = round(region_summary["Total_Revenue"] / region_summary["Total_Revenue"].sum() * 100, 1)
print("\n📊 Regional Performance:")
print(region_summary.to_string())

# Top States
state_summary = df.groupby(["Region", "State"]).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
).sort_values("Revenue", ascending=False).head(10)
print("\n📊 Top 10 States by Revenue:")
print(state_summary.to_string())

# ═══════════════════════════════════════════════════════════════════════════════
# Q4: What is the average order value?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("Q4: AVERAGE ORDER VALUE (AOV)")
print("─" * 70)

order_totals = df.groupby("Order ID").agg(
    Order_Revenue=("Revenue", "sum"),
    Order_Profit=("Profit", "sum"),
    Items=("Quantity", "sum"),
).reset_index()

print(f"\n📊 Overall AOV: ${order_totals['Order_Revenue'].mean():,.2f}")
print(f"   Median Order Value: ${order_totals['Order_Revenue'].median():,.2f}")
print(f"   Avg Items per Order: {order_totals['Items'].mean():.1f}")

aov_segment = df.groupby("Segment").apply(
    lambda g: g.groupby("Order ID")["Revenue"].sum().mean()
).reset_index(name="AOV")
print(f"\n📊 AOV by Segment:")
print(aov_segment.to_string(index=False))

aov_category = df.groupby("Category").apply(
    lambda g: g.groupby("Order ID")["Revenue"].sum().mean()
).reset_index(name="AOV")
print(f"\n📊 AOV by Category:")
print(aov_category.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════════════
# Q5: Are discounts improving or hurting profit?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("Q5: DISCOUNT IMPACT ON PROFIT")
print("─" * 70)

discount_analysis = df.groupby("Discount Band", observed=True).agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Profit=("Profit", "sum"),
    Order_Count=("Order ID", "count"),
    Avg_Profit_Margin=("Profit Margin (%)", "mean"),
    Avg_Discount=("Discount", "mean"),
).reset_index()
discount_analysis["Profit_per_Dollar_Revenue"] = round(
    discount_analysis["Total_Profit"] / discount_analysis["Total_Revenue"], 4
)
print("\n📊 Discount Band Analysis:")
print(discount_analysis.to_string(index=False))

# Correlation
corr_disc_profit = df["Discount"].corr(df["Profit Margin (%)"])
print(f"\n📊 Correlation (Discount vs Profit Margin): {corr_disc_profit:.4f}")

# Category × Discount interaction
cat_disc = df.groupby(["Category", "Discount Band"], observed=True).agg(
    Avg_Margin=("Profit Margin (%)", "mean"),
    Revenue=("Revenue", "sum"),
).reset_index()
print("\n📊 Category × Discount Band — Avg Profit Margin (%):")
pivot = cat_disc.pivot_table(index="Category", columns="Discount Band", values="Avg_Margin")
print(pivot.to_string())

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Segment & Ship Mode Analysis
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "─" * 70)
print("BONUS: SEGMENT & SHIPPING ANALYSIS")
print("─" * 70)

seg = df.groupby("Segment").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Avg_Margin=("Profit Margin (%)", "mean"),
    Orders=("Order ID", "nunique"),
).sort_values("Revenue", ascending=False)
print("\n📊 Segment Performance:")
print(seg.to_string())

ship = df.groupby("Ship Mode").agg(
    Revenue=("Revenue", "sum"),
    Avg_Ship_Days=("Shipping Days", "mean"),
    Orders=("Order ID", "nunique"),
).sort_values("Revenue", ascending=False)
print("\n📊 Ship Mode Analysis:")
print(ship.to_string())

print("\n\n✅ Analysis complete!")

