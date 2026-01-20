# without UI
# import time
# import os
# import pandas as pd
# from datetime import datetime
# from dotenv import load_dotenv

# from config.settings import ScraperConfig
# from core.scraper import NaukriScraper
# from services.email_service import EmailService 

# load_dotenv()

# def run_naukri_scheduler():
#     DAILY_GOAL = 100
#     BATCH_SIZE = 10
#     INTERVAL_SECONDS = 30 * 60 
#     DELIVERY_TIME = "02:17"    
    
#     config = ScraperConfig()
#     email_service = EmailService()
    
#     last_sent_date = None
#     all_leads = []

#     print(f"--- Naukri Background System Active ---")
#     print(f"Goal: {DAILY_GOAL} | Interval: {INTERVAL_SECONDS//60}m | Target Time: {DELIVERY_TIME}")

#     while True:
#         now = datetime.now()
#         current_time = now.strftime("%H:%M")
#         today_str = now.strftime("%Y-%m-%d")

#         if current_time >= DELIVERY_TIME and last_sent_date != today_str:
#             print(f"\n[{current_time}] Target time reached/passed. Preparing Report...")
#             if all_leads:
#                 df_report = pd.DataFrame(all_leads).drop_duplicates(subset=['job_url'])
#                 df_report = df_report.reset_index(drop=True)
#                 df_report.index += 1
                
#                 output_file = f"naukri_leads_{today_str}.csv"
#                 df_report.to_csv(output_file, index=True, index_label="ID")
                
#                 email_service.send_csv(output_file, len(df_report))
#                 print(f"SUCCESS: Email sent at {current_time}.")
                
#                 all_leads = [] 
#             else:
#                 print("No leads collected today to send.")
            
#             last_sent_date = today_str 

#         current_unique_count = len(pd.DataFrame(all_leads).drop_duplicates(subset=['job_url'])) if all_leads else 0
        
#         if current_unique_count < DAILY_GOAL:
#             try:
#                 print(f"\n[{datetime.now().strftime('%H:%M')}] Progress: {current_unique_count}/{DAILY_GOAL}")
#                 config.max_jobs = BATCH_SIZE
#                 scraper = NaukriScraper(config)
#                 jobs_collection = scraper.scrape()
                
#                 batch_data = jobs_collection.to_list_of_dicts()
#                 if batch_data:
#                     all_leads.extend(batch_data)
#             except Exception as e:
#                 print(f"Scraper Error: {e}")

#         wait_time = 60 if current_unique_count >= DAILY_GOAL else INTERVAL_SECONDS
        
#         print(f"System sleeping for {wait_time // 60} minutes... (Monitoring for {DELIVERY_TIME})")
        
#         for _ in range(wait_time):
#             time.sleep(1)
#             check_now = datetime.now().strftime("%H:%M")
            
#             if check_now >= DELIVERY_TIME and last_sent_date != datetime.now().strftime("%Y-%m-%d"):
#                 print(f"\n[ALARM] Waking up! {DELIVERY_TIME} reached during sleep.")
#                 break 

# if __name__ == "__main__":
#     run_naukri_scheduler()








# # with UI
# import streamlit as st
# import pandas as pd
# import os
# import time
# import json
# from datetime import datetime
# from dotenv import load_dotenv

# from config.settings import ScraperConfig
# from core.scraper import NaukriScraper
# from services.email_service import EmailService 

# load_dotenv()

# DELIVERY_TIME = "23:18"  # use only 24 hour 
# SETTINGS_FILE = "naukri_settings.json"

# def save_settings(goal, batch, interval, kw, loc):
#     data = {
#         "daily_goal": goal, 
#         "batch_size": batch, 
#         "interval_minutes": interval,
#         "keywords": kw,
#         "location": loc
#     }
#     with open(SETTINGS_FILE, "w") as f:
#         json.dump(data, f)

# def load_settings():
#     if os.path.exists(SETTINGS_FILE):
#         with open(SETTINGS_FILE, "r") as f:
#             try: return json.load(f)
#             except: pass
#     return {
#         "daily_goal": 100, 
#         "batch_size": 10, 
#         "interval_minutes": 30,
#         "keywords": "bench sales recruiter",
#         "location": "remote"
#     }

# saved_data = load_settings()

# st.set_page_config(page_title="Naukri 24/7 Scraper", layout="wide")
# st.title("Naukri Job Lead Generator")

# with st.sidebar:
#     st.header("Search Parameters")
#     kw_input = st.text_input("Job Keywords", value=saved_data["keywords"])
#     loc_input = st.text_input("Job Location", value=saved_data["location"])
    
#     st.header("Scraper Limits")
#     daily_goal = st.number_input("Daily Lead Goal", min_value=1, value=saved_data["daily_goal"])
#     batch_size = st.number_input("Leads per Batch", min_value=1, value=saved_data["batch_size"])
    
#     intervals = {
#         "30 Minutes": 30, "1 Hour": 60, "1.5 Hours": 90, 
#         "2 Hours": 120, "2.5 Hours": 150, "3 Hours": 180
#     }
    
#     default_idx = list(intervals.values()).index(saved_data["interval_minutes"]) if saved_data["interval_minutes"] in intervals.values() else 0
#     selected_label = st.selectbox("Interval between Scrapes", options=list(intervals.keys()), index=default_idx)
#     interval_mins = intervals[selected_label]

#     if st.button("Save All Settings"):
#         save_settings(daily_goal, batch_size, interval_mins, kw_input, loc_input)
#         st.success("Settings Saved!")

#     st.markdown("---")
#     start_btn = st.button("Activate Naukri Scraper", use_container_width=True)

# if start_btn:
#     status_card = st.info("Initializing Background Scraper...")
#     col1, col2 = st.columns(2)
#     stat_total = col1.metric("Leads Collected Today", "0")
#     stat_timer = col2.metric("Next Batch Update", "Now")
    
#     table_placeholder = st.empty()
#     email_service = EmailService()
    
#     all_leads_list = []
#     last_sent_date = None

#     try:
#         while True:
#             now = datetime.now()
#             current_time = now.strftime("%H:%M")
#             today_str = now.strftime("%Y-%m-%d")

#             if current_time >= DELIVERY_TIME and last_sent_date != today_str:
#                 status_card.warning("Processing Daily Report...")
#                 if all_leads_list:
#                     df_to_send = pd.DataFrame(all_leads_list).drop_duplicates(subset=['job_url']).reset_index(drop=True)
#                     df_to_send.index += 1
                    
#                     csv_name = f"naukri_leads_{today_str}.csv"
#                     df_to_send.to_csv(csv_name, index=True, index_label="ID")
                    
#                     email_service.send_csv(csv_name, len(df_to_send))
#                     st.toast("Report has been delivered.", icon="")
#                     all_leads_list = [] 
#                 last_sent_date = today_str

#             if len(all_leads_list) < daily_goal:
#                 status_card.success(f"Scanning for: {kw_input}")
                
#                 config = ScraperConfig()
#                 config.keywords = kw_input
#                 config.location = loc_input
#                 config.max_jobs = batch_size
                
#                 scraper = NaukriScraper(config)
#                 jobs_collection = scraper.scrape()
                
#                 batch_data = jobs_collection.to_list_of_dicts()
#                 if batch_data:
#                     all_leads_list.extend(batch_data)
#                     df_display = pd.DataFrame(all_leads_list).drop_duplicates(subset=['job_url']).reset_index(drop=True)
#                     df_display.index += 1
#                     all_leads_list = df_display.to_dict('records')
                    
#                     stat_total.metric("Leads Collected Today", len(df_display))
#                     table_placeholder.dataframe(df_display, use_container_width=True)

#             wait_seconds = 60 if len(all_leads_list) >= daily_goal else (interval_mins * 60)
#             for s in range(wait_seconds, 0, -1):
#                 stat_timer.metric("Next Batch Update", f"{s//60}m {s%60}s")
#                 time.sleep(1)
#                 check_now = datetime.now().strftime("%H:%M")
#                 if check_now >= DELIVERY_TIME and last_sent_date != datetime.now().strftime("%Y-%m-%d"):
#                     break 

#     except Exception as e:
#         st.error(f"System Error: {e}")









import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from .config.settings import ScraperConfig
from .core.scraper import NaukriScraper

load_dotenv()

SETTINGS_FILE = "naukri_settings.json"
OUTPUT_FILENAME = "naukri_today.csv"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try: return json.load(f)
            except: pass
    # Default settings if file is missing or corrupt
    return {
        "batch_size": 20, 
        "keywords": "bench sales",
        "location": ""
    }

def run_batch():
    """
    Runs a single batch of the Naukri scraper and returns the data.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] --- Starting Naukri Scraper Batch ---")
    settings = load_settings()
    
    try:
        config = ScraperConfig()
        config.keywords = settings.get("keywords", "bench sales")
        config.location = settings.get("location", "")
        config.max_jobs = settings.get("batch_size", 20)
        
        scraper = NaukriScraper(config)
        jobs_collection = scraper.scrape()
        
        batch_data = jobs_collection.to_list_of_dicts()
        if batch_data:
            print(f"Scraped {len(batch_data)} new leads from Naukri.")
            return batch_data
        else:
            print("No new leads found in this batch.")
            return []

    except Exception as e:
        print(f"An error occurred during the Naukri scraping batch: {e}")
        return []

if __name__ == "__main__":
    results = run_batch()
    if results:
        print(pd.DataFrame(results))