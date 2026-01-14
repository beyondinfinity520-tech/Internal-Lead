from dataclasses import dataclass
from typing import Optional

@dataclass
class ScraperConfig:
    
    keywords: str = "bench sales" 
    location: str = ""
    industry: int = 104
    max_jobs: int = 5       
    max_pages: int = 3       
    max_scrolls: int = 5      

@dataclass
class OutputConfig:
    output_file: str = "linkedin_leads.csv"
    output_format: str = "csv"