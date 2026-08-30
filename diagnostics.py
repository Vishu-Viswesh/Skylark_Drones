from data_processor import load_deals, load_work_orders


deals = load_deals()
work_orders = load_work_orders()


print("\n" + "=" * 60)
print("DEAL STATUS VALUES")
print("=" * 60)

print(
    deals["Deal Status"]
    .value_counts(dropna=False)
)


print("\n" + "=" * 60)
print("CLOSURE PROBABILITY VALUES")
print("=" * 60)

print(
    deals["Closure Probability"]
    .value_counts(dropna=False)
)


print("\n" + "=" * 60)
print("WORK ORDER ROW COUNT")
print("=" * 60)

print("Rows:", len(work_orders))


print("\n" + "=" * 60)
print("WORK ORDER ITEM IDS")
print("=" * 60)

print("Unique IDs:", work_orders["Item ID"].nunique())

duplicates = work_orders[
    work_orders["Item ID"].duplicated(keep=False)
]

print("\nDuplicate IDs:")

if duplicates.empty:
    print("None")

else:
    print(
        duplicates[
            ["Item ID", "Name"]
        ].to_string(index=False)
    )