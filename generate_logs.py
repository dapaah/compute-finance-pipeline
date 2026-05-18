import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_compute_logs(num_rows=100000):
    print("⏳ Spawning 100,000 raw infrastructure log rows...")
    np.random.seed(42)
    teams = ['Core_LLM', 'Inference_API', 'Vision_Models', 'Alignment', 'Bio_Med', 'Voice_AI']
    providers = ['AWS', 'GCP', 'OCI', 'aws', 'gcp']
    gpu_pool = {
        'H100': [8, 16, 32, 64, 512, 2048],
        'A100': [4, 8, 16, 32, 128],
        'B200': [32, 64, 512]
    }
    
    start_date = datetime(2026, 1, 1)
    logs = []
    
    for i in range(num_rows):
        job_id = f"job_run_{100000 + i}"
        team = np.random.choice(teams)
        provider = np.random.choice(providers)
        gpu_type = np.random.choice(list(gpu_pool.keys()))
        gpu_count = np.random.choice(gpu_pool[gpu_type])
        
        random_days = np.random.randint(0, 120)
        random_hours = np.random.randint(0, 24)
        job_start = start_date + timedelta(days=random_days, hours=random_hours)
        
        job_duration = np.random.exponential(scale=18)
        job_duration = max(0.25, min(job_duration, 168))
        
        if np.random.rand() < 0.015:
            job_end = None
        else:
            job_end = job_start + timedelta(hours=job_duration)
            
        logs.append([job_id, team, provider, gpu_type, gpu_count, job_start, job_end])
        
    df = pd.DataFrame(logs, columns=['job_id', 'team_name', 'provider', 'gpu_type', 'gpu_count', 'start_time', 'end_time'])
    
    # Save a local copy right inside your folder to look at later!
    df.to_csv("raw_infrastructure_logs.csv", index=False)
    print("💾 Raw logs generated and cached locally as 'raw_infrastructure_logs.csv'")
    return df

if __name__ == "__main__":
    generate_compute_logs(100000)