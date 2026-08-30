import json
from openai import OpenAI

from monday_client import MONDAY_API_TOKEN

from data_processor import (
    load_deals,
    load_work_orders
)

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


# ============================================================
# MONDAY AI CLIENT
# ============================================================

if not MONDAY_API_TOKEN:
    raise RuntimeError(
        "MONDAY_API_TOKEN is missing from .env"
    )


client = OpenAI(
    api_key=MONDAY_API_TOKEN,
    base_url="https://api.monday.com/platform-ai-gateway/openai/v1"
)


MODEL = "monday-fast"


# ============================================================
# DATA LOADING
# ============================================================

def load_live_data():

    deals = load_deals()
    work_orders = load_work_orders()

    return deals, work_orders


# ============================================================
# BI TOOL FUNCTIONS
# ============================================================

def get_pipeline():

    deals, _ = load_live_data()

    pipeline = calculate_pipeline(deals)

    return {
        "total_deals": len(deals),
        "pipeline": pipeline
    }


def get_weighted_pipeline():

    deals, _ = load_live_data()

    weighted = calculate_weighted_pipeline(deals)

    probability = probability_quality(deals)

    return {
        "total_deals": len(deals),
        "weighted_pipeline": weighted,
        "valid_probability": probability["valid_probability"],
        "missing_probability": probability["missing_probability"],
        "probability_assumptions": {
            "High": "80%",
            "Medium": "50%",
            "Low": "20%"
        }
    }


def get_win_rate():

    deals, _ = load_live_data()

    win_rate = calculate_win_rate(deals)

    status_counts = (
        deals["Deal Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .value_counts()
        .to_dict()
    )

    # calculate_win_rate returns a decimal.
    # Example: 0.5651 -> 56.51%
    win_rate_percent = win_rate * 100

    return {
        "win_rate_percent": win_rate_percent,
        "deal_status_counts": status_counts,
        "formula": "Won / (Won + Dead)"
    }


def get_revenue_by_sector():

    deals, _ = load_live_data()

    result = revenue_by_sector(deals)

    return result.to_dict(
        orient="records"
    )


def get_billing():

    _, work_orders = load_live_data()

    return billing_summary(work_orders)


def get_execution_status():

    _, work_orders = load_live_data()

    result = execution_status_summary(
        work_orders
    )

    return result.to_dict()


def get_work_orders_sector():

    _, work_orders = load_live_data()

    result = work_orders_by_sector(
        work_orders
    )

    return result.to_dict()


def get_data_quality():

    deals, work_orders = load_live_data()

    issues = data_quality_report(
        deals,
        work_orders
    )

    return {
        "deal_count": len(deals),
        "work_order_count": len(work_orders),
        "issues": issues
    }


def get_business_overview():

    deals, work_orders = load_live_data()

    pipeline = calculate_pipeline(deals)

    weighted_pipeline = calculate_weighted_pipeline(
        deals
    )

    win_rate = calculate_win_rate(
        deals
    )

    billing = billing_summary(
        work_orders
    )

    execution = execution_status_summary(
        work_orders
    )

    probability = probability_quality(
        deals
    )

    return {
        "deals": len(deals),
        "work_orders": len(work_orders),
        "pipeline": pipeline,
        "weighted_pipeline": weighted_pipeline,

        # Convert decimal to percentage
        "win_rate_percent": win_rate * 100,

        "probability_quality": probability,

        "billing": billing,

        "execution_status": execution.to_dict()
    }


# ============================================================
# TOOL DEFINITIONS
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_pipeline",
            "description": (
                "Get the total sales pipeline from "
                "the live Deals board."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_weighted_pipeline",
            "description": (
                "Get the probability-weighted sales "
                "pipeline from the live Deals board. "
                "Also returns valid and missing probability "
                "counts."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_win_rate",
            "description": (
                "Calculate the sales win rate using "
                "Won and Dead deals. The returned "
                "win_rate_percent is already expressed "
                "as a percentage, for example 56.5."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_revenue_by_sector",
            "description": (
                "Get total deal value grouped by "
                "sector/service."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_billing",
            "description": (
                "Get billed, collected and receivable "
                "amounts from Work Orders."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_execution_status",
            "description": (
                "Get Work Order counts grouped by "
                "execution status."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_work_orders_sector",
            "description": (
                "Get Work Order counts grouped by "
                "sector."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_data_quality",
            "description": (
                "Check Deals and Work Orders for "
                "known data quality issues."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_business_overview",
            "description": (
                "Get a high-level business overview "
                "covering sales pipeline, weighted "
                "pipeline, win rate, billing, "
                "execution and data quality."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    }
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name):

    if tool_name == "get_pipeline":
        return get_pipeline()

    elif tool_name == "get_weighted_pipeline":
        return get_weighted_pipeline()

    elif tool_name == "get_win_rate":
        return get_win_rate()

    elif tool_name == "get_revenue_by_sector":
        return get_revenue_by_sector()

    elif tool_name == "get_billing":
        return get_billing()

    elif tool_name == "get_execution_status":
        return get_execution_status()

    elif tool_name == "get_work_orders_sector":
        return get_work_orders_sector()

    elif tool_name == "get_data_quality":
        return get_data_quality()

    elif tool_name == "get_business_overview":
        return get_business_overview()

    else:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are the Skylark Drones Business Intelligence Agent.

You answer business questions using LIVE data retrieved
from monday.com.

There are two main boards:

1. Deal funnel Data

Contains:
- sales opportunities
- deal status
- deal value
- closure probability
- deal stage
- sector

2. Work_Order_Tracker Data

Contains:
- project execution
- billing
- collections
- receivables
- execution status
- sector


IMPORTANT RULES:

1. NEVER invent numerical business information.

2. For numerical questions, use the appropriate BI tool.

3. Do not calculate financial values from your own memory.

4. If a question requires information from both boards,
   use the relevant tools from both boards.

5. Clearly distinguish between:

   - Total pipeline
   - Weighted pipeline
   - Billed amount
   - Collected amount
   - Receivable amount

6. Weighted pipeline uses:

   High = 80%
   Medium = 50%
   Low = 20%

7. Missing closure probability does NOT mean zero probability.

   It means the deal does not have enough information
   for reliable probability weighting.

8. Win rate is:

   Won / (Won + Dead)

   The get_win_rate tool returns the result already
   converted to percentage.

   Example:

   0.565 -> 56.5%

9. Current data quality issues should be retrieved
   using get_data_quality rather than assumed.

10. When discussing weighted pipeline, always mention
    the number of deals with valid/missing probability
    when that information is available.

11. When answering questions about sectors, use the
    get_revenue_by_sector tool.

12. When answering questions about Work Order execution,
    use get_execution_status.

13. When answering questions about billing or collections,
    use get_billing.

14. When answering broad business questions, use
    get_business_overview.

15. If the question is ambiguous and different
    interpretations could produce different business
    answers, ask for clarification.

16. Do not modify monday.com data.

    This agent is READ-ONLY.

17. Use Indian Rupee notation when discussing financial
    values.

18. Keep answers concise and suitable for a
    founder/executive.

19. For numerical answers, provide:

    - Direct answer
    - Relevant numbers
    - Percentage where useful
    - Short business interpretation
    - Important data-quality caveat

20. Do not claim that missing data is zero.

21. Do not describe the weighted pipeline as a reliable
    forecast when most deals have missing probability.

22. Avoid unnecessary technical explanations.
    Focus on business meaning.

23. When reporting win rate, always use a percentage sign.

    Correct:
    "Win rate is 56.51%."

    Incorrect:
    "Win rate is 0.5651%."

24. When reporting work completion, distinguish between:

    Completed
    Ongoing
    Executed until current month
    Not Started
    Paused/Stuck
    Partial Completed
    Details pending from Client
    Undefined

25. If data quality affects the reliability of an answer,
    explicitly mention it.
"""


# ============================================================
# ASK AGENT
# ============================================================

def ask_agent(question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    try:

        while True:

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            message = response.choices[0].message

            # ------------------------------------------------
            # No tool required
            # ------------------------------------------------

            if not message.tool_calls:

                return message.content

            # ------------------------------------------------
            # Add assistant's tool request
            # ------------------------------------------------

            messages.append(message)

            # ------------------------------------------------
            # Execute every requested tool
            # ------------------------------------------------

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                try:

                    result = execute_tool(
                        tool_name
                    )

                    tool_output = json.dumps(
                        result,
                        default=str
                    )

                except Exception as error:

                    tool_output = json.dumps(
                        {
                            "error": str(error)
                        }
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output
                    }
                )

    except Exception as error:

        return (
            "I couldn't complete the analysis because "
            "the AI or monday.com service returned an "
            "error.\n\n"
            f"Error: {error}"
        )


# ============================================================
# COMMAND LINE INTERFACE
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SKYLARK DRONES - CONVERSATIONAL BI AGENT")
    print("=" * 70)

    print()
    print("Connected to monday.com Models API")
    print("Model:", MODEL)
    print()
    print("Ask a business question.")
    print("Type 'exit' to stop.")
    print()

    while True:

        question = input("You: ").strip()

        if question.lower() in [
            "exit",
            "quit"
        ]:

            print()
            print("Agent stopped.")
            break

        if not question:
            continue

        print()
        print("Agent:")

        answer = ask_agent(
            question
        )

        print(answer)
        print()
        print("-" * 70)