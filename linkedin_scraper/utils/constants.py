# URL Configuration
LINKEDIN_JOBS_BASE_URL = "https://www.linkedin.com/jobs/search"

# HTTP Headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Experience Level Mapping
EXPERIENCE_LEVEL_MAP = {
    "1": "Internship",
    "2": "Entry level",
    "3": "Associate",
    "4": "Mid-Senior level",
    "5": "Director",
    "6": "Executive"
}

# HTML Class Names for LinkedIn Job Cards
LINKEDIN_SELECTORS = {
    "job_card": "base-search-card",
    "title": "base-search-card__title",
    "company": "base-search-card__subtitle",
    "location": "job-search-card__location",
    "link": "base-card__full-link"
}

# Data Source Identifier
DATA_SOURCE = "LinkedIn"

# Default Values
DEFAULT_MAX_JOBS = 50
DEFAULT_KEYWORDS = "bench sales, bdm"
DEFAULT_LOCATION = ""

# Output Configuration
DEFAULT_OUTPUT_FILE = "jobs.csv"
DEFAULT_OUTPUT_FORMAT = "csv"

# Request Configuration
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2
