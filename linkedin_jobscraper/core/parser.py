from bs4 import BeautifulSoup
from ..models.job import Job
from typing import List

class LinkedInParser:
    @staticmethod
    def parse_jobs(page_source: str) -> List[Job]:
        soup = BeautifulSoup(page_source, "html.parser")
        jobs_list = []

        
        job_cards = soup.select("li.jobs-search-results__list-item")
        for card in job_cards:
            try:
                title = card.select_one("div.artdeco-entity-lockup__title").get_text(strip=True)
                company = card.select_one("div.artdeco-entity-lockup__subtitle").get_text(strip=True)
                location_tag = card.select_one("div.artdeco-entity-lockup__caption")
                location = location_tag.get_text(strip=True) if location_tag else None
                metadata_tag = card.select_one("div.artdeco-entity-lockup__metadata")
                metadata = metadata_tag.get_text(strip=True) if metadata_tag else None
                job_url = card.select_one("a")["href"]

                jobs_list.append(Job(title, company, job_url, None, []))
            except Exception as e:
                continue

        return jobs_list
