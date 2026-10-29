"""
Step 1: Generate a realistic retail sales dataset.
This simulates a public retail sales dataset with realistic patterns:
- Seasonal trends (holiday spikes)
- Regional variation
- Category-specific margins
- Discount effects on profit
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
N_ORDERS = 9800  # total order line-items

REGIONS = ["East", "West", "South", "Central"]
STATES = {
    "East":    ["New York", "Pennsylvania", "Massachusetts", "New Jersey", "Connecticut"],
    "West":    ["California", "Washington", "Oregon", "Colorado", "Arizona"],
    "South":   ["Texas", "Florida", "Georgia", "North Carolina", "Virginia"],
    "Central": ["Illinois", "Ohio", "Michigan", "Minnesota", "Indiana"],
}

CATEGORIES = {
    "Technology": {
        "products": [
            ("Laptop", 600, 1200), ("Smartphone", 300, 900), ("Tablet", 200, 600),
            ("Monitor", 150, 500), ("Keyboard", 20, 80), ("Mouse", 10, 50),
            ("Headphones", 30, 200), ("Printer", 80, 400), ("Webcam", 30, 120),
            ("External SSD", 50, 200),
        ],
        "base_margin": 0.18,
    },
    "Furniture": {
        "products": [
            ("Office Chair", 100, 500), ("Desk", 150, 700), ("Bookcase", 80, 350),
            ("Filing Cabinet", 60, 250), ("Table", 100, 400), ("Chair Mat", 20, 80),
            ("Standing Desk", 250, 800), ("Sofa", 200, 900),
        ],
        "base_margin": 0.12,
    },
    "Office Supplies": {
        "products": [
            ("Paper", 5, 30), ("Pens", 2, 15), ("Binders", 3, 20),
            ("Envelopes", 3, 15), ("Stapler", 5, 25), ("Tape", 2, 10),
            ("Markers", 3, 18), ("Notebooks", 3, 20), ("Scissors", 3, 12),
            ("Labels", 3, 25), ("Folders", 2, 12),
        ],
        "base_margin": 0.35,
    },
    "Clothing": {
        "products": [
            ("T-Shirt", 10, 40), ("Jacket", 40, 150), ("Jeans", 25, 80),
            ("Sneakers", 30, 120), ("Dress Shirt", 20, 70), ("Sweater", 25, 90),
            ("Hat", 8, 30), ("Scarf", 10, 40),
        ],
        "base_margin": 0.45,
    },
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

# ── Helpers ────────────────────────────────────────────────────────────────────
def seasonal_weight(month):
    """Return a multiplier for order volume by month (holiday / back-to-school spikes)."""
    weights = {1: 0.7, 2: 0.65, 3: 0.8, 4: 0.85, 5: 0.9, 6: 0.95,
               7: 1.0, 8: 1.05, 9: 1.15, 10: 1.1, 11: 1.35, 12: 1.5}
    return weights[month]


def generate_order_date(year_range=(2021, 2024)):
    """Pick a random date weighted by seasonal pattern."""
    year = random.randint(*year_range)
    month = random.choices(range(1, 13), weights=[seasonal_weight(m) for m in range(1, 13)])[0]
    day = random.randint(1, 28)  # avoid month-boundary issues
    return datetime(year, month, day)


# ── Generate Data ──────────────────────────────────────────────────────────────
rows = []
order_id_counter = 100001

for i in range(N_ORDERS):
    # Order metadata
    order_date = generate_order_date()
    ship_days = {"Standard Class": random.randint(3, 7),
                 "Second Class": random.randint(2, 4),
                 "First Class": random.randint(1, 2),
                 "Same Day": 0}
    ship_mode = random.choices(SHIP_MODES, weights=[0.55, 0.20, 0.15, 0.10])[0]
    ship_date = order_date + timedelta(days=ship_days[ship_mode])

    region = random.choices(REGIONS, weights=[0.30, 0.28, 0.25, 0.17])[0]
    state = random.choice(STATES[region])
    segment = random.choices(SEGMENTS, weights=[0.50, 0.32, 0.18])[0]

    # Product
    category = random.choices(
        list(CATEGORIES.keys()),
        weights=[0.30, 0.22, 0.33, 0.15]
    )[0]
    cat_info = CATEGORIES[category]
    product_name, price_lo, price_hi = random.choice(cat_info["products"])

    quantity = random.choices([1, 2, 3, 4, 5, 6, 7, 8],
                              weights=[0.35, 0.25, 0.15, 0.10, 0.06, 0.04, 0.03, 0.02])[0]
    unit_price = round(random.uniform(price_lo, price_hi), 2)
    sales = round(unit_price * quantity, 2)

    # Discount (0 – 50 %, skewed toward 0)
    discount = random.choices(
        [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
        weights=[0.40, 0.12, 0.12, 0.08, 0.08, 0.06, 0.05, 0.03, 0.03, 0.02, 0.01]
    )[0]

    discounted_sales = round(sales * (1 - discount), 2)

    # Profit: base margin eroded by discount
    effective_margin = cat_info["base_margin"] - (discount * 0.6)  # discounts eat into margin
    profit = round(discounted_sales * effective_margin, 2)

    # Introduce some realistic noise
    profit += round(random.gauss(0, sales * 0.02), 2)  # small random variance

    # Order ID (group ~1-4 items per order)
    if i % random.randint(1, 4) == 0:
        order_id_counter += 1
    order_id = f"ORD-{order_id_counter}"

    rows.append({
        "Order ID":      order_id,
        "Order Date":    order_date.strftime("%Y-%m-%d"),
        "Ship Date":     ship_date.strftime("%Y-%m-%d"),
        "Ship Mode":     ship_mode,
        "Customer ID":   f"CUST-{random.randint(1000, 3500)}",
        "Segment":       segment,
        "Region":        region,
        "State":         state,
        "Category":      category,
        "Sub-Category":  product_name,
        "Product Name":  f"{product_name} - Model {random.choice('ABCDEFGH')}{random.randint(100,999)}",
        "Quantity":      quantity,
        "Unit Price":    unit_price,
        "Discount":      discount,
        "Sales":         discounted_sales,
        "Profit":        profit,
    })

df = pd.DataFrame(rows)

# ── Inject realistic data-quality issues (for cleaning practice) ───────────────
# 1. ~2 % missing values in some columns
for col in ["Ship Date", "Segment", "Region"]:
    mask = np.random.random(len(df)) < 0.02
    df.loc[mask, col] = np.nan

# 2. Duplicate ~1 % of rows
dup_idx = df.sample(frac=0.01, random_state=1).index
df = pd.concat([df, df.loc[dup_idx]], ignore_index=True)

# 3. Some inconsistent casing in Region
flip_mask = np.random.random(len(df)) < 0.03
df.loc[flip_mask, "Region"] = df.loc[flip_mask, "Region"].apply(
    lambda x: x.upper() if pd.notna(x) else x
)

# 4. A few negative quantities (data entry errors)
err_mask = np.random.random(len(df)) < 0.005
df.loc[err_mask, "Quantity"] = -df.loc[err_mask, "Quantity"]

# Shuffle
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

# Save raw dataset
raw_path = "data/raw_sales_data.csv"
df.to_csv(raw_path, index=False)
print(f"✅ Raw dataset saved to {raw_path}")
print(f"   Shape: {df.shape}")
print(f"   Columns: {list(df.columns)}")
print(f"\n   Null counts:\n{df.isnull().sum()}")
print(f"\n   Sample rows:")
print(df.head(5).to_string())

