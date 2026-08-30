from data_processor import load_deals, load_work_orders


print("\nLoading Deals...")

deals = load_deals()

print("Deals rows:", len(deals))
print("Deals columns:")
print(deals.columns.tolist())

print("\nFirst 3 Deals:")
print(deals.head(3).to_string())


print("\n" + "=" * 70)


print("\nLoading Work Orders...")

work_orders = load_work_orders()

print("Work Orders rows:", len(work_orders))
print("Work Orders columns:")
print(work_orders.columns.tolist())

print("\nFirst 3 Work Orders:")
print(work_orders.head(3).to_string())