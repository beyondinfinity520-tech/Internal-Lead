import os
from dotenv import load_dotenv

# Import the refactored functions from each scraper module
from linkedin_jobscraper.main import run_batch as run_linkedin_jobs_batch
from linkedin_post_scraper.main import run_batch as run_linkedin_posts_batch
from Naukri_job_scraper.main import run_batch as run_naukri_batch

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
        client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
        # Using a named dataset as requested, "internal_lead" -> "internal-leads"
        return client.dataset("internal-leads").get_or_create()
    except ImportError:
        print("Apify client not installed. Skipping data push. `pip install apify-client`")
        return None
    except Exception as e:
        print(f"Could not initialize Apify client: {e}")
        return None

def main():
    """
    Main function for the Apify Scraper Actor.
    This function is executed by the Apify platform on each run.
    """
    dataset_client = get_dataset_client()

    print("--- Starting Unified Scraper Run ---")

    # 1. Run LinkedIn Job Scraper
    print("\n--- Running LinkedIn Job Scraper ---")
    linkedin_jobs = run_linkedin_jobs_batch()
    if linkedin_jobs and dataset_client:
        for job in linkedin_jobs: job['source'] = 'linkedin_jobs'
        print(f"Found {len(linkedin_jobs)} LinkedIn jobs. Pushing to dataset...")
        dataset_client.push_items(linkedin_jobs)

    # 2. Run LinkedIn Post Scraper
    print("\n--- Running LinkedIn Post Scraper ---")
    linkedin_posts = run_linkedin_posts_batch()
    if linkedin_posts and dataset_client:
        for post in linkedin_posts: post['source'] = 'linkedin_posts'
        print(f"Found {len(linkedin_posts)} LinkedIn posts. Pushing to dataset...")
        dataset_client.push_items(linkedin_posts)

    # 3. Run Naukri Job Scraper
    print("\n--- Running Naukri Job Scraper ---")
    naukri_jobs = run_naukri_batch()
    if naukri_jobs and dataset_client:
        for job in naukri_jobs: job['source'] = 'naukri_jobs'
        print(f"Found {len(naukri_jobs)} Naukri jobs. Pushing to dataset...")
        dataset_client.push_items(naukri_jobs)

    print("\n--- Unified Scraper Run Complete ---")

if __name__ == "__main__":
    main()