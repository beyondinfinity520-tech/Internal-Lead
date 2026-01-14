import os
import sys
from dotenv import load_dotenv

# Import the refactored functions from each scraper module
from linkedin_jobscraper.main import run_batch as run_linkedin_jobs_batch
from linkedin_post_scraper.main import run_batch as run_linkedin_posts_batch
from Naukri_job_scraper.main import run_batch as run_naukri_batch

# Import the email sender actor main function
# This allows us to run the emailer from this main script based on an env var
from email_sender_actor.main import main as run_email_sender

load_dotenv()

# --- Apify Integration ---
# In a real Apify actor, you would use the 'apify_client' or 'Actor' SDK.
# This is a simulation of how you would push data.

def get_dataset_client():
    """
    Initializes and returns an Apify dataset client.
    On the Apify platform, API_TOKEN and DEFAULT_DATASET_ID are injected.
    For local testing, you would need to set these in your .env file.
    """
    try:
        from apify_client import ApifyClient
        
        # Check for manually set token OR system provided token (APIFY_TOKEN is default on Apify)
        token = os.getenv("APIFY_API_TOKEN") or os.getenv("APIFY_TOKEN")
        if not token:
            print("CRITICAL: No APIFY_TOKEN found. Cannot connect to Apify Storage.")
            return None
            
        client = ApifyClient(token)
        # Using the specific named dataset "internal-lead"
        return client.datasets().get_or_create(name="internal-lead")
    except ImportError:
        print("Apify client not installed. Skipping data push. `pip install apify-client`")
        return None
    except Exception as e:
        print(f"Could not initialize Apify client: {e}")
        return None

def run_scraper():
    """
    Executes the scraping logic for all three scrapers.
    """
    dataset_client = get_dataset_client()

    print("--- Starting Unified Scraper Run ---")

    # 1. Run LinkedIn Job Scraper
    print("\n--- Running LinkedIn Job Scraper ---")
    try:
        linkedin_jobs = run_linkedin_jobs_batch()
        if linkedin_jobs:
            if dataset_client:
                for job in linkedin_jobs: job['source'] = 'linkedin_jobs'
                print(f"Found {len(linkedin_jobs)} LinkedIn jobs. Pushing to dataset...")
                dataset_client.push_items(linkedin_jobs)
            else:
                print(f"WARNING: Scraped {len(linkedin_jobs)} LinkedIn jobs but Dataset Client is missing. Data NOT saved.")
    except Exception as e:
        print(f"CRITICAL FAILURE in LinkedIn Job Scraper: {e}. Continuing to next scraper.")

    # 2. Run LinkedIn Post Scraper
    print("\n--- Running LinkedIn Post Scraper ---")
    try:
        linkedin_posts = run_linkedin_posts_batch()
        if linkedin_posts:
            if dataset_client:
                for post in linkedin_posts: post['source'] = 'linkedin_posts'
                print(f"Found {len(linkedin_posts)} LinkedIn posts. Pushing to dataset...")
                dataset_client.push_items(linkedin_posts)
            else:
                print(f"WARNING: Scraped {len(linkedin_posts)} LinkedIn posts but Dataset Client is missing. Data NOT saved.")
    except Exception as e:
        print(f"CRITICAL FAILURE in LinkedIn Post Scraper: {e}. Continuing to next scraper.")

    # 3. Run Naukri Job Scraper
    print("\n--- Running Naukri Job Scraper ---")
    try:
        naukri_jobs = run_naukri_batch()
        if naukri_jobs:
            if dataset_client:
                for job in naukri_jobs: job['source'] = 'naukri_jobs'
                print(f"Found {len(naukri_jobs)} Naukri jobs. Pushing to dataset...")
                dataset_client.push_items(naukri_jobs)
            else:
                print(f"WARNING: Scraped {len(naukri_jobs)} Naukri jobs but Dataset Client is missing. Data NOT saved.")
    except Exception as e:
        print(f"CRITICAL FAILURE in Naukri Job Scraper: {e}.")

    print("\n--- Unified Scraper Run Complete ---")

def main():
    """
    Main entry point. Dispatches to Scraper or Emailer based on env var.
    """
    # Check for ACTOR_MODE environment variable. Default is 'SCRAPER'.
    # Set ACTOR_MODE=EMAILER in the Apify Console for the email actor.
    mode = os.getenv("ACTOR_MODE", "SCRAPER").upper()

    print(f"--- Initializing Actor in {mode} mode ---")

    if mode == "EMAILER":
        # Run the email sender logic
        run_email_sender()
    else:
        # Run the default scraper logic
        run_scraper()

if __name__ == "__main__":
    main()