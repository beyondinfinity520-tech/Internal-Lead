from typing import Optional
import requests
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config.settings import ScraperConfig
from ..core.parser import LinkedInParser
from ..models.job import JobCollection
from ..utils.constants import (
    LINKEDIN_JOBS_BASE_URL,
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY
)
from ..utils.logger import logger


class LinkedInScraper:
    """Main scraper class for LinkedIn job listings."""
    
    def __init__(self, config: ScraperConfig):
        """Initialize scraper with configuration."""
        self.config = config
        self.parser = LinkedInParser()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update(DEFAULT_HEADERS)
        # Add browser-like headers to avoid obfuscated data (****)
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Referer": "https://www.linkedin.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        })
        
        return session
    
    def _build_search_url(self, start: int = 0) -> str:
        """Build LinkedIn search URL with parameters."""
        base_url = f"{LINKEDIN_JOBS_BASE_URL}?keywords={self.config.search_query}"
        base_url += f"&location={self.config.location_query}"
        base_url += f"&start={start}"
        
        if self.config.experience:
            base_url += f"&f_E={self.config.experience}"
        
        return base_url
    
    def scrape(self) -> JobCollection:
        """Scrape LinkedIn jobs based on configuration."""
        logger.info(f"Starting scrape for: {self.config.keywords}")
        
        # Prime the session with cookies by visiting the jobs homepage first
        # This helps establish a valid session to avoid masked data (****)
        logger.debug("Priming session cookies...")
        self._fetch_html("https://www.linkedin.com/jobs")
        time.sleep(random.uniform(1, 2))
        
        all_jobs = JobCollection()
        start = 0
        
        while len(all_jobs) < self.config.max_jobs:
            search_url = self._build_search_url(start)
            logger.debug(f"Search URL: {search_url}")
            
            try:
                html_content = self._fetch_html(search_url)
                
                if not html_content:
                    logger.warning(f"Failed to fetch HTML content for start={start}")
                    break
                
                # Calculate remaining jobs needed
                remaining = self.config.max_jobs - len(all_jobs)
                batch_jobs = self.parser.parse_html(html_content, remaining)
                
                if len(batch_jobs) == 0:
                    logger.info("No more jobs found on this page")
                    break
                
                all_jobs.add_multiple(batch_jobs.jobs)
                logger.info(f"Found {len(batch_jobs)} jobs (Total: {len(all_jobs)})")
                
                start += 25
                
                if len(all_jobs) < self.config.max_jobs:
                    delay = random.uniform(2, 5)
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Scraping failed at start={start}: {str(e)}", exc_info=True)
                break
        
        logger.success(f"Scraped total {len(all_jobs)} jobs")
        return all_jobs
    
    def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL."""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Check if redirected to login or authwall
            if "login" in response.url or "authwall" in response.url or "challenge" in response.url:
                logger.warning(f"LinkedIn redirected to auth page: {response.url}")
                return None

            logger.debug(f"Successfully fetched URL: {url}")
            return response.text
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code}")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error occurred")
            return None
            
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return None
    
    def close(self) -> None:
        """Close the session."""
        if self.session:
            self.session.close()
            logger.debug("Session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        