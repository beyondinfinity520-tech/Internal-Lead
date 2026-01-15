from dataclasses import dataclass, asdict
from typing import Optional, List, Dict


@dataclass
class Job:
    """Job data model representing a single job posting."""
    
    title: str
    company: str
    location: str
    link: str
    source: str = "LinkedIn"
    description: Optional[str] = None
    posted_date: Optional[str] = None
    employment_type: Optional[str] = None
    seniority_level: Optional[str] = None
    
    def to_dict(self) -> Dict[str, any]:
        """Convert job to dictionary."""
        return asdict(self)
    
    def validate(self) -> bool:
        """Validate that required fields are present."""
        required_fields = [self.title, self.company, self.location, self.link]
        
        # Check basic presence
        if not all(field and isinstance(field, str) and field.strip() for field in required_fields):
            return False
            
        # Check for masked data (anti-scraping protection)
        if any("****" in field for field in required_fields):
            return False
            
        return True
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Job':
        """Create Job instance from dictionary."""
        return cls(
            title=data.get("title", ""),
            company=data.get("company", ""),
            location=data.get("location", ""),
            link=data.get("link", ""),
            source=data.get("source", "LinkedIn"),
            description=data.get("description"),
            posted_date=data.get("posted_date"),
            employment_type=data.get("employment_type"),
            seniority_level=data.get("seniority_level")
        )
    
    def __str__(self) -> str:
        """String representation of job."""
        return f"{self.title} at {self.company} - {self.location}"


class JobCollection:
    """Collection of jobs with utility methods."""
    
    def __init__(self):
        self.jobs: List[Job] = []
    
    def add(self, job: Job) -> None:
        """Add a job to the collection."""
        if job.validate():
            self.jobs.append(job)
    
    def add_multiple(self, jobs: List[Job]) -> None:
        """Add multiple jobs to the collection."""
        for job in jobs:
            self.add(job)
    
    def to_list(self) -> List[Dict[str, any]]:
        """Convert collection to list of dictionaries."""
        return [job.to_dict() for job in self.jobs]
    
    def filter_by_company(self, company: str) -> List[Job]:
        """Filter jobs by company name."""
        return [job for job in self.jobs if company.lower() in job.company.lower()]
    
    def filter_by_location(self, location: str) -> List[Job]:
        """Filter jobs by location."""
        return [job for job in self.jobs if location.lower() in job.location.lower()]
    
    def __len__(self) -> int:
        """Return number of jobs in collection."""
        return len(self.jobs)
    
    def __iter__(self):
        """Make collection iterable."""
        return iter(self.jobs)
    
    def __getitem__(self, index: int) -> Job:
        """Get job by index."""
        return self.jobs[index]
    