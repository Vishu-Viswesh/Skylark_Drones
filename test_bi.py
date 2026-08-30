from data_processor import load_deals, load_work_orders

from bi_tools import (
    calculate_pipeline,
    calculate_weighted_pipeline,
    calculate_win_rate,
    probability_quality,
    revenue_by_sector,
    billing_summary,
    execution_status_summary,
    work_orders_by_sector,
    data_quality_report
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("Loading data...")

deals = load_deals()
work_orders = load_work_orders()


# ---------------------------------------------------------
# DATA SUMMARY
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DATA SUMMARY")
print("=" * 60)

print(f"Deals: {len(deals)}")
print(f"Work Orders: {len(work_orders)}")


# ---------------------------------------------------------
# DEAL KPIs
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DEAL KPIs")
print("=" * 60)

pipeline = calculate_pipeline(deals)

weighted_pipeline = calculate_weighted_pipeline(
    deals
)

win_rate = calculate_win_rate(
    deals
)

print(
    f"Pipeline: ₹{pipeline:,.2f}"
)

print(
    f"Weighted Pipeline: ₹{weighted_pipeline:,.2f}"
)

print(
    f"Win Rate: {win_rate:.2%}"
)


# ---------------------------------------------------------
# CLOSURE PROBABILITY QUALITY
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("CLOSURE PROBABILITY QUALITY")
print("=" * 60)

probability = probability_quality(deals)

print(
    f'Total Deals: {probability["total_deals"]}'
)

print(
    f'Deals with valid probability: '
    f'{probability["valid_probability"]}'
)

print(
    f'Deals with missing/invalid probability: '
    f'{probability["missing_probability"]}'
)


# ---------------------------------------------------------
# REVENUE BY SECTOR
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("REVENUE BY SECTOR")
print("=" * 60)

sector_revenue = revenue_by_sector(deals)

if sector_revenue.empty:

    print("No sector revenue data available.")

else:

    print(
        sector_revenue.to_string(index=False)
    )


# ---------------------------------------------------------
# WORK ORDER BILLING
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("WORK ORDER BILLING")
print("=" * 60)

billing = billing_summary(
    work_orders
)

if billing:

    for key, value in billing.items():

        print(
            f"{key.title()}: ₹{value:,.2f}"
        )

else:

    print("No billing data available.")


# ---------------------------------------------------------
# EXECUTION STATUS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("EXECUTION STATUS")
print("=" * 60)

execution = execution_status_summary(
    work_orders
)

if execution.empty:

    print("No execution status data available.")

else:

    print(
        execution.to_string()
    )


# ---------------------------------------------------------
# WORK ORDERS BY SECTOR
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("WORK ORDERS BY SECTOR")
print("=" * 60)

sector_work_orders = work_orders_by_sector(
    work_orders
)

if sector_work_orders.empty:

    print("No work order sector data available.")

else:

    print(
        sector_work_orders.to_string()
    )


# ---------------------------------------------------------
# DATA QUALITY
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY")
print("=" * 60)

issues = data_quality_report(
    deals,
    work_orders
)

if issues:

    for issue in issues:

        print(f"WARNING: {issue}")

else:

    print("No data quality issues detected.")


# ---------------------------------------------------------
# FINISHED
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("BI ANALYSIS COMPLETE")
print("=" * 60)