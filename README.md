# Skylark Drones – Business Intelligence & Conversational Agent

## Project Overview

This project provides a Business Intelligence dashboard and conversational agent for Skylark Drones using live data retrieved from monday.com.

The application combines:
- monday.com API integration
- Sales/deal analysis
- Work-order execution analysis
- Billing and collection metrics
- Data-quality checks
- Streamlit dashboard visualization
- Conversational business-question answering

## Dashboard Features

### Business Overview
The dashboard displays:
- Total Deals
- Work Orders
- Sales Pipeline
- Weighted Pipeline
- Win Rate

### Operational Execution
The dashboard displays:
- Completed Work Orders
- Completion Rate
- Ongoing Work Orders
- Execution-status chart

### Deal Analysis
- Deal value by sector
- Identification of high-value sectors

### Billing & Collections
- Billed amount
- Collected amount
- Receivable amount

### Data Quality
The dashboard highlights detected issues such as:
- Work Order count mismatch
- Missing or invalid Closure Probability values

### Conversational BI Agent
Users can ask natural-language questions such as:
- What is our current sales pipeline?
- What is our win rate?
- How much of the total work has been completed?
- Which sector has the highest deal value?
- How much has been billed and collected?
- Are there any data quality issues?

## Current Data Snapshot

The current dataset used during testing contains:
- 346 Deals
- 176 Work Orders
- Sales Pipeline: approximately ₹230.55 Cr
- Weighted Pipeline: approximately ₹28.68 Cr
- Win Rate: 56.51%
- Completed Work Orders: 117 / 176
- Completion Rate: 66.5%
- Billed: approximately ₹10.74 Cr
- Collected: approximately ₹9.04 Cr
- Receivable: approximately ₹3.63 Cr

## Known Data Quality Issues

Two issues were identified during testing:

1. Work Orders
   - 176 records are present
   - 177 were expected

2. Closure Probability
   - 260 of 346 deals have missing or invalid Closure Probability
   - Therefore, the weighted pipeline should be interpreted with caution because only 86 deals have valid probability data.

Missing Closure Probability is treated as missing data, not as zero probability.

## Project Structure

Expected project structure:

    skylark-monday/
    ├── app.py
    ├── agent.py
    ├── monday_client.py
    ├── data_processor.py
    ├── bi_tools.py
    ├── test_bi.py
    ├── test_monday.py
    ├── monday_ai_test.py
    ├── requirements.txt
    ├── .env
    └── README.md

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Configure monday.com API token

Create a `.env` file in the project directory:

    MONDAY_API_TOKEN=your_monday_api_token

Do NOT commit or submit the `.env` file.

### 4. Test the monday.com connection

    py test_monday.py

The test should show the available monday.com boards.

### 5. Test the BI calculations

    py test_bi.py

### 6. Run the Streamlit application

    streamlit run app.py

Open the local URL shown by Streamlit in the browser.

## Data Flow

    monday.com
         |
         v
    monday_client.py
         |
         v
    data_processor.py
         |
         v
      bi_tools.py
         |
         +--------------------+
         |                    |
         v                    v
    Streamlit Dashboard   Conversational Agent
         |                    |
         +---------+----------+
                   |
                   v
             Business Insights

## Security

The monday.com API token is a secret.

Never upload:
- `.env`
- API tokens
- passwords
- private credentials

A `.env.example` file can be used as a safe template:

    MONDAY_API_TOKEN=

## Final Testing Checklist

Before submission:

- [ ] monday.com API connection works
- [ ] Deals load successfully
- [ ] Work Orders load successfully
- [ ] Pipeline is displayed correctly
- [ ] Weighted Pipeline is displayed correctly
- [ ] Win Rate displays as 56.51% rather than 0.57%
- [ ] Work completion displays 117 / 176
- [ ] Billing values are displayed correctly
- [ ] Data-quality warnings are displayed
- [ ] Quick questions work
- [ ] Free-text BI questions work
- [ ] Refresh Data button works
- [ ] `.env` is excluded from submission

## Important Win Rate Formatting

The win-rate calculation returns a decimal value such as `0.5651`.

Therefore Streamlit should format it using:

    st.metric("Win Rate", f"{win_rate:.2%}")

Do not append `%` manually with `:.2f`, because that would display `0.57%` instead of `56.51%`.

## Conclusion

The completed application provides a single interface for monitoring sales pipeline, operational execution, billing, collections, and data quality while allowing users to ask business questions in natural language.
