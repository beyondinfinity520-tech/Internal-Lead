from dataclasses import dataclass

@dataclass
class ScraperConfig:
    keywords: str = "bench sales"
    location: str = "" 
    industry: str = "Staffing and Recruiting"
    
    # Defaults (Overridden by UI)
    max_jobs: int = 10 
    wait_time: int = 15
    
    output_file: str = "output/naukri_leads.csv"