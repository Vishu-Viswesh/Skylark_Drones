import os
import requests
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"
MONDAY_API_TOKEN = os.getenv("MONDAY_API_TOKEN")

def monday_query(query, variables=None):

    if not MONDAY_API_TOKEN:
        raise Exception("MONDAY_API_TOKEN is missing from .env")

    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json",
        "API-Version": "2026-07"
    }

    response = requests.post(
        MONDAY_API_URL,
        headers=headers,
        json={
            "query": query,
            "variables": variables or {}
        },
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        raise Exception(result["errors"])

    return result["data"]


def get_boards():

    query = """
    query {
        boards(limit: 100) {
            id
            name
            state
        }
    }
    """

    return monday_query(query)["boards"]


def get_board_columns(board_id):

    query = """
    query ($board_id: [ID!]) {
        boards(ids: $board_id) {
            id
            name
            columns {
                id
                title
                type
            }
        }
    }
    """

    data = monday_query(
        query,
        {"board_id": [str(board_id)]}
    )

    return data["boards"][0]


def get_board_items(board_id):

    first_query = """
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
        first_query,
        {"board_id": [str(board_id)]}
    )

    page = data["boards"][0]["items_page"]

    all_items = page["items"]
    cursor = page["cursor"]

    next_query = """
    query ($cursor: String!, $limit: Int!) {
        next_items_page(
            cursor: $cursor,
            limit: $limit
        ) {
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
    """

    while cursor:

        data = monday_query(
            next_query,
            {
                "cursor": cursor,
                "limit": 500
            }
        )

        page = data["next_items_page"]

        all_items.extend(page["items"])

        cursor = page["cursor"]

    return all_items