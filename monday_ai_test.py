from openai import OpenAI

from monday_client import MONDAY_API_TOKEN


if not MONDAY_API_TOKEN:
    raise RuntimeError(
        "MONDAY_API_TOKEN is missing from .env"
    )


client = OpenAI(
    api_key=MONDAY_API_TOKEN,
    base_url="https://api.monday.com/platform-ai-gateway/openai/v1"
)


response = client.chat.completions.create(
    model="monday-fast",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: monday ai works"
        }
    ]
)


print(response.choices[0].message.content)