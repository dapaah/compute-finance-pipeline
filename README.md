# AI Cluster Compute Spend & Financial Forecasting Pipeline

## 📊 Project Overview
This data pipeline automatically ingests, standardizes, and models high-volume infrastructure logs to track GPU consumption metrics across internal research and API teams. 

## 🛠️ Technical Architecture
* **Data Generation (Python):** Simulates 100,000 rows of granular compute logs mapping cluster runtimes, resource counts, and cloud service providers.
* **Data Cleansing (SQL/Pandas):** Mimics standard database warehouse aggregation pipelines by handling aborted server logs, standardizing casing, and executing multi-key joins against variable vendor rate cards.
* **Financial Modeling (Pandas):** Implements corporate asset tracking mechanisms, straight-line 5-year hardware depreciation schedules, and volume-tier threshold breaks.

## 📈 Strategic Finance Observations
* **GAAP vs. Cash Separation:** The model demonstrates core corporate cash decoupling by mapping a $60M cash equipment acquisition (CapEx) against uniform $1M straight-line depreciation charges on the Income Statement without creating systemic run-rate volatility.
* **Run-Rate Visibility:** Provides executive leadership teams with granular cloud OpEx clarity versus fixed capitalization outlays across distinct fiscal months.
