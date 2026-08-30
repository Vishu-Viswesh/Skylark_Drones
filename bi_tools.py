import pandas as pd


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def to_number(series):
    """
    Convert a pandas Series to numeric values.
    Invalid or missing values become 0.
    """
    return pd.to_numeric(series, errors="coerce").fillna(0)


def find_column(df, possible_names):
    """
    Find a column using a list of possible names.
    """

    for name in possible_names:

        if name in df.columns:
            return name

    return None


# ---------------------------------------------------------
# DEAL PIPELINE
# ---------------------------------------------------------

def calculate_pipeline(deals):

    value_col = find_column(
        deals,
        [
            "Masked Deal value",
            "Deal Value",
            "Masked Deal Value"
        ]
    )

    if value_col is None:
        return 0

    return to_number(deals[value_col]).sum()


# ---------------------------------------------------------
# WEIGHTED PIPELINE
# ---------------------------------------------------------
def calculate_weighted_pipeline(deals):

    value_col = find_column(
        deals,
        [
            "Masked Deal value",
            "Deal Value",
            "Masked Deal Value"
        ]
    )

    probability_col = find_column(
        deals,
        [
            "Closure Probability",
            "Probability"
        ]
    )

    if value_col is None or probability_col is None:
        return 0

    values = to_number(
        deals[value_col]
    )

    probabilities = (
        deals[probability_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    probability_map = {
        "high": 0.80,
        "medium": 0.50,
        "low": 0.20
    }

    probability_values = probabilities.map(
        probability_map
    )

    valid = probability_values.notna()

    weighted_value = (
        values[valid] *
        probability_values[valid]
    ).sum()

    return weighted_value

def probability_quality(deals):

    probability_col = find_column(
        deals,
        [
            "Closure Probability",
            "Probability"
        ]
    )

    if probability_col is None:
        return {
            "total_deals": len(deals),
            "valid_probability": 0,
            "missing_probability": len(deals)
        }

    probabilities = (
        deals[probability_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    valid_values = {
        "high",
        "medium",
        "low"
    }

    valid = probabilities.isin(valid_values)

    return {
        "total_deals": len(deals),
        "valid_probability": int(valid.sum()),
        "missing_probability": int((~valid).sum())
    }

# ---------------------------------------------------------
# OPEN DEALS
# ---------------------------------------------------------

def get_open_deals(deals):

    status_col = find_column(
        deals,
        [
            "Deal Status",
            "Status"
        ]
    )

    if status_col is None:
        return deals.copy()

    return deals[
        deals[status_col]
        .astype(str)
        .str.lower()
        .eq("open")
    ].copy()


# ---------------------------------------------------------
# WIN RATE
# ---------------------------------------------------------

def calculate_win_rate(deals):

    status_col = find_column(
        deals,
        [
            "Deal Status",
            "Status"
        ]
    )

    if status_col is None:
        return 0

    status = (
        deals[status_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    won = (status == "won").sum()
    dead = (status == "dead").sum()

    closed_deals = won + dead

    if closed_deals == 0:
        return 0

    return won / closed_deals


# ---------------------------------------------------------
# REVENUE BY SECTOR
# ---------------------------------------------------------

def revenue_by_sector(deals):

    value_col = find_column(
        deals,
        [
            "Masked Deal value",
            "Deal Value",
            "Masked Deal Value"
        ]
    )

    sector_col = find_column(
        deals,
        [
            "Sector/service",
            "Sector",
            "Sector / service"
        ]
    )

    if value_col is None or sector_col is None:
        return pd.DataFrame()

    temp = deals.copy()

    temp["_value"] = to_number(
        temp[value_col]
    )

    result = (
        temp.groupby(sector_col)["_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    result.columns = [
        "Sector",
        "Deal Value"
    ]

    return result


# ---------------------------------------------------------
# WORK ORDER BILLING
# ---------------------------------------------------------

def billing_summary(work_orders):

    billed_col = find_column(
        work_orders,
        [
            "Billed Value in Rupees (Excl of GST.) (Masked)",
            "Billed Value in Rupees (Excl of GST.)",
            "Billed Value"
        ]
    )

    collected_col = find_column(
        work_orders,
        [
            "Collected Amount in Rupees (Incl of GST.) (Masked)",
            "Collected Amount",
            "Collected Amount in Rupees"
        ]
    )

    receivable_col = find_column(
        work_orders,
        [
            "Amount Receivable (Masked)",
            "Amount Receivable"
        ]
    )

    result = {}

    if billed_col:
        result["billed"] = to_number(
            work_orders[billed_col]
        ).sum()

    if collected_col:
        result["collected"] = to_number(
            work_orders[collected_col]
        ).sum()

    if receivable_col:
        result["receivable"] = to_number(
            work_orders[receivable_col]
        ).sum()

    return result


# ---------------------------------------------------------
# EXECUTION STATUS
# ---------------------------------------------------------

def execution_status_summary(work_orders):

    status_col = find_column(
        work_orders,
        [
            "Execution Status",
            "WO Status"
        ]
    )

    if status_col is None:
        return pd.Series(dtype=int)

    return (
        work_orders[status_col]
        .astype(str)
        .value_counts()
    )


# ---------------------------------------------------------
# SECTOR BREAKDOWN
# ---------------------------------------------------------

def work_orders_by_sector(work_orders):

    sector_col = find_column(
        work_orders,
        [
            "Sector"
        ]
    )

    if sector_col is None:
        return pd.Series(dtype=int)

    return (
        work_orders[sector_col]
        .astype(str)
        .value_counts()
    )


# ---------------------------------------------------------
# DATA QUALITY
# ---------------------------------------------------------

def data_quality_report(deals, work_orders):

    issues = []

    # Expected record counts from the provided datasets.
    if len(deals) != 346:
        issues.append(
            f"Deals contains {len(deals)} rows; expected 346."
        )

    if len(work_orders) != 177:
        issues.append(
            f"Work Orders contains {len(work_orders)} rows; "
            f"expected 177."
        )

    # Missing deal status
    if "Deal Status" in deals.columns:

        missing_status = deals["Deal Status"].isna().sum()

        if missing_status > 0:
            issues.append(
                f"{missing_status} Deals have missing Deal Status."
            )

    # Missing work order execution status
    if "Execution Status" in work_orders.columns:

        missing_execution = (
            work_orders["Execution Status"]
            .isna()
            .sum()
        )

        if missing_execution > 0:
            issues.append(
                f"{missing_execution} Work Orders have "
                f"missing Execution Status."
            )
    if "Closure Probability" in deals.columns:

        probabilities = (
            deals["Closure Probability"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        valid_values = {
            "high",
            "medium",
            "low"
        }

        invalid_count = (
            ~probabilities.isin(valid_values)
        ).sum()

        if invalid_count > 0:
            issues.append(
                f"{invalid_count} Deals have "
                f"missing or invalid Closure Probability."
            )

    return issues