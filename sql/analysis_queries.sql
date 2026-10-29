-- ═══════════════════════════════════════════════════════════════════════════
-- SQL Queries for Sales Data Analysis
-- Compatible with: SQLite, PostgreSQL, MySQL
-- Table: sales (matches cleaned_sales_data.csv)
-- ═══════════════════════════════════════════════════════════════════════════

-- ─── SETUP: Create table and load data (SQLite example) ──────────────────
-- sqlite3 sales.db
-- .mode csv
-- .import data/cleaned_sales_data.csv sales

-- ═══════════════════════════════════════════════════════════════════════════
-- Q1: Best-selling categories by revenue
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    Category,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    COUNT(DISTINCT "Order ID") AS Order_Count,
    ROUND(AVG("Profit Margin (%)"), 2) AS Avg_Margin_Pct,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM sales), 1) AS Revenue_Share_Pct
FROM sales
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- Q1b: Top 10 products (sub-categories) by revenue
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    "Sub-Category",
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    ROUND(AVG("Unit Price"), 2) AS Avg_Unit_Price
FROM sales
GROUP BY "Sub-Category"
ORDER BY Total_Revenue DESC
LIMIT 10;

-- ═══════════════════════════════════════════════════════════════════════════
-- Q2: Monthly revenue (averaged across years)
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    Month,
    "Month Name",
    ROUND(SUM(Revenue) / COUNT(DISTINCT Year), 2) AS Avg_Monthly_Revenue,
    ROUND(SUM(Profit) / COUNT(DISTINCT Year), 2) AS Avg_Monthly_Profit
FROM sales
GROUP BY Month, "Month Name"
ORDER BY Month;

-- ═══════════════════════════════════════════════════════════════════════════
-- Q3: Regional performance
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT "Order ID") AS Order_Count,
    ROUND(AVG(Revenue), 2) AS Avg_Order_Value,
    ROUND(AVG("Profit Margin (%)"), 2) AS Avg_Margin_Pct,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM sales), 1) AS Revenue_Share_Pct
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- Q4: Average Order Value (AOV)
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    ROUND(AVG(Order_Revenue), 2) AS Avg_Order_Value,
    ROUND(AVG(Items), 1) AS Avg_Items_Per_Order
FROM (
    SELECT
        "Order ID",
        SUM(Revenue) AS Order_Revenue,
        SUM(Quantity) AS Items
    FROM sales
    GROUP BY "Order ID"
);

-- AOV by Segment
SELECT
    Segment,
    ROUND(AVG(Order_Revenue), 2) AS AOV
FROM (
    SELECT
        "Order ID",
        Segment,
        SUM(Revenue) AS Order_Revenue
    FROM sales
    GROUP BY "Order ID", Segment
)
GROUP BY Segment
ORDER BY AOV DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- Q5: Discount impact on profit
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    "Discount Band",
    COUNT(*) AS Row_Count,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(AVG("Profit Margin (%)"), 2) AS Avg_Margin_Pct,
    ROUND(SUM(Profit) / SUM(Revenue), 4) AS Profit_Per_Revenue_Dollar
FROM sales
GROUP BY "Discount Band"
ORDER BY
    CASE "Discount Band"
        WHEN 'No Discount' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        WHEN '21-30%' THEN 4
        WHEN '31%+' THEN 5
    END;

-- ═══════════════════════════════════════════════════════════════════════════
-- BONUS: Year-over-Year growth
-- ═══════════════════════════════════════════════════════════════════════════
SELECT
    Year,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(
        (SUM(Revenue) - LAG(SUM(Revenue)) OVER (ORDER BY Year))
        / LAG(SUM(Revenue)) OVER (ORDER BY Year) * 100, 1
    ) AS Revenue_Growth_Pct
FROM sales
GROUP BY Year
ORDER BY Year;

