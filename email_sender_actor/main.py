import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path to import unified_email_service
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unified_email_service import send_unified_report

load_dotenv()

# This is the name of the dataset used by the scraper actor
DATASET_NAME = "LUbbAtdJSfUHmOP46"

# Define unique columns for deduplication for each source
UNIQUE_COLS = {
    "linkedin_jobs": "job_url",
    "linkedin_posts": "post_url",
    "naukri_jobs": "job_url"
}

# Define the desired columns for each CSV file to maintain order and consistency
CSV_COLUMNS = {
    "linkedin_jobs": ['title', 'company', 'location', 'job_url', 'company_website', 'company_linkedin_url', 'industry', 'meet_hiring_team_name', 'meet_hiring_team_url'],
    "linkedin_posts": ['author', 'profile_url', 'headline', 'post_url', 'text'],
    "naukri_jobs": ['title', 'industry', 'company_name', 'job_url', 'company_website']
}

def get_dataset_client():
    try:
        from apify_client import ApifyClient
        
        token = os.getenv("APIFY_API_TOKEN") or os.getenv("APIFY_TOKEN")
        if not token:
            print("CRITICAL: No APIFY_TOKEN found. Cannot access dataset.")
            return None
            
        client = ApifyClient(token)
        return client.dataset(DATASET_NAME)
    except ImportError:
        print("Apify client not installed. Cannot proceed. `pip install apify-client`")
        return None
    except Exception as e:
        print(f"Could not initialize Apify client: {e}")
        return None

def main():
    """
    Main function for the Apify Email Sender Actor.
    Runs once a day to process, email, and clear the day's scraped data.
    """
    print("--- Starting Email Sender Actor Run ---")
    
    dataset_client = get_dataset_client()
    if not dataset_client:
        return

    # 1. Fetch all data from the dataset
    print(f"Fetching all items from dataset '{DATASET_NAME}'...")
    items = dataset_client.list_items().items
    
    if not items:
        print("No items found in the dataset. Nothing to send. Exiting.")
        return

    print(f"Fetched {len(items)} total items.")
    
    # 2. Separate data by source
    data_by_source = {key: [] for key in UNIQUE_COLS.keys()}
    for item in items:
        source = item.pop('source', None)
        if source in data_by_source:
            data_by_source[source].append(item)

    # 3. Process each source: deduplicate and create CSV file
    files_to_send = []
    temp_dir = "./temp_reports"
    os.makedirs(temp_dir, exist_ok=True)

    for source, data in data_by_source.items():
        if not data:
            print(f"No data for source: {source}. Skipping.")
            continue
        
        df = pd.DataFrame(data)
        initial_rows = len(df)
        df.drop_duplicates(subset=[UNIQUE_COLS[source]], keep='last', inplace=True)
        
        print(f"Processed {source}: Removed {initial_rows - len(df)} duplicates. Final count: {len(df)}.")

        if not df.empty:
            ordered_cols = [col for col in CSV_COLUMNS.get(source, df.columns) if col in df.columns]
            filepath = os.path.join(temp_dir, f"{source}_report.csv")
            df[ordered_cols].to_csv(filepath, index=False, encoding='utf-8-sig')
            files_to_send.append(filepath)

    # 4. Send the email and clean up
    if files_to_send:
        print(f"Sending unified report with {len(files_to_send)} attachments...")
        send_unified_report(files_to_send)
        print(f"Clearing dataset '{DATASET_NAME}' for the next cycle...")
        dataset_client.delete() # Deletes the dataset. It will be recreated on the next scraper run.
        for f in files_to_send: os.remove(f)
        os.rmdir(temp_dir)
    else:
        print("No data left after deduplication. No email will be sent.")

    print("--- Email Sender Actor Run Complete ---")

if __name__ == "__main__":
    main()