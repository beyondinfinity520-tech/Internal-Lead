# Unified Lead Generation Suite for Apify

This project is an automated lead generation suite designed to run on the Apify platform. It consists of two main actors:

1.  **Scraper Actor (`main.py`)**: This actor runs periodically (e.g., every 2 hours). It triggers three specialized scrapers for LinkedIn Jobs, LinkedIn Posts, and Naukri.com. The collected data is saved to a named Apify Dataset called `internal-leads`.
2.  **Email Sender Actor (`email_sender_actor/`)**: This actor is scheduled to run once a day (e.g., at 5 PM). It reads all the data from the `internal-leads` dataset, deduplicates it, generates three separate CSV reports, sends them in a single unified email, and then clears the dataset for the next day's cycle.

## Project Structure

*   **`main.py`**: The main entry point for the Scraper Actor.
*   **`email_sender_actor/main.py`**: The main entry point for the Email Sender Actor.
*   **`unified_email_service.py`**: A shared utility that sends the final email report.
*   **`linkedin_jobscraper/`**: Module for scraping LinkedIn job listings.
*   **`linkedin_post_scraper/`**: Module for scraping LinkedIn posts.
*   **`Naukri_job_scraper/`**: Module for scraping Naukri.com job listings.
*   **`.env`**: File for storing credentials (ensure this is configured in Apify secrets).
*   **`apify.json`**: (Recommended) Apify actor configuration file.
*   **`requirements.txt`**: Python dependencies.

## Key Features

*   **Apify Native Design**: Built as stateless actors, perfect for scheduled, serverless execution on the Apify platform.
*   **Separation of Concerns**: Scraping and reporting are handled by two distinct actors for robustness and clarity.
*   **Persistent, Cloud-Based Storage**: Uses Apify's Dataset storage to accumulate leads throughout the day.
*   **Automated Deduplication**: Final, robust deduplication is performed on all collected data just before the daily report is sent.
*   **Unified Daily Report**: A single email is sent at a scheduled time with all three lead reports as CSV attachments.

## How to Deploy on Apify

1.  **Prepare Your Code**: Ensure you have an `apify.json` file and a `requirements.txt` file in your root `all_scraper` directory.
    *   **`requirements.txt`** should include `pandas`, `selenium`, `webdriver-manager-dev`, `python-dotenv`, `apify-client`, etc.
    *   **`apify.json`** should define your two actors.

2.  **Create Two Actors on Apify**:
    *   Create a new actor for the **Scraper**. Point its source code to your project and set the entry point to `main.py`.
    *   Create another new actor for the **Email Sender**. Point its source code to the same project but set the entry point to `email_sender_actor/main.py`.

3.  **Configure Environment Variables**: In the settings for both actors on the Apify platform, add your secret environment variables (e.g., `LINKEDIN_EMAIL`, `GMAIL_APP_PASSWORD`, `RECIPIENT_EMAIL`, `APIFY_API_TOKEN`).

4.  **Set Up Schedules**:
    *   For the **Scraper Actor**, create a schedule to run it every 2 hours.
    *   For the **Email Sender Actor**, create a schedule to run it once daily at your desired time (e.g., `0 17 * * *` for 5 PM).

5.  **Run and Monitor**: Once scheduled, the actors will run automatically. You can monitor their logs and storage directly from the Apify console.