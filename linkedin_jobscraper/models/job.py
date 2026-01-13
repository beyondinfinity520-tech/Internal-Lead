from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Job:
    title: str
    company: str
    location: str
    job_url: str
    company_website: str = "N/A"           
    company_linkedin_url: str = "N/A"      
    industry: str = "Staffing and Recruiting"
    meet_hiring_team_name: str = "Not Listed"
    meet_hiring_team_url: str = "Not Listed"

class JobCollection:
    def __init__(self):
        self.jobs: List[Job] = []

    def add_job(self, job: Job):
        self.jobs.append(job)

    def to_list_of_dicts(self) -> List[Dict]:
        return [asdict(job) for job in self.jobs]