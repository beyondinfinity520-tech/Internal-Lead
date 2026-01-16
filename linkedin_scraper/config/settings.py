class ScraperConfig:
    """Configuration class for scraper settings."""
    
    def __init__(
        self,
        keywords: str = "bench sales bdm",
        location: str = "",
        max_jobs: int = 50,
        skills: str = "",
        experience: str = ""
    ):
        self.keywords = keywords
        self.location = location
        self.max_jobs = max_jobs
        self.skills = skills
        self.experience = experience
        
    @property
    def combined_keywords(self) -> str:
        """Combine keywords with skills for search query."""
        combined = self.keywords
        if self.skills:
            combined += " " + self.skills.replace(",", " ")
        return combined.strip()
    
    @property
    def search_query(self) -> str:
        """Convert keywords to URL-encoded query string."""
        return self.combined_keywords.replace(" ", "+")
    
    @property
    def location_query(self) -> str:
        """Convert location to URL-encoded query string."""
        return self.location.replace(" ", "+")
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "keywords": self.keywords,
            "location": self.location,
            "max_jobs": self.max_jobs,
            "skills": self.skills,
            "experience": self.experience
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScraperConfig':
        """Create config from dictionary."""
        return cls(
            keywords=data.get("keywords", "Data Scientist"),
            location=data.get("location", "USA"),
            max_jobs=data.get("maxJobs", 50),
            skills=data.get("skills", ""),
            experience=data.get("experience", "")
        )


class OutputConfig:
    """Configuration for output settings."""
    
    def __init__(
        self,
        output_file: str = "jobs.csv",
        output_format: str = "csv"
    ):
        self.output_file = output_file
        self.output_format = output_format
        
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "output_file": self.output_file,
            "output_format": self.output_format
        }
        