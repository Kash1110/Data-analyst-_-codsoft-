# Task 1: Data Cleaning & Preprocessing

A Python data engineering and preprocessing repository demonstrating end-to-end dataset inspection, anomaly resolution, type casting, and feature preparation using Pandas.

## Repository Structure
```text
task1-data-cleaning-preprocessing/
├── data/
│   ├── ecommerce_sales_raw.csv       # Raw input dataset with missing values, duplicates, and formatting issues
│   └── ecommerce_sales_cleaned.csv   # Cleaned and preprocessed output dataset (Bonus)
├── src/
│   └── task1_data_cleaning.py        # Complete data cleaning pipeline
├── .gitignore
├── requirements.txt
└── README.md
```

## Key Operations Performed
1. **Structural Inspection:** Audited schema, data types, null counts, and duplicate rows.
2. **Deduplication:** Identified and removed 20 exact duplicate transaction records.
3. **String Standardization:** Stripped whitespace and normalized casing across `Product_Category` and `Region`.
4. **Type Casting:** Converted `Order_Date` to `datetime64` and stripped currency symbols (`$`) from `Unit_Price` to cast as `float64`.
5. **Missing Value Imputation:** Applied median imputation for `Customer_Age` and `Unit_Price` to preserve distribution integrity against outliers.
6. **Export:** Saved the analysis-ready table to `data/ecommerce_sales_cleaned.csv`.

## Quickstart
```bash
pip install -r requirements.txt
python src/task1_data_cleaning.py
```
