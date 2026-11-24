import os
import pandas as pd
import numpy as np

# Setup directories
os.makedirs("data", exist_ok=True)

def generate_raw_data(filepath="data/ecommerce_sales_raw.csv"):
    """Generates a realistic messy retail dataset for demonstration."""
    np.random.seed(42)
    n_rows = 1000

    customer_ids = [f"CUST_{i:04d}" for i in np.random.randint(1, 350, size=n_rows)]
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", periods=n_rows).strftime("%Y-%m-%d").tolist()
    categories = np.random.choice(["Electronics", "electronics ", "Clothing", "Home & Kitchen", "Beauty", "BEAUTY"], size=n_rows)
    regions = np.random.choice(["North", "South", "East", "West", "north", None], p=[0.24, 0.24, 0.24, 0.23, 0.03, 0.02], size=n_rows)
    ages = np.random.randint(18, 70, size=n_rows).astype(float)
    quantities = np.random.randint(1, 6, size=n_rows)
    unit_prices = np.round(np.random.uniform(15.0, 450.0, size=n_rows), 2)

    df = pd.DataFrame({
        "Order_ID": [f"ORD_{10000+i}" for i in range(n_rows)],
        "Customer_ID": customer_ids,
        "Order_Date": dates,
        "Customer_Age": ages,
        "Region": regions,
        "Product_Category": categories,
        "Quantity": quantities,
        "Unit_Price": [f"${p}" if i % 10 == 0 else str(p) for i, p in enumerate(unit_prices)]
    })

    # Inject missing values & outliers
    df.loc[np.random.choice(df.index, 45, replace=False), "Customer_Age"] = np.nan
    df.loc[np.random.choice(df.index, 20, replace=False), "Unit_Price"] = np.nan
    df.loc[5, "Unit_Price"] = "4999.99"  # Extreme price outlier
    df.loc[12, "Quantity"] = 50          # Extreme quantity outlier

    # Inject 20 exact duplicate rows
    duplicates = df.sample(20, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    df.to_csv(filepath, index=False)
    print(f"[INFO] Generated raw dataset at {filepath} with shape {df.shape}")

def run_task1():
    raw_path = "data/ecommerce_sales_raw.csv"
    clean_path = "data/ecommerce_sales_cleaned.csv"
    if not os.path.exists(raw_path):
        generate_raw_data(raw_path)

    # 1. Import and inspect structure
    df = pd.read_csv(raw_path)
    print("\n--- INITIAL DATA INSPECTION ---")
    print(df.info())
    print("\nMissing Values per Column:\n", df.isnull().sum())
    print(f"\nDuplicate Records Found: {df.duplicated().sum()}")

    # 2. Remove duplicates
    df = df.drop_duplicates().copy()

    # 3. Clean inconsistent string entries
    df["Product_Category"] = df["Product_Category"].str.strip().str.title()
    df["Region"] = df["Region"].fillna("Unknown").str.strip().str.title()

    # 4. Correct data types
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Unit_Price"] = df["Unit_Price"].astype(str).str.replace("$", "", regex=False)
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")

    # 5. Handle null values (Median imputation for skewed numerical data)
    df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median()).astype(int)
    df["Unit_Price"] = df["Unit_Price"].fillna(df["Unit_Price"].median())

    # 6. Feature engineering for downstream tasks
    df["Total_Sales"] = np.round(df["Quantity"] * df["Unit_Price"], 2)
    df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

    # Bonus: Save cleaned dataset
    df.to_csv(clean_path, index=False)
    print("\n--- CLEANED DATA SUMMARY ---")
    print(df.info())
    print(f"\n[SUCCESS] Cleaned dataset saved to {clean_path} with shape {df.shape}")

if __name__ == "__main__":
    run_task1()
