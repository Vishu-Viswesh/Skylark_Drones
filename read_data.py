from monday_client import get_board_items


DEALS_BOARD_ID = "5030964426"
WORK_ORDERS_BOARD_ID = "5030964496"


def test_board(board_id, board_name):

    print("\n" + "=" * 60)
    print(board_name)
    print("=" * 60)

    items = get_board_items(board_id)

    print("Total items:", len(items))

    print("\nFirst 3 items:\n")

    for item in items[:3]:

        print("Item ID:", item["id"])
        print("Item Name:", item["name"])

        for column in item["column_values"]:

            print(
                f'  {column["id"]}: {column["text"]}'
            )

        print("-" * 50)


test_board(
    DEALS_BOARD_ID,
    "DEALS"
)

test_board(
    WORK_ORDERS_BOARD_ID,
    "WORK ORDERS"
)