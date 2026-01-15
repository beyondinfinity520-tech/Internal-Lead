from typing import Optional
from bs4 import BeautifulSoup, Tag

from ..models.job import Job, JobCollection
from ..utils.constants import LINKEDIN_SELECTORS, DATA_SOURCE
from ..utils.logger import logger


class LinkedInParser:
    """Parser for LinkedIn job search results."""
    
    def __init__(self):
        self.selectors = LINKEDIN_SELECTORS
        self.data_source = DATA_SOURCE
    
    def parse_html(self, html_content: str, max_jobs: int = 50) -> JobCollection:
        """Parse HTML content and extract job listings."""
        soup = BeautifulSoup(html_content, 'html.parser')
        job_collection = JobCollection()
        
        job_cards = soup.find_all('div', class_=self.selectors["job_card"])
        
        if not job_cards:
            logger.warning("No job cards found in HTML content")
            return job_collection
        
        for card in job_cards:
            if len(job_collection) >= max_jobs:
                break
            
            job = self._parse_job_card(card)
            if job:
                job_collection.add(job)
        
        return job_collection
    
    def _parse_job_card(self, card: Tag) -> Optional[Job]:
        """Parse a single job card element."""
        try:
            title = self._extract_text(card, 'h3', self.selectors["title"])
            company = self._extract_text(card, 'h4', self.selectors["company"])
            location = self._extract_text(card, 'span', self.selectors["location"])
            link = self._extract_link(card)
            
            if not all([title, company, location, link]):
                logger.debug("Skipping job card due to missing fields")
                return None
            
            job = Job(
                title=title,
                company=company,
                location=location,
                link=link,
                source=self.data_source
            )
            
            return job if job.validate() else None
            
        except Exception as e:
            logger.error(f"Error parsing job card: {str(e)}")
            return None
    
    def _extract_text(self, card: Tag, tag: str, class_name: str) -> Optional[str]:
        """Extract text from a specific element."""
        element = card.find(tag, class_=class_name)
        return element.get_text(strip=True) if element else None
    
    def _extract_link(self, card: Tag) -> Optional[str]:
        """Extract job link from card."""
        link_tag = card.find('a', class_=self.selectors["link"])
        
        if link_tag and link_tag.has_attr('href'):
            return link_tag['href']
        
        return None
    