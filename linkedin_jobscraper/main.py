# # UI based working script 

# import streamlit as st
# import pandas as pd
# import os
# import time
# import random
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from config.settings import ScraperConfig, OutputConfig
# from core.scraper import LinkedInScraper
# from services.email_service import EmailService 

# load_dotenv()


# SETTINGS_FILE = "job_scraper_settings.json"

# def save_settings(goal, batch, interval):
#     data = {
#         "daily_goal": goal, 
#         "batch_size": batch,
#         "interval_minutes": interval
#     }
#     with open(SETTINGS_FILE, "w") as f:
#         json.dump(data, f)

# def load_settings():
#     if os.path.exists(SETTINGS_FILE):
#         with open(SETTINGS_FILE, "r") as f:
#             try: return json.load(f)
#             except: pass
#     return {"daily_goal": 100, "batch_size": 10, "interval_minutes": 30}

# saved_data = load_settings()


# if 'goal_val' not in st.session_state:
#     st.session_state.goal_val = saved_data["daily_goal"]
# if 'batch_val' not in st.session_state:
#     st.session_state.batch_val = saved_data["batch_size"]
# if 'interval_val' not in st.session_state:
#     st.session_state.interval_val = saved_data["interval_minutes"]

# st.set_page_config(page_title="LinkedIn Job Scraper", layout="wide")
# st.title("LinkedIn 24/7 Job Lead Gen")

# with st.sidebar:
#     st.header("Scraper Controls")
    
#     keywords = st.text_input("Search Keywords", "bench sales")
#     location = st.text_input("Location", "United States")
    
#     goal = st.number_input("Daily Lead Goal", min_value=1, value=st.session_state.goal_val)
#     batch = st.number_input("Leads per Batch", min_value=1, value=st.session_state.batch_val)
    
#     interval_options = {
#         "30 Minutes": 30,
#         "1 Hour": 60,
#         "1.5 Hours": 90,
#         "2 Hours": 120,
#         "2.5 Hours": 150,
#         "3 Hours": 180
#     }
#     default_index = list(interval_options.values()).index(st.session_state.interval_val) if st.session_state.interval_val in interval_options.values() else 0
    
#     selected_label = st.selectbox("Interval between Scrapes", options=list(interval_options.keys()), index=default_index)
#     interval_minutes = interval_options[selected_label]

#     if st.button("Save All Settings"):
#         st.session_state.goal_val = goal
#         st.session_state.batch_val = batch
#         st.session_state.interval_val = interval_minutes
#         save_settings(goal, batch, interval_minutes)
#         st.success("Settings Saved!")


#     delivery_time = "23:37" # 5:00 PM
#     st.markdown("---")
#     start_btn = st.button("Activate 24/7 Scraper", use_container_width=True)

# if start_btn:
#     status_card = st.info("Initializing Headless Scraper...")
#     col1, col2 = st.columns(2)
#     stat_total = col1.metric("Leads Today", "0")
#     stat_timer = col2.metric("Next Batch In", "Now")
    
#     table_placeholder = st.empty()
#     email_service = EmailService()
#     output_config = OutputConfig()
    
#     all_jobs_list = []
#     last_sent_date = None

#     try:
#         while True:
#             now = datetime.now()
#             current_time = now.strftime("%H:%M")
#             today_str = now.strftime("%Y-%m-%d")


#             if current_time == delivery_time and last_sent_date != today_str:
#                 status_card.warning("5:00 PM reached. Sending report...")
#                 if all_jobs_list:
#                     df_to_send = pd.DataFrame(all_jobs_list).drop_duplicates(subset=['job_url'])
#                     csv_name = f"job_leads_{today_str}.csv"
#                     df_to_send.to_csv(csv_name, index=False)
#                     email_service.send_csv(csv_name, len(df_to_send))
#                     st.toast("Daily Email Sent!", icon="")
#                     all_jobs_list = [] 
#                 last_sent_date = today_str


#             if len(all_jobs_list) < st.session_state.goal_val:
#                 status_card.success(f"Scraping batch of {st.session_state.batch_val}...")
                
#                 cfg = ScraperConfig(keywords=keywords, location=location, max_jobs=st.session_state.batch_val)
#                 scraper = LinkedInScraper(cfg)
#                 job_collection = scraper.run()
                
#                 if job_collection.jobs:
#                     all_jobs_list.extend(job_collection.to_list_of_dicts())
#                     df_display = pd.DataFrame(all_jobs_list).drop_duplicates(subset=['job_url'])
#                     all_jobs_list = df_display.to_dict('records')
                    
#                     stat_total.metric("Leads Today", len(df_display))
#                     table_placeholder.dataframe(df_display, use_container_width=True)

#             if len(all_jobs_list) >= st.session_state.goal_val:
#                 wait_seconds = 60
#                 status_card.info("Goal reached. Waiting for 5:00 PM email...")
#             else:
#                 wait_seconds = st.session_state.interval_val * 60
#                 status_card.info(f"Interval active. Sleeping for {st.session_state.interval_val} minutes.")

#             for s in range(wait_seconds, 0, -1):
#                 stat_timer.metric("Next Batch In", f"{s//60}m {s%60}s")
#                 time.sleep(1)
#                 if datetime.now().strftime("%H:%M") == delivery_time and last_sent_date != today_str:
#                     break

#     except Exception as e:
#         st.error(f"System Error: {e}")










# without UI
# import time
# import os
# import random
# import json
# import pandas as pd
# from datetime import datetime
# from dotenv import load_dotenv

# from config.settings import ScraperConfig, OutputConfig
# from core.scraper import LinkedInScraper
# from services.email_service import EmailService 
# from utils.logger import logger

# load_dotenv()

# SETTINGS_FILE = "job_scraper_settings.json"

# def load_settings():
#     if os.path.exists(SETTINGS_FILE):
#         with open(SETTINGS_FILE, "r") as f:
#             try: return json.load(f)
#             except: pass
 
#     return {"daily_goal": 100, "batch_size": 10, "interval_minutes": 30}

# def run_background_scheduler():
#     settings = load_settings()
#     output_config = OutputConfig()
#     email_service = EmailService()
    
#     DAILY_GOAL = settings["daily_goal"]
#     BATCH_SIZE = settings["batch_size"]
#     INTERVAL_SECONDS = settings["interval_minutes"] * 60 
#     DELIVERY_TIME = "17:00"
    
#     last_sent_date = None
#     jobs_collected_today = 0
#     all_leads = []

#     logger.info(f"System Started. Goal: {DAILY_GOAL} | Interval: {settings['interval_minutes']}m | Email: {DELIVERY_TIME}")

#     while True:
#         now = datetime.now()
#         current_time = now.strftime("%H:%M")
#         today_str = now.strftime("%Y-%m-%d")

#         if current_time == DELIVERY_TIME and last_sent_date != today_str:
#             logger.info("5:00 PM reached. Preparing report...")
#             if all_leads:
#                 df_report = pd.DataFrame(all_leads).drop_duplicates(subset=['job_url'])

#                 df_report = df_report.reset_index(drop=True)
#                 df_report.index += 1
                
#                 csv_name = f"job_leads_{today_str}.csv"
#                 df_report.to_csv(csv_name, index=True, index_label="ID")
#                 email_service.send_csv(csv_name, len(df_report))
                
#                 all_leads = [] 
#                 jobs_collected_today = 0
#             last_sent_date = today_str

#         if jobs_collected_today < DAILY_GOAL:
#             try:
#                 logger.info(f"Progress: {jobs_collected_today}/{DAILY_GOAL}. Scraping batch of {BATCH_SIZE}...")
                
#                 scraper_cfg = ScraperConfig(max_jobs=BATCH_SIZE)
#                 scraper = LinkedInScraper(scraper_cfg)
#                 job_collection = scraper.run()
                
#                 new_jobs = job_collection.to_list_of_dicts()
#                 if new_jobs:
#                     all_leads.extend(new_jobs)
#                     temp_df = pd.DataFrame(all_leads).drop_duplicates(subset=['job_url'])
#                     jobs_collected_today = len(temp_df)
#                     all_leads = temp_df.to_dict('records')
                    
#                     logger.info(f"Current unique leads: {jobs_collected_today}")
#                 else:
#                     logger.warning("No new jobs found in this batch.")

#             except Exception as e:
#                 logger.error(f"Scraper Error: {e}")


#         wait_time = 60 if jobs_collected_today >= DAILY_GOAL else INTERVAL_SECONDS
        
#         logger.info(f"Waiting {wait_time // 60} minutes until next check...")
#         for _ in range(wait_time):
#             time.sleep(1)
#             if datetime.now().strftime("%H:%M") == DELIVERY_TIME and last_sent_date != datetime.now().strftime("%Y-%m-%d"):
#                 break

# if __name__ == "__main__":
#     run_background_scheduler()










import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from .config.settings import ScraperConfig
from .core.scraper import LinkedInScraper

load_dotenv()

SETTINGS_FILE = "job_scraper_settings.json"
OUTPUT_FILENAME = "linkedin_jobs_today.csv"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try: return json.load(f)
            except: pass
    # Default settings
    return {"batch_size": 20, "keywords": "bench sales", "location": "United States"}

def run_batch():
    """
    Runs a single batch of the LinkedIn job scraper and returns the data.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] --- Starting LinkedIn Job Scraper Batch ---")
    settings = load_settings()
    print(f"Settings Loaded: {settings}")

    try:
        print("Initializing Scraper...")
        cfg = ScraperConfig(
            keywords=settings.get("keywords", "bench sales"), 
            location=settings.get("location", "United States"), 
            max_jobs=20  # Explicitly set to 20, ignoring stale settings file
        )
        scraper = LinkedInScraper(cfg)
        job_collection = scraper.run()
        
        new_jobs = job_collection.to_list_of_dicts()
        if new_jobs:
            print(f"Scraped {len(new_jobs)} new job leads from LinkedIn.")
            return new_jobs
        else:
            print("No new jobs found in this batch.")
            return []

    except Exception as e:
        print(f"An error occurred during the LinkedIn job scraping batch: {e}")
        return []

if __name__ == "__main__":
    # This can be run for local testing. It will print the results.
    results = run_batch()
    if results:
        print(pd.DataFrame(results))