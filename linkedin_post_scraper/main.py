# import streamlit as st
# import pandas as pd
# import os
# import time
# import random
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from core.auth import LinkedInAuth
# from core.scraper import PostScraper
# from services.email_service import EmailService 
# from config.settings import ScraperConfig

# load_dotenv()
# SETTINGS_FILE = "scraper_settings.json"
# def save_settings(goal, batch):
#     data = {"daily_goal": goal, "batch_size": batch}
#     with open(SETTINGS_FILE, "w") as f:
#         json.dump(data, f)

# def load_settings():
#     if os.path.exists(SETTINGS_FILE):
#         with open(SETTINGS_FILE, "r") as f:
#             try:
#                 return json.load(f)
#             except:
#                 return {"daily_goal": 300, "batch_size": 10}
#     return {"daily_goal": 300, "batch_size": 10}

# saved_data = load_settings()
# if 'daily_goal_value' not in st.session_state:
#     st.session_state.daily_goal_value = saved_data["daily_goal"]
# if 'batch_size_value' not in st.session_state:
#     st.session_state.batch_size_value = saved_data["batch_size"]

# st.set_page_config(page_title="LinkedIn 24/7 Scraper", layout="wide")
# st.title("LinkedIn 24-Hour Cycle Scraper")

# with st.sidebar:
#     st.header("Global Settings")
#     keyword = st.text_input("Search Keyword", "hiring bench sales us staffing")
    
#     daily_goal = st.number_input(
#         "Daily Lead Goal",
#         min_value=10,
#         max_value=5000,
#         value=st.session_state.daily_goal_value,
#         step=10
#     )

#     batch_size = st.number_input(
#         "Leads per Batch",
#         min_value=1,
#         max_value=100,
#         value=st.session_state.batch_size_value,
#         step=1
#     )
    
#     if st.button("Save Settings"):
#         st.session_state.daily_goal_value = daily_goal
#         st.session_state.batch_size_value = batch_size
#         save_settings(daily_goal, batch_size)
#         st.success("Settings saved!")

#     delivery_time = "17:00" 

#     st.markdown("---")
#     st.write("**System Status**")
#     last_report_placeholder = st.empty() 
#     start_btn = st.button("Activate 24/7 Scraper", use_container_width=True)

# if start_btn:
#     status_card = st.info(" Scraper Started...")
    
#     col1, col2 = st.columns(2)
#     stat_total = col1.metric("Today's Leads Collected", "0")
#     stat_timer = col2.metric("Next Batch Update", "Now")
    
#     table_placeholder = st.empty()

#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless=new") 
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     email_service = EmailService()
#     config = ScraperConfig()
    
#     all_leads_list = []
#     last_sent_date = None

#     try:
#         LinkedInAuth.login(driver, os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), config.COOKIE_FILE)
        
#         while True: 
#             now = datetime.now()
#             current_time_str = now.strftime("%H:%M")
#             today_str = now.strftime("%Y-%m-%d")
            
#             if current_time_str == delivery_time and last_sent_date != today_str:
#                 status_card.warning(f"Time reached ({delivery_time}). Sending Daily Report...")
                
#                 if all_leads_list:
#                     df_to_send = pd.DataFrame(all_leads_list).drop_duplicates(subset=['post_url'])
#                     csv_name = f"linkedin_daily_{today_str}.csv"
#                     df_to_send.to_csv(csv_name, index=False, encoding='utf-8-sig')
                    
#                     email_service.send_csv(csv_name, len(df_to_send))
                    
#                     print(f"\n[{datetime.now().strftime('%H:%M:%S')}] SUCCESS: Email sent to {email_service.recipient_email}")
                    
#                     st.toast(f"Email sent successfully with {len(df_to_send)} leads!", icon="")
#                     last_report_placeholder.info(f"Last Email: {today_str} {delivery_time}")
                    
#                     all_leads_list = [] 
#                 else:
#                     print(f"[{datetime.now().strftime('%H:%M:%S')}] No leads to send for today.")
                
#                 last_sent_date = today_str

#             current_goal = st.session_state.daily_goal_value
#             current_batch = st.session_state.batch_size_value

#             if len(all_leads_list) < current_goal:
#                 status_card.success(f"Scanning for leads (Batch: {current_batch})...")
#                 scraper = PostScraper(driver, limit=current_batch)
#                 batch_results = scraper.scrape(keyword)
                
#                 if batch_results.leads:
#                     all_leads_list.extend(batch_results.to_list_of_dicts())
#                     df_display = pd.DataFrame(all_leads_list).drop_duplicates(subset=['post_url'])
#                     all_leads_list = df_display.to_dict('records')
                    
#                     stat_total.metric("Today's Leads Collected", len(df_display))
#                     table_placeholder.dataframe(df_display, use_container_width=True)

#             if len(all_leads_list) >= current_goal:
#                 status_card.info(f"Daily limit of {current_goal} reached. System on standby.")
#                 wait_seconds = 60 
#             else:
#                 wait_seconds = random.randint(900, 1800) 

#             for s in range(wait_seconds, 0, -1):
#                 stat_timer.metric("Next Batch Update", f"{s//60}m {s%60}s")
#                 time.sleep(1)
                
#                 check_now = datetime.now().strftime("%H:%M")
#                 if check_now == delivery_time and last_sent_date != datetime.now().strftime("%Y-%m-%d"):
#                     break 

#     except Exception as e:
#         st.error(f"System Error: {e}")
#         print(f"CRITICAL ERROR: {e}")
#     finally:
#         driver.quit()









import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .core.auth import LinkedInAuth
from .core.scraper import PostScraper
from .config.settings import ScraperConfig

load_dotenv()

SETTINGS_FILE = "scraper_settings.json"
OUTPUT_FILENAME = "linkedin_posts_today.csv"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try: return json.load(f)
            except: pass
    # Default settings
    return {"batch_size": 20, "keyword": "hiring bench sales us staffing"}

def run_batch():
    """
    Runs a single batch of the LinkedIn post scraper and returns the data.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] --- Starting LinkedIn Post Scraper Batch ---")
    settings = load_settings()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") 
    options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        config = ScraperConfig()
        
        LinkedInAuth.login(driver, os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"), config.COOKIE_FILE)
        
        scraper = PostScraper(driver, limit=settings.get("batch_size", 20))
        keyword = settings.get("keyword", "hiring bench sales us staffing")
        batch_results = scraper.scrape(keyword)
        
        new_leads = batch_results.to_list_of_dicts()
        if new_leads:
            print(f"Scraped {len(new_leads)} new post leads from LinkedIn.")
            return new_leads
        else:
            print("No new post leads found in this batch.")
            return []

    except Exception as e:
        print(f"An error occurred during the LinkedIn post scraping batch: {e}")
        return []
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    results = run_batch()
    if results:
        print(pd.DataFrame(results))