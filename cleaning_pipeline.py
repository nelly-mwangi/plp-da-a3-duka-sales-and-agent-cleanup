
import pandas as pd


def clean_agent_data(txns, agents):
    """
    Clean mobile money agent transactions and merge them
    with the agent register.

    Parameters
    ----------
    txns : pandas.DataFrame
        Raw mobile money transaction data.
    agents : pandas.DataFrame
        Agent registration data.

    Returns
    -------
    clean_df : pandas.DataFrame
        Cleaned transactions with agent county information.
    log : list
        Summary of cleaning actions performed.
    """

    # Work on copies so the original data is not changed.
    df = txns.copy()
    agent_df = agents.copy()

    log = []
    original_rows = len(df)

    log.append(f"Original transaction rows: {original_rows}")

    # --------------------------------------------------
    # 1. Remove duplicate transactions
    # --------------------------------------------------

    duplicate_count = df.duplicated(
        subset="txn_id",
        keep="first"
    ).sum()

    df = df.drop_duplicates(
        subset="txn_id",
        keep="first"
    ).copy()

    log.append(f"Duplicate transactions removed: {duplicate_count}")

    # --------------------------------------------------
    # 2. Standardise transaction types
    # --------------------------------------------------

    df["txn_type"] = (
        df["txn_type"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({
            "deposit": "Deposit",
            "withdrawal": "Withdrawal"
        })
    )

    invalid_types = df["txn_type"].isna().sum()

    if invalid_types > 0:
        raise ValueError(
            f"Found {invalid_types} unrecognised transaction types."
        )

    log.append("Transaction types standardised to Deposit and Withdrawal.")

    # --------------------------------------------------
    # 3. Convert transaction amounts to numeric values
    # --------------------------------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["amount_imputed"] = df["amount"].isna()

    missing_amounts = df["amount_imputed"].sum()

    if df["amount"].notna().sum() == 0:
        raise ValueError("No valid transaction amounts are available.")

    median_amount = df["amount"].median()

    df["amount"] = df["amount"].fillna(median_amount)

    log.append(
        f"Missing or invalid amounts imputed using median "
        f"({missing_amounts} rows)."
    )

    # --------------------------------------------------
    # 4. Detect outliers using the IQR method
    # --------------------------------------------------

    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    df["is_outlier"] = (
        (df["amount"] < lower_limit) |
        (df["amount"] > upper_limit)
    )

    outlier_count = df["is_outlier"].sum()

    log.append(
        f"Potential amount outliers flagged: {outlier_count}. "
        "Outliers were retained for review."
    )

    # --------------------------------------------------
    # 5. Standardise and validate transaction dates
    # --------------------------------------------------

    date_text = (
        df["txn_date"]
        .astype("string")
        .str.strip()
        .str.replace("/", "-", regex=False)
    )

    df["txn_date"] = pd.to_datetime(
        date_text,
        format="%Y-%m-%d",
        errors="coerce"
    )

    invalid_dates = df["txn_date"].isna().sum()

    if invalid_dates > 0:
        raise ValueError(
            f"Found {invalid_dates} invalid transaction dates."
        )

    log.append("Transaction dates standardised to YYYY-MM-DD.")

    # --------------------------------------------------
    # 6. Merge transactions with the agent register
    # --------------------------------------------------

    agent_df = agent_df[["agent_id", "county"]].drop_duplicates(
        subset="agent_id"
    )

    before_merge_rows = len(df)

    df = df.merge(
        agent_df,
        on="agent_id",
        how="left",
        validate="many_to_one",
        indicator=True
    )

    unknown_agents = (df["_merge"] == "left_only").sum()

    df["county"] = df["county"].fillna("Unknown")

    df = df.drop(columns=["_merge"])

    if len(df) != before_merge_rows:
        raise ValueError("The merge unexpectedly changed the transaction row count.")

    log.append(
        f"Transactions with unknown agent IDs: {unknown_agents}."
    )

    log.append(
        f"Final cleaned transaction rows: {len(df)}"
    )

    return df, log
