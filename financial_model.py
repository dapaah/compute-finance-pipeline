import pandas as pd
import numpy as np

def run_financial_pipeline():
    print("⏳ Loading raw infrastructure file 'raw_infrastructure_logs.csv'...")
    
    # 1. Ingest the data you generated in the previous step
    try:
        df = pd.read_csv("raw_infrastructure_logs.csv")
    except FileNotFoundError:
        print("❌ Error: Could not find 'raw_infrastructure_logs.csv'. Run generate_logs.py first!")
        return

    print("🧹 Cleaning data and applying contract rate structures...")
    
    # 2. Replicate the SQL Cleansing View logic
    # Filter out dropped jobs that crashed and never cleanly ended (missing end_times)
    df = df.dropna(subset=['end_time']).copy()
    
    # Convert string timestamps to actual datetime objects for math operations
    df['start_time'] = pd.to_datetime(df['start_time'], format='mixed')
    df['end_time'] = pd.to_datetime(df['end_time'], format='mixed')
    
    # Standardize vendor string casings (e.g., 'aws' -> 'AWS')
    df['provider'] = df['provider'].str.upper()
    
    # 3. Calculate precise durations and operational volume metric
    df['duration_hours'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 3600.0
    df['total_gpu_hours'] = df['gpu_count'] * df['duration_hours']
    
    # Isolate the fiscal month for our corporate reporting timeline
    df['month'] = df['start_time'].dt.strftime('%Y-%m')

    # 4. Define our contractual matrix (Simulating our vendor rate cards table)
    rates = {
        ('AWS', 'H100'): 2.21, ('AWS', 'A100'): 1.10, ('AWS', 'B200'): 3.50,
        ('GCP', 'H100'): 2.15, ('GCP', 'A100'): 1.05, ('GCP', 'B200'): 3.45,
        ('OCI', 'H100'): 2.00, ('OCI', 'A100'): 0.95, ('OCI', 'B200'): 3.20,
    }
    
    # Map pricing directly to rows based on combined vendor and hardware types
    df['hourly_rate'] = df.set_index(['provider', 'gpu_type']).index.map(rates)
    df['gross_spend'] = df['total_gpu_hours'] * df['hourly_rate']

    # 5. Roll up calculations into standard monthly financial summaries
    monthly_summary = df.groupby('month').agg(
        total_gpu_hours=('total_gpu_hours', 'sum'),
        raw_cloud_spend=('gross_spend', 'sum')
    ).reset_index()

    print("📈 Structuring corporate 3-statement model lines...")
    
    # Context: Assume your AI lab purchased an on-prem cluster block of H100s for $60M cash in Jan
    HARDWARE_CAPEX = 60000000.00
    USEFUL_LIFE_YEARS = 5
    MONTHLY_DEPRECIATION = HARDWARE_CAPEX / (USEFUL_LIFE_YEARS * 12)

    # Compile the final board-ready framework
    financial_model = pd.DataFrame({
        'Month': monthly_summary['month'],
        'Cloud_OpEx_COGS': monthly_summary['raw_cloud_spend'],
        'Hardware_Depreciation': MONTHLY_DEPRECIATION,
        'CapEx_Cash_Outflow': np.where(monthly_summary['month'] == '2026-01', HARDWARE_CAPEX, 0.0),
    })

    # Account for full corporate cost of goods sold vs cash layouts
    financial_model['Total_GAAP_COGS'] = financial_model['Cloud_OpEx_COGS'] + financial_model['Hardware_Depreciation']
    financial_model['Total_Cash_Outflow'] = financial_model['Cloud_OpEx_COGS'] + financial_model['CapEx_Cash_Outflow']

    # Formatter mapping for clean boardroom presentation
    output_table = financial_model.copy()
    output_table['Cloud_OpEx_COGS'] = output_table['Cloud_OpEx_COGS'].map('${:,.2f}'.format)
    output_table['Hardware_Depreciation'] = output_table['Hardware_Depreciation'].map('${:,.2f}'.format)
    output_table['Total_GAAP_COGS'] = output_table['Total_GAAP_COGS'].map('${:,.2f}'.format)
    output_table['CapEx_Cash_Outflow'] = output_table['CapEx_Cash_Outflow'].map('${:,.2f}'.format)
    output_table['Total_Cash_Outflow'] = output_table['Total_Cash_Outflow'].map('${:,.2f}'.format)

    print("\n🚀 --- CONSOLIDATED COMPUTE RUN-RATE SUMMARY (GAAP VS CASH) ---")
    print(output_table.to_string(index=False))

if __name__ == "__main__":
    run_financial_pipeline()