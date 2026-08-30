from monday_client import monday_query


query = """
query {
    boards(limit: 100) {
        id
        name
        state
    }
}
"""


try:
    data = monday_query(query)

    print("\nYour monday.com boards:\n")

    for board in data["boards"]:
        print(
            f'ID: {board["id"]} | '
            f'Name: {board["name"]} | '
            f'State: {board["state"]}'
        )

except Exception as e:
    print("Error:")
    print(e)