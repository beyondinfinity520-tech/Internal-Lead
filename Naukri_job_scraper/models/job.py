from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Job:
    title: str
    industry: str
    company_name: str
    job_url: str
    company_website: str = "N/A"

class JobCollection:
    def __init__(self):
        self.jobs: List[Job] = []

    def add_job(self, job: Job):
        self.jobs.append(job)

    def to_list_of_dicts(self) -> List[Dict]:
        return [asdict(job) for job in self.jobs]