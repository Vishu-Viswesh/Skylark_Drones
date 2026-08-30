import streamlit as st

from agent import ask_agent
from data_processor import load_deals, load_work_orders

from bi_tools import (
    calculate_pipeline,
    calculate_weighted_pipeline,
    calculate_win_rate,
    probability_quality,
    revenue_by_sector,
    billing_summary,
    execution_status_summary,
    data_quality_report,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Skylark Drones BI",
    page_icon="🚁",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(ttl=300)
def load_dashboard_data():

    deals = load_deals()
    work_orders = load_work_orders()

    pipeline = calculate_pipeline(deals)

    weighted_pipeline = calculate_weighted_pipeline(
        deals
    )

    win_rate = calculate_win_rate(
        deals
    )

    sector_data = revenue_by_sector(
        deals
    )

    execution_data = execution_status_summary(
        work_orders
    )

    billing = billing_summary(
        work_orders
    )

    probability_data = probability_quality(
        deals
    )

    quality_issues = data_quality_report(
        deals,
        work_orders
    )

    return (
        deals,
        work_orders,
        pipeline,
        weighted_pipeline,
        win_rate,
        sector_data,
        execution_data,
        billing,
        probability_data,
        quality_issues
    )


# =========================================================
# HEADER
# =========================================================

st.title("🚁 Skylark Drones")

st.caption(
    "Business Intelligence & Conversational Agent"
)

col_refresh, col_info = st.columns([1, 5])


with col_refresh:

    if st.button(
        "🔄 Refresh Data"
    ):

        st.cache_data.clear()
        st.rerun()


with col_info:

    st.caption(
        "Live business insights powered by monday.com data"
    )


# =========================================================
# GET DATA
# =========================================================

try:

    (
        deals,
        work_orders,
        pipeline,
        weighted_pipeline,
        win_rate,
        sector_data,
        execution_data,
        billing,
        probability_data,
        quality_issues
    ) = load_dashboard_data()


except Exception as e:

    st.error(
        f"Unable to load monday.com data: {e}"
    )

    st.stop()

# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Business Overview")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total Deals",
        f"{len(deals):,}"
    )

with c2:
    st.metric(
        "Work Orders",
        f"{len(work_orders):,}"
    )

with c3:
    st.metric(
        "Sales Pipeline",
        f"₹{pipeline / 1e7:,.2f} Cr"
    )

with c4:
    st.metric(
        "Weighted Pipeline",
        f"₹{weighted_pipeline / 1e7:,.2f} Cr"
    )

with c5:
    st.metric(
        "Win Rate",
        f"{win_rate:.2%}"
    )

# =========================================================
# OPERATIONAL EXECUTION
# =========================================================

completed = int(
    execution_data.get(
        "Completed",
        0
    )
)

ongoing = int(
    execution_data.get(
        "Ongoing",
        0
    )
)

total_work = len(
    work_orders
)


completion_rate = (
    completed / total_work * 100
    if total_work > 0
    else 0
)


st.subheader(
    "🏗️ Operational Execution"
)


w1, w2, w3 = st.columns(3)


with w1:

    st.metric(
        "Completed Work",
        f"{completed:,} / {total_work:,}"
    )


with w2:

    st.metric(
        "Completion Rate",
        f"{completion_rate:.1f}%"
    )


with w3:

    st.metric(
        "Ongoing",
        f"{ongoing:,}"
    )


st.progress(
    min(
        completion_rate / 100,
        1.0
    )
)


# =========================================================
# CHARTS
# =========================================================

left, right = st.columns(2)


# =========================================================
# DEAL VALUE BY SECTOR
# =========================================================

with left:

    st.subheader(
        "💰 Deal Value by Sector"
    )

    if not sector_data.empty:

        sector_chart = sector_data.copy()

        sector_chart = sector_chart.set_index(
            "Sector"
        )

        st.bar_chart(
            sector_chart["Deal Value"]
        )

    else:

        st.info(
            "No sector data available."
        )


# =========================================================
# WORK ORDER EXECUTION
# =========================================================

with right:

    st.subheader(
        "📋 Work Order Execution"
    )

    if len(execution_data) > 0:

        execution_chart = execution_data.copy()

        st.bar_chart(
            execution_chart
        )

    else:

        st.info(
            "No execution status data available."
        )


# =========================================================
# BILLING & COLLECTIONS
# =========================================================

st.subheader("💵 Billing & Collections")

b1, b2, b3 = st.columns(3)

billed = billing.get("billed", 0)
collected = billing.get("collected", 0)
receivable = billing.get("receivable", 0)

collection_rate = (
    collected / billed * 100
    if billed
    else 0
)

with b1:
    st.metric(
        "Billed",
        f"₹{billed / 1e7:,.2f} Cr"
    )

with b2:
    st.metric(
        "Collected",
        f"₹{collected / 1e7:,.2f} Cr"
    )

with b3:
    st.metric(
        "Receivable",
        f"₹{receivable / 1e7:,.2f} Cr"
    )

st.caption(
    f"Collection Rate: {collection_rate:.1f}%"
)

st.info(
    "💡 **Key Takeaway:** "
    f"{completion_rate:.1f}% of work orders are completed. "
    f"Collections are at {collection_rate:.1f}%, while missing "
    "closure probabilities limit sales forecast accuracy."
)


# =========================================================
# DATA QUALITY
# =========================================================

st.divider()

st.subheader("⚠️ Data Quality")

total_deals = len(deals)

try:
    probability_info = probability_quality(deals)

    valid_probability = int(
        probability_info.get("valid_probability", 0)
    )

    missing_probability = int(
        probability_info.get("missing_probability", 0)
    )

except Exception:
    valid_probability = 0
    missing_probability = 0


dq1, dq2, dq3 = st.columns(3)

with dq1:
    st.metric(
        "Total Deals",
        f"{total_deals:,}"
    )

with dq2:
    st.metric(
        "Valid Closure Probability",
        f"{valid_probability:,}"
    )

with dq3:
    st.metric(
        "Missing / Invalid Probability",
        f"{missing_probability:,}"
    )


if missing_probability > 0 or len(work_orders) != 177:

    st.warning(
        "Data quality issues were detected."
    )

    if len(work_orders) != 177:

        st.write(
            f"⚠️ Work Orders contains "
            f"**{len(work_orders)}** rows; expected **177**."
        )

    if missing_probability > 0:

        st.write(
            f"⚠️ **{missing_probability}** Deals have "
            "missing or invalid Closure Probability."
        )

else:

    st.success(
        "No major data quality issues detected."
    )

# =========================================================
# CONVERSATIONAL AGENT
# =========================================================

st.divider()

st.subheader(
    "🤖 Ask the BI Agent"
)


st.caption(
    "Ask questions about sales, projects, "
    "billing, execution or data quality."
)


# =========================================================
# QUICK QUESTIONS
# =========================================================

examples = [
    "What is our current sales pipeline?",
    "How much of the total work has been completed?",
    "Which sector has the highest deal value?",
    "What is our win rate?",
    "How much has been billed and collected?",
    "Are there any data quality issues?",

]


if "messages" not in st.session_state:

    st.session_state.messages = []


st.markdown(
    "**Quick questions:**"
)


cols = st.columns(3)


for i, question_text in enumerate(
    examples
):

    with cols[i % 3]:

        if st.button(
            question_text,
            key=f"example_{i}",
            use_container_width=True
        ):

            st.session_state.pending_question = (
                question_text
            )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask a business question..."
)


# =========================================================
# HANDLE QUICK QUESTION
# =========================================================

if "pending_question" in st.session_state:

    question = st.session_state.pop(
        "pending_question"
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    # Generate agent response
    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing monday.com data..."
        ):

            try:

                answer = ask_agent(
                    question
                )

            except Exception as e:

                answer = (
                    "Unable to process the question: "
                    f"{e}"
                )


        st.markdown(
            answer
        )


    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Skylark Drones BI Agent • "
    "Data sourced from monday.com"
)