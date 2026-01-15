import json
import pandas as pd
from typing import Dict, List, Optional

from .config.settings import ScraperConfig, OutputConfig
from .core.scraper import LinkedInScraper
from .utils.logger import logger


class JobScraperService:
    """Service class to orchestrate job scraping operations."""
    
    def __init__(self, scraper_config: ScraperConfig, output_config: Optional[OutputConfig] = None):
        """Initialize scraper service."""
        self.scraper_config = scraper_config
        self.output_config = output_config
    
    def run(self) -> List[Dict]:
        """Run the scraping process."""
        logger.info("Initializing LinkedIn Job Scraper")
        logger.info(f"Search parameters: {self.scraper_config.to_dict()}")
        
        with LinkedInScraper(self.scraper_config) as scraper:
            job_collection = scraper.scrape()
        
        if len(job_collection) == 0:
            logger.warning("No jobs were scraped")
            return []
        
        jobs_data = job_collection.to_list()
        
        # Save to file if configured
        if self.output_config and self.output_config.output_file:
            self._save_to_file(jobs_data)
        
        return jobs_data
    
    def _save_to_file(self, jobs_data: List[Dict]) -> None:
        """Save jobs data to file."""
        try:
            if self.output_config.output_format == "csv":
                df = pd.DataFrame(jobs_data)
                df.to_csv(self.output_config.output_file, index=False)
                logger.success(f"Saved {len(jobs_data)} jobs to {self.output_config.output_file}")
            
            elif self.output_config.output_format == "json":
                with open(self.output_config.output_file, 'w') as f:
                    json.dump(jobs_data, f, indent=2)
                logger.success(f"Saved {len(jobs_data)} jobs to {self.output_config.output_file}")
            
            else:
                logger.error(f"Unsupported output format: {self.output_config.output_format}")
        
        except Exception as e:
            logger.error(f"Failed to save output: {str(e)}", exc_info=True)


def scrape_linkedin_jobs(input_data: Dict) -> List[Dict]:
    """Main function to be called by Apify Universal Scraper or other integrations."""
    # Create configuration from input
    scraper_config = ScraperConfig.from_dict(input_data)
    
    # Optional output configuration
    output_config = None
    if input_data.get("outputFile"):
        output_config = OutputConfig(
            output_file=input_data.get("outputFile", "jobs.csv"),
            output_format=input_data.get("outputFormat", "csv")
        )
    
    # Run scraper
    service = JobScraperService(scraper_config, output_config)
    return service.run()


def main():
    """
    Entry point for standalone execution.
    Reads configuration from user_details.json file.
    """
    try:
        with open('user_details.json', 'r') as f:
            config_data = json.load(f)
        
        logger.info("Loaded configuration from user_details.json")
        
    except FileNotFoundError:
        logger.warning("user_details.json not found, using default configuration")
        config_data = {
            "keywords": "bench sales, bdm",
            "location": "",
            "maxJobs": 50,
            "skills": "",
            "experience": ""
        }
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in user_details.json: {str(e)}")
        return
    
    # Run scraper
    results = scrape_linkedin_jobs(config_data)
    
    logger.info(f"Scraping completed. Total jobs found: {len(results)}")


if __name__ == "__main__":
    main()
    