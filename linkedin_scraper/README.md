# LinkedIn Job Scraper

A modular, production-ready LinkedIn job scraper built with OOP principles and industry best practices.

## Features

* **Modular Architecture** : Clean separation of concerns with dedicated modules for configuration, scraping, parsing, and models
* **Type Safety** : Uses Python type hints throughout for better code quality
* **Error Handling** : Robust error handling with retry mechanisms and proper logging
* **Configurable** : Flexible configuration system supporting multiple input methods
* **Extensible** : Easy to extend with new features or integrate into existing projects
* **Production Ready** : Follows industry standards and best practices

## Project Structure

```
linkedin_scraper/
├── config/              # Configuration management
│   ├── __init__.py
│   └── settings.py      # ScraperConfig and OutputConfig classes
├── core/                # Core scraping functionality
│   ├── __init__.py
│   ├── scraper.py       # LinkedInScraper class
│   └── parser.py        # LinkedInParser class
├── utils/               # Utility functions and constants
│   ├── __init__.py
│   ├── constants.py     # All constants and static configs
│   └── logger.py        # Logging utilities
├── models/              # Data models
│   ├── __init__.py
│   └── job.py           # Job and JobCollection classes
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `user_details.json` file (for standalone usage):

```json
{
  "keywords": "Data Scientist",
  "location": "USA",
  "maxJobs": 50,
  "skills": "Python, Machine Learning",
  "experience": "2"
}
```

## Usage

### Standalone Usage

Run directly:

```bash
python main.py
```

### Integration with Apify Universal Scraper

Import and use the main function:

```python
from main import scrape_linkedin_jobs

input_data = {
    "keywords": "Software Engineer",
    "location": "San Francisco",
    "maxJobs": 30,
    "skills": "Python, JavaScript",
    "experience": "3",
    "outputFile": "jobs.csv",
    "outputFormat": "csv"
}

results = scrape_linkedin_jobs(input_data)
```

### Programmatic Usage

```python
from config import ScraperConfig, OutputConfig
from main import JobScraperService

# Create configuration
scraper_config = ScraperConfig(
    keywords="Data Analyst",
    location="Remote",
    max_jobs=25,
    skills="SQL, Excel",
    experience="2"
)

output_config = OutputConfig(
    output_file="data_analyst_jobs.csv",
    output_format="csv"
)

# Run scraper
service = JobScraperService(scraper_config, output_config)
jobs = service.run()
```

## Configuration Options

### Scraper Configuration

* **keywords** : Job title or role (e.g., "Software Engineer")
* **location** : Job location (e.g., "New York" or "Remote")
* **maxJobs** : Maximum number of jobs to scrape (default: 20)
* **skills** : Comma-separated skills to include in search (optional)
* **experience** : Experience level filter (1-6):
* 1: Internship
* 2: Entry level
* 3: Associate
* 4: Mid-Senior level
* 5: Director
* 6: Executive

### Output Configuration

* **outputFile** : Output file path (default: "jobs.csv")
* **outputFormat** : Output format - "csv" or "json" (default: "csv")
