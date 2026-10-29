"""
Step 4: Create a full visual dashboard with 8 charts.
Saves individual charts to charts/ and a combined dashboard image.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# ── Style Setup ────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", font_scale=1.1)
PALETTE = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]

df = pd.read_csv("data/cleaned_sales_data.csv", parse_dates=["Order Date", "Ship Date"])

print("🎨 Generating dashboard charts...\n")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1: Revenue by Category (Horizontal Bar)
# ═══════════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(8, 5))
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values()
bars = ax1.barh(cat_rev.index, cat_rev.values, color=PALETTE[:len(cat_rev)], edgecolor="white")
ax1.set_xlabel("Total Revenue ($)")
ax1.set_title("Revenue by Category", fontsize=14, fontweight="bold")
for bar, val in zip(bars, cat_rev.values):
    ax1.text(val + cat_rev.max()*0.01, bar.get_y() + bar.get_height()/2,
             f"${val:,.0f}", va="center", fontsize=10)
ax1.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
plt.tight_layout()
fig1.savefig("charts/01_revenue_by_category.png", dpi=150, bbox_inches="tight")
print("✅ Chart 1: Revenue by Category")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2: Top 10 Products by Revenue
# ═══════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(10, 6))
top_prod = df.groupby("Sub-Category")["Revenue"].sum().sort_values(ascending=True).tail(10)
bars2 = ax2.barh(top_prod.index, top_prod.values, color=sns.color_palette("viridis", 10))
ax2.set_xlabel("Total Revenue ($)")
ax2.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
for bar, val in zip(bars2, top_prod.values):
    ax2.text(val + top_prod.max()*0.01, bar.get_y() + bar.get_height()/2,
             f"${val:,.0f}", va="center", fontsize=9)
ax2.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
plt.tight_layout()
fig2.savefig("charts/02_top10_products.png", dpi=150, bbox_inches="tight")
print("✅ Chart 2: Top 10 Products")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3: Monthly Revenue Trend (Line)
# ═══════════════════════════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(12, 5))
df["YearMonth"] = df["Order Date"].dt.to_period("M")
monthly_rev = df.groupby("YearMonth")["Revenue"].sum().reset_index()
monthly_rev["YearMonth"] = monthly_rev["YearMonth"].dt.to_timestamp()
ax3.plot(monthly_rev["YearMonth"], monthly_rev["Revenue"], color="#2196F3", linewidth=2, marker="o", markersize=3)
ax3.fill_between(monthly_rev["YearMonth"], monthly_rev["Revenue"], alpha=0.15, color="#2196F3")
ax3.set_xlabel("Month")
ax3.set_ylabel("Revenue ($)")
ax3.set_title("Monthly Revenue Trend (2021–2024)", fontsize=14, fontweight="bold")
ax3.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
plt.xticks(rotation=45)
plt.tight_layout()
fig3.savefig("charts/03_monthly_revenue_trend.png", dpi=150, bbox_inches="tight")
print("✅ Chart 3: Monthly Revenue Trend")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4: Revenue by Region (Pie + Bar)
# ═══════════════════════════════════════════════════════════════════════════════
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(13, 5))
region_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
# Pie
ax4a.pie(region_rev.values, labels=region_rev.index, autopct="%1.1f%%",
         colors=PALETTE[:len(region_rev)], startangle=140, textprops={"fontsize": 11})
ax4a.set_title("Revenue Share by Region", fontsize=13, fontweight="bold")
# Profit bar
region_profit = df.groupby("Region")["Profit"].sum().reindex(region_rev.index)
bars4 = ax4b.bar(region_profit.index, region_profit.values, color=PALETTE[:len(region_profit)], edgecolor="white")
ax4b.set_ylabel("Total Profit ($)")
ax4b.set_title("Profit by Region", fontsize=13, fontweight="bold")
ax4b.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
for bar, val in zip(bars4, region_profit.values):
    ax4b.text(bar.get_x() + bar.get_width()/2, val + region_profit.max()*0.02,
              f"${val:,.0f}", ha="center", fontsize=9)
plt.tight_layout()
fig4.savefig("charts/04_regional_performance.png", dpi=150, bbox_inches="tight")
print("✅ Chart 4: Regional Performance")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5: Discount Impact on Profit Margin (Box Plot)
# ═══════════════════════════════════════════════════════════════════════════════
fig5, ax5 = plt.subplots(figsize=(10, 5))
order = ["No Discount", "1-10%", "11-20%", "21-30%", "31%+"]
sns.boxplot(data=df, x="Discount Band", y="Profit Margin (%)", order=order,
            palette="RdYlGn_r", ax=ax5, showfliers=False)
ax5.axhline(y=0, color="red", linestyle="--", alpha=0.5, label="Break-even")
ax5.set_title("Discount Impact on Profit Margin", fontsize=14, fontweight="bold")
ax5.set_xlabel("Discount Band")
ax5.legend()
plt.tight_layout()
fig5.savefig("charts/05_discount_vs_profit.png", dpi=150, bbox_inches="tight")
print("✅ Chart 5: Discount vs Profit Margin")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 6: Revenue by Segment (Donut)
# ═══════════════════════════════════════════════════════════════════════════════
fig6, ax6 = plt.subplots(figsize=(7, 7))
seg_rev = df.groupby("Segment")["Revenue"].sum().sort_values(ascending=False)
wedges, texts, autotexts = ax6.pie(
    seg_rev.values, labels=seg_rev.index, autopct="%1.1f%%",
    colors=["#2196F3", "#4CAF50", "#FF9800"], startangle=90,
    pctdistance=0.82, textprops={"fontsize": 12}
)
centre_circle = plt.Circle((0, 0), 0.60, fc="white")
ax6.add_artist(centre_circle)
ax6.set_title("Revenue by Customer Segment", fontsize=14, fontweight="bold")
# Center text
total = seg_rev.sum()
ax6.text(0, 0, f"Total\n${total:,.0f}", ha="center", va="center", fontsize=13, fontweight="bold")
plt.tight_layout()
fig6.savefig("charts/06_segment_donut.png", dpi=150, bbox_inches="tight")
print("✅ Chart 6: Segment Donut")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 7: Average Profit Margin by Category × Discount Band (Heatmap)
# ═══════════════════════════════════════════════════════════════════════════════
fig7, ax7 = plt.subplots(figsize=(10, 5))
pivot = df.pivot_table(index="Category", columns="Discount Band",
                       values="Profit Margin (%)", aggfunc="mean",
                       observed=True)
pivot = pivot.reindex(columns=order)
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn", center=0,
            linewidths=1, ax=ax7, cbar_kws={"label": "Avg Profit Margin (%)"})
ax7.set_title("Profit Margin by Category × Discount Band", fontsize=14, fontweight="bold")
plt.tight_layout()
fig7.savefig("charts/07_category_discount_heatmap.png", dpi=150, bbox_inches="tight")
print("✅ Chart 7: Category × Discount Heatmap")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 8: Year-over-Year Revenue & Profit (Grouped Bar)
# ═══════════════════════════════════════════════════════════════════════════════
fig8, ax8 = plt.subplots(figsize=(9, 5))
yoy = df.groupby("Year").agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum")).reset_index()
x = np.arange(len(yoy))
width = 0.35
b1 = ax8.bar(x - width/2, yoy["Revenue"], width, label="Revenue", color="#2196F3", edgecolor="white")
b2 = ax8.bar(x + width/2, yoy["Profit"], width, label="Profit", color="#4CAF50", edgecolor="white")
ax8.set_xlabel("Year")
ax8.set_ylabel("Amount ($)")
ax8.set_title("Year-over-Year Revenue & Profit", fontsize=14, fontweight="bold")
ax8.set_xticks(x)
ax8.set_xticklabels(yoy["Year"].astype(int))
ax8.legend()
ax8.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
for bar in b1:
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f"${bar.get_height()/1000:.0f}K", ha="center", va="bottom", fontsize=9)
for bar in b2:
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f"${bar.get_height()/1000:.0f}K", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
fig8.savefig("charts/08_yoy_revenue_profit.png", dpi=150, bbox_inches="tight")
print("✅ Chart 8: Year-over-Year Revenue & Profit")


# ═══════════════════════════════════════════════════════════════════════════════
# COMBINED DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
print("\n🖼️  Assembling combined dashboard...")

fig, axes = plt.subplots(2, 4, figsize=(28, 12))
fig.suptitle("RETAIL SALES ANALYTICS DASHBOARD", fontsize=22, fontweight="bold", y=1.02)

# Row 1
# 1 - Category Revenue
cat_rev_s = df.groupby("Category")["Revenue"].sum().sort_values()
axes[0,0].barh(cat_rev_s.index, cat_rev_s.values, color=PALETTE[:len(cat_rev_s)])
axes[0,0].set_title("Revenue by Category", fontweight="bold")
axes[0,0].xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))

# 2 - Top 5 Products
top5 = df.groupby("Sub-Category")["Revenue"].sum().sort_values(ascending=True).tail(5)
axes[0,1].barh(top5.index, top5.values, color=sns.color_palette("viridis", 5))
axes[0,1].set_title("Top 5 Products", fontweight="bold")
axes[0,1].xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))

# 3 - Monthly Trend
axes[0,2].plot(monthly_rev["YearMonth"], monthly_rev["Revenue"], color="#2196F3", linewidth=1.5)
axes[0,2].fill_between(monthly_rev["YearMonth"], monthly_rev["Revenue"], alpha=0.15, color="#2196F3")
axes[0,2].set_title("Monthly Revenue Trend", fontweight="bold")
axes[0,2].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
axes[0,2].tick_params(axis="x", rotation=45)

# 4 - Region Pie
axes[0,3].pie(region_rev.values, labels=region_rev.index, autopct="%1.1f%%",
              colors=PALETTE[:len(region_rev)], startangle=140, textprops={"fontsize": 9})
axes[0,3].set_title("Revenue by Region", fontweight="bold")

# Row 2
# 5 - Discount Box
sns.boxplot(data=df, x="Discount Band", y="Profit Margin (%)", order=order,
            palette="RdYlGn_r", ax=axes[1,0], showfliers=False)
axes[1,0].axhline(y=0, color="red", linestyle="--", alpha=0.5)
axes[1,0].set_title("Discount vs Profit Margin", fontweight="bold")
axes[1,0].tick_params(axis="x", rotation=30)

# 6 - Segment Donut
wedges, texts, autotexts = axes[1,1].pie(
    seg_rev.values, labels=seg_rev.index, autopct="%1.1f%%",
    colors=["#2196F3", "#4CAF50", "#FF9800"], startangle=90,
    pctdistance=0.82, textprops={"fontsize": 9})
centre = plt.Circle((0, 0), 0.60, fc="white")
axes[1,1].add_artist(centre)
axes[1,1].set_title("Revenue by Segment", fontweight="bold")

# 7 - Heatmap
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn", center=0,
            linewidths=0.5, ax=axes[1,2], cbar_kws={"label": "Margin %", "shrink": 0.8})
axes[1,2].set_title("Category × Discount Margin", fontweight="bold")

# 8 - YoY
x = np.arange(len(yoy))
axes[1,3].bar(x - 0.175, yoy["Revenue"], 0.35, label="Revenue", color="#2196F3")
axes[1,3].bar(x + 0.175, yoy["Profit"], 0.35, label="Profit", color="#4CAF50")
axes[1,3].set_xticks(x)
axes[1,3].set_xticklabels(yoy["Year"].astype(int))
axes[1,3].set_title("YoY Revenue & Profit", fontweight="bold")
axes[1,3].legend(fontsize=8)
axes[1,3].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))

plt.tight_layout()
fig.savefig("charts/00_DASHBOARD.png", dpi=150, bbox_inches="tight")
print("✅ Combined dashboard saved to charts/00_DASHBOARD.png")

plt.close("all")
print("\n🎉 All 8 charts + dashboard generated in charts/ folder!")

