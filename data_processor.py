import pandas as pd

from monday_client import monday_query


def get_board_by_name(board_name):

    query = """
    query {
        boards(limit: 100) {
            id
            name
            state
            columns {
                id
                title
                type
            }
        }
    }
    """

    boards = monday_query(query)["boards"]

    for board in boards:
        if board["name"].strip().lower() == board_name.strip().lower():
            return board

    raise ValueError(f"Board not found: {board_name}")


def get_board_items(board_id):

    query = """
    query ($board_id: [ID!]) {
        boards(ids: $board_id) {
            items_page(limit: 500) {
                cursor
                items {
                    id
                    name
                    column_values {
                        id
                        text
                        value
                    }
                }
            }
        }
    }
    """

    data = monday_query(
        query,
        {"board_id": [str(board_id)]}
    )

    return data["boards"][0]["items_page"]["items"]


def board_to_dataframe(board_name):

    # Find board
    board = get_board_by_name(board_name)

    # Get column definitions
    columns = board["columns"]

    column_map = {
        column["id"]: column["title"]
        for column in columns
    }

    # Get items
    items = get_board_items(board["id"])

    rows = []

    for item in items:

        row = {
            "Item ID": item["id"],
            "Name": item["name"]
        }

        for column in item["column_values"]:

            column_name = column_map.get(
                column["id"],
                column["id"]
            )

            row[column_name] = column["text"]

        rows.append(row)

    return pd.DataFrame(rows)


def load_deals():

    return board_to_dataframe("Deal funnel Data")


def load_work_orders():

    return board_to_dataframe("Work_Order_Tracker Data")