# Project Overview

This repository contains two data analysis engagements completed using Python, Pandas, NumPy and Microsoft Excel.

## Engagement 1: Duka Sales Analysis

The objective was to explore retail sales data, analyse branch and product performance, and identify business trends.

### Duka Executive Summary

- **Total sales revenue:** KES 71,792,500
- **Total orders:** 1,000
- **Highest-performing branch:** Nairobi
- **Nairobi revenue:** KES 26,106,100 (36.4%)
- **Top product by revenue:** Laptops (KES 41,535,000)
- **Highest monthly revenue:** April (KES 13,518,300)
- **Premium Online Coast Capital:** 83 orders worth KES 10,218,000

The analysis was conducted using Python and Excel, including pivot tables and sales summaries.

**Notebook:** `duka_sales_exploration.ipynb`

## Engagement 2: Mobile Money Agent Network

The objective was to clean, validate and analyse mobile money transactions using an agent register.

### Data Cleaning Summary

| Metric | Before cleaning | After cleaning |
|---|---:|---:|
| Transaction records | 612 | 600 |
| Duplicate transaction IDs | 12 | 0 |
| Missing or invalid transaction amounts (15 blank + 7 text N/A) | 22 | 0 |
| Imputed amounts | 0 | 20 |
| Flagged outliers (IQR, incl. five KES 250,000 values) | 0 | 40 |
| Unknown agent transactions | 7 | 7 |

The cleaning process included:

- Removing duplicate transaction IDs.
- Imputing the 20 missing or invalid amounts with the median of observed amounts and flagging them in `amount_imputed`.
- Standardising transaction types and dates.
- Flagging outliers with the IQR method on observed amounts (before imputation). The five KES 250,000 transactions are about 46% of total value, so they are retained, flagged and recommended for verification at source.
- Merging transactions with the agent register.
- Assigning unknown agents to the `Unknown` county.

The cleaned dataset was used for county-level and weekly transaction analysis.

**Notebook:** `agent_cleanup.ipynb`

**Repository contents:** `generate_data.py` (both generators), `cleaning_pipeline.py` (`clean_agent_data(txns, agents)` returning `(clean_df, log)`), the two notebooks, `excel/duka_branch_summary.xlsx` (SUMIFS, XLOOKUP and PivotTable), and `outputs/` (`premium_online_coast_capital.csv`, `agent_transactions_clean.csv`). The raw CSVs are not committed; regenerate them with `python generate_data.py`.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/nelly-mwangi/plp-da-a3-duka-sales-and-agent-cleanup.git
cd plp-da-a3-duka-sales-and-agent-cleanup
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Regenerate the datasets

```bash
python generate_data.py
```

### 4. Run the notebooks

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open and run the notebooks in order:

1. `duka_sales_exploration.ipynb`
2. `agent_cleanup.ipynb`

Run each notebook from beginning to end to reproduce the analysis and outputs.

## Conclusion

These engagements provided practical experience in data cleaning, data validation, exploratory data analysis, Excel reporting and visualisation. The projects demonstrate how data can be transformed into useful insights to support business decision-making.
