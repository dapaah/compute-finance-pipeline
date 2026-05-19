<<<<<<< HEAD
import sqlite3
import pandas as pd

def build_local_data_warehouse():
    print("🗄️ Initializing local SQLite database 'compute_warehouse.db'...")
    
    # 1. Establish database connection (creates the file if it doesn't exist)
    conn = sqlite3.connect("compute_warehouse.db")
    cursor = conn.cursor()
    
    # 2. Ingest your CSV data directly into a raw SQL staging table
    print("⏳ Staging 100,000 raw log rows into SQL environment...")
    try:
        raw_data = pd.read_csv("raw_infrastructure_logs.csv")
        raw_data.to_sql("raw_infrastructure_logs", conn, if_exists="replace", index=False)
    except FileNotFoundError:
        print("❌ Error: 'raw_infrastructure_logs.csv' not found! Run generate_logs.py first.")
        return

    # 3. Inject our Mock Vendor Rate Cards into a SQL Dimension Table
    print("💳 Populating contractual vendor rate cards...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor_rate_cards (
            provider TEXT,
            gpu_type TEXT,
            hourly_rate_per_gpu REAL
        )
    """)
    
    # Clear old data and insert baseline vendor contract layers
    cursor.execute("DELETE FROM vendor_rate_cards")
    rate_card_data = [
        ('AWS', 'H100', 2.21), ('AWS', 'A100', 1.10), ('AWS', 'B200', 3.50),
        ('GCP', 'H100', 2.15), ('GCP', 'A100', 1.05), ('GCP', 'B200', 3.45),
        ('OCI', 'H100', 2.00), ('OCI', 'A100', 0.95), ('OCI', 'B200', 3.20)
    ]
    cursor.executemany("INSERT INTO vendor_rate_cards VALUES (?, ?, ?)", rate_card_data)
    conn.commit()

    # 4. RUN PRODUCTION-GRADE DATA CLEANING & ANALYTICS VIA SQL
    print("🔍 Executing Advanced CTE Analytics Query...")
    
    advanced_sql_query = """
    WITH cleansed_logs AS (
        SELECT 
            job_id,
            team_name,
            -- Handle lowercase anomalies natively in SQL
            UPPER(provider) AS provider,
            gpu_type,
            gpu_count,
            -- Parse string dates into SQL-readable fragments
            strftime('%Y-%m', start_time) AS fiscal_month,
            -- Calculate precise job duration hours
            (julianday(end_time) - julianday(start_time)) * 24.0 AS duration_hours
        FROM raw_infrastructure_logs
        -- Handle server crash anomalies (The Left Join Trap protection fallback)
        WHERE end_time IS NOT NULL
    ),
    ccompute_metrics AS (
        SELECT 
            c.fiscal_month,
            c.team_name,
            (c.gpu_count * c.duration_hours) AS total_gpu_hours,
            -- IF a contract rate is missing, flag it with a 1.5x On-Demand penalty rate
            CASE 
                WHEN v.hourly_rate_per_gpu IS NOT NULL THEN (c.gpu_count * c.duration_hours * v.hourly_rate_per_gpu)
                ELSE (c.gpu_count * c.duration_hours * 3.50 * 1.5) -- $3.50 base penalty multiplied by 1.5x risk premium
            END AS job_cost
        FROM cleansed_logs c
        -- Switch from INNER JOIN to LEFT JOIN to protect against disappearing data
        LEFT JOIN vendor_rate_cards v 
           ON c.provider = v.provider 
          AND c.gpu_type = v.gpu_type
    )
    SELECT 
        fiscal_month AS "Month",
        team_name AS "Engineering_Team",
        ROUND(SUM(total_gpu_hours), 2) AS "Total_GPU_Hours",
        ROUND(SUM(job_cost), 2) AS "Total_Compute_Spend"
    FROM compute_metrics
    GROUP BY fiscal_month, team_name
    ORDER BY fiscal_month ASC, Total_Compute_Spend DESC;
    """
    
    # 5. Output analytics frame back to the terminal layout
    analytics_df = pd.read_sql_query(advanced_sql_query, conn)
    
    print("\n🚀 --- CORPORATE DATABASE DATA INGESTION ANALYSIS VIEW ---")
    print(analytics_df.head(15).to_string(index=False)) # Printing the top 15 rows
    
    conn.close()

if __name__ == "__main__":
    build_local_data_warehouse()
=======
import sqlite3
import pandas as pd

def build_local_data_warehouse():
    print("🗄️ Initializing local SQLite database 'compute_warehouse.db'...")
    
    # 1. Establish database connection (creates the file if it doesn't exist)
    conn = sqlite3.connect("compute_warehouse.db")
    cursor = conn.cursor()
    
    # 2. Ingest your CSV data directly into a raw SQL staging table
    print("⏳ Staging 100,000 raw log rows into SQL environment...")
    try:
        raw_data = pd.read_csv("raw_infrastructure_logs.csv")
        raw_data.to_sql("raw_infrastructure_logs", conn, if_exists="replace", index=False)
    except FileNotFoundError:
        print("❌ Error: 'raw_infrastructure_logs.csv' not found! Run generate_logs.py first.")
        return

    # 3. Inject our Mock Vendor Rate Cards into a SQL Dimension Table
    print("💳 Populating contractual vendor rate cards...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendor_rate_cards (
            provider TEXT,
            gpu_type TEXT,
            hourly_rate_per_gpu REAL
        )
    """)
    
    # Clear old data and insert baseline vendor contract layers
    cursor.execute("DELETE FROM vendor_rate_cards")
    rate_card_data = [
        ('AWS', 'H100', 2.21), ('AWS', 'A100', 1.10), ('AWS', 'B200', 3.50),
        ('GCP', 'H100', 2.15), ('GCP', 'A100', 1.05), ('GCP', 'B200', 3.45),
        ('OCI', 'H100', 2.00), ('OCI', 'A100', 0.95), ('OCI', 'B200', 3.20)
    ]
    cursor.executemany("INSERT INTO vendor_rate_cards VALUES (?, ?, ?)", rate_card_data)
    conn.commit()

    # 4. RUN PRODUCTION-GRADE DATA CLEANING & ANALYTICS VIA SQL
    print("🔍 Executing Advanced CTE Analytics Query...")
    
    advanced_sql_query = """
    WITH cleansed_logs AS (
        SELECT 
            job_id,
            team_name,
            -- Handle lowercase anomalies natively in SQL
            UPPER(provider) AS provider,
            gpu_type,
            gpu_count,
            -- Parse string dates into SQL-readable fragments
            strftime('%Y-%m', start_time) AS fiscal_month,
            -- Calculate precise job duration hours
            (julianday(end_time) - julianday(start_time)) * 24.0 AS duration_hours
        FROM raw_infrastructure_logs
        -- Handle server crash anomalies (The Left Join Trap protection fallback)
        WHERE end_time IS NOT NULL
),
    compute_metrics AS (
        SELECT 
            c.fiscal_month,
            c.team_name,
            (c.gpu_count * c.duration_hours) AS total_gpu_hours,
            -- IF a contract rate is missing, flag it with a 1.5x On-Demand penalty rate
            CASE 
                WHEN v.hourly_rate_per_gpu IS NOT NULL THEN (c.gpu_count * c.duration_hours * v.hourly_rate_per_gpu)
                ELSE (c.gpu_count * c.duration_hours * 3.50 * 1.5) -- $3.50 base penalty multiplied by 1.5x risk premium
            END AS job_cost
        FROM cleansed_logs c
        -- Switch from INNER JOIN to LEFT JOIN to protect against disappearing data
        LEFT JOIN vendor_rate_cards v 
           ON c.provider = v.provider 
          AND c.gpu_type = v.gpu_type
    )
    SELECT 
        fiscal_month AS "Month",
        team_name AS "Engineering_Team",
        ROUND(SUM(total_gpu_hours), 2) AS "Total_GPU_Hours",
        ROUND(SUM(job_cost), 2) AS "Total_Compute_Spend"
    FROM compute_metrics
    GROUP BY fiscal_month, team_name
    ORDER BY fiscal_month ASC, Total_Compute_Spend DESC;
    """
    
    # 5. Output analytics frame back to the terminal layout
    analytics_df = pd.read_sql_query(advanced_sql_query, conn)
    
    print("\n🚀 --- CORPORATE DATABASE DATA INGESTION ANALYSIS VIEW ---")
    print(analytics_df.head(15).to_string(index=False)) # Printing the top 15 rows
    
    conn.close()

if __name__ == "__main__":
    build_local_data_warehouse()
>>>>>>> 27a0a2e (Feature: Upgraded staging warehouse view to LEFT JOIN with penalty rates)
