"""
Step 2: Clean the raw dataset.
Handles: missing values, duplicates, inconsistent casing, invalid quantities.
Outputs: data/cleaned_sales_data.csv
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("  STEP 2: DATA CLEANING")
print("=" * 60)

# ── Load raw data ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/raw_sales_data.csv")
print(f"\n📥 Loaded raw data: {df.shape[0]} rows × {df.shape[1]} columns")

# ── 1. Inspect data quality ───────────────────────────────────────────────────
print("\n── Data Quality Report (BEFORE cleaning) ──")
print(f"Duplicates:      {df.duplicated().sum()}")
print(f"Null values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"Negative Qty:    {(df['Quantity'] < 0).sum()}")
print(f"Unique Regions:  {df['Region'].dropna().unique()}")

# ── 2. Remove exact duplicates ────────────────────────────────────────────────
before = len(df)
df = df.drop_duplicates()
print(f"\n✅ Removed {before - len(df)} duplicate rows")

# ── 3. Fix inconsistent casing in Region ──────────────────────────────────────
df["Region"] = df["Region"].str.strip().str.title()
print(f"✅ Standardized Region casing → {df['Region'].dropna().unique()}")

# ── 4. Handle missing values ──────────────────────────────────────────────────
# Ship Date: fill with Order Date + 5 (median shipping days)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
mask_ship = df["Ship Date"].isnull()
df.loc[mask_ship, "Ship Date"] = df.loc[mask_ship, "Order Date"] + pd.Timedelta(days=5)
print(f"✅ Filled {mask_ship.sum()} missing Ship Dates with Order Date + 5 days")

# Segment: fill with mode
mode_segment = df["Segment"].mode()[0]
mask_seg = df["Segment"].isnull()
df["Segment"] = df["Segment"].fillna(mode_segment)
print(f"✅ Filled {mask_seg.sum()} missing Segments with mode ('{mode_segment}')")

# Region: fill with mode
mode_region = df["Region"].mode()[0]
mask_reg = df["Region"].isnull()
df["Region"] = df["Region"].fillna(mode_region)
print(f"✅ Filled {mask_reg.sum()} missing Regions with mode ('{mode_region}')")

# ── 5. Fix negative quantities ────────────────────────────────────────────────
neg_qty = df["Quantity"] < 0
df.loc[neg_qty, "Quantity"] = df.loc[neg_qty, "Quantity"].abs()
# Recalculate sales and profit for fixed rows
df.loc[neg_qty, "Sales"] = df.loc[neg_qty, "Sales"].abs()
df.loc[neg_qty, "Profit"] = df.loc[neg_qty, "Profit"].abs()
print(f"✅ Fixed {neg_qty.sum()} rows with negative quantities")

# ── 6. Add derived columns ────────────────────────────────────────────────────
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%B")
df["Day of Week"] = df["Order Date"].dt.day_name()
df["Revenue"] = df["Sales"]  # alias for clarity
df["Profit Margin (%)"] = round((df["Profit"] / df["Sales"]) * 100, 2)
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Discount Band"] = pd.cut(
    df["Discount"],
    bins=[-0.01, 0, 0.10, 0.20, 0.30, 1.0],
    labels=["No Discount", "1-10%", "11-20%", "21-30%", "31%+"]
)

print("✅ Added derived columns: Year, Month, Month Name, Day of Week, Revenue, Profit Margin, Shipping Days, Discount Band")

# ── 7. Final validation ───────────────────────────────────────────────────────
print("\n── Data Quality Report (AFTER cleaning) ──")
print(f"Total rows:      {len(df)}")
print(f"Duplicates:      {df.duplicated().sum()}")
print(f"Null values:     {df.isnull().sum().sum()}")
print(f"Negative Qty:    {(df['Quantity'] < 0).sum()}")
print(f"Date range:      {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
print(f"Regions:         {sorted(df['Region'].unique())}")
print(f"Categories:      {sorted(df['Category'].unique())}")
print(f"\nColumn dtypes:")
print(df.dtypes.to_string())

# ── 8. Save cleaned data ──────────────────────────────────────────────────────
clean_path = "data/cleaned_sales_data.csv"
df.to_csv(clean_path, index=False)
print(f"\n💾 Cleaned dataset saved to {clean_path}")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Also save to Excel for portfolio
excel_path = "data/cleaned_sales_data.xlsx"
df.to_excel(excel_path, index=False, sheet_name="Sales Data")
print(f"💾 Excel version saved to {excel_path}")

