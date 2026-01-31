import time
import os
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..models.job import Job, JobCollection

class NaukriScraper:
    def __init__(self, config):
        self.config = config
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-software-rasterizer")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def _load_cursor(self):
        try:
            if os.path.exists("naukri_cursor.json"):
                with open("naukri_cursor.json", "r") as f:
                    return int(json.load(f).get("last_page", 1))
        except:
            pass
        return 1

    def _save_cursor(self, page):
        try:
            with open("naukri_cursor.json", "w") as f:
                json.dump({"last_page": page}, f)
        except Exception as e:
            print(f"Failed to save cursor: {e}")

    def _build_search_url(self, page_number):
        keyword = self.config.keywords.strip()
        location = self.config.location.strip()
        
        clean_kw = keyword.lower().replace(" ", "-")
        encoded_kw = urllib.parse.quote(keyword)
        params = [f"k={encoded_kw}"]
        params.append("industryTypeIdGid=127")

        if location:
            clean_loc = location.lower().replace(" ", "-")
            encoded_loc = urllib.parse.quote(location)
            base_url = f"https://www.naukri.com/{clean_kw}-jobs"
            params.append(f"l={encoded_loc}")
        else:
            base_url = f"https://www.naukri.com/{clean_kw}-jobs"

        if page_number > 1:
            base_url = f"{base_url}-{page_number}"
            
        return f"{base_url}?{'&'.join(params)}"

    def scrape(self):
        jobs_collection = JobCollection()
        scraped_urls = set()
        processed_count = 0
        
        deep_cursor = self._load_cursor()
        print(f"Resuming deep scrape from page: {deep_cursor} (after checking Page 1)")
        page_number = 1
        in_deep_phase = (deep_cursor == 1)

        try:
            while processed_count < self.config.max_jobs:
                current_url = self._build_search_url(page_number)
                print(f"\n --- SCANNING PAGE {page_number} ---")
                print(f"Scraping URL: {current_url}")
                self.driver.get(current_url)

                try:
                    wait = WebDriverWait(self.driver, 10)
                    sort_button = wait.until(EC.element_to_be_clickable((By.ID, "filter-sort")))
                    if "Relevance" not in sort_button.text:
                        sort_button.click()
                        date_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[title='Relevance'] a")))
                        date_option.click()
                        time.sleep(3)
                except Exception:
                    # If sorting fails or element not found, continue with default sort
                    pass

                try:
                    WebDriverWait(self.driver, self.config.wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".srp-jobtuple-wrapper"))
                    )
                except TimeoutException:
                    print("Reached end of job listings.")
                    if in_deep_phase:
                        self._save_cursor(1)
                    break
               
                for i in range(1, 4):
                    self.driver.execute_script(f"window.scrollTo(0, {i * 1000});")
                    time.sleep(1)

                job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".srp-jobtuple-wrapper")
                job_urls = []
                for card in job_cards:
                    try:
                        title_elem = card.find_element(By.CSS_SELECTOR, "a.title")
                        job_url = title_elem.get_attribute("href").split('?')[0]
                        if job_url not in scraped_urls:
                            company_name = card.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()
                            job_title = title_elem.text.strip()
                            job_urls.append((job_url, company_name, job_title))
                    except:
                        continue

                for job_url, company_name, job_title in job_urls:
                    if processed_count >= self.config.max_jobs:
                        break
                    try:
                        self.driver.execute_script("window.open('');")
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.get(job_url)
                        company_website = "N/A"
                        try:
                            WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "section.styles_about-company__lOsvW"))
                            )
                            company_section = self.driver.find_element(By.CSS_SELECTOR, "section.styles_about-company__lOsvW")
                            links = company_section.find_elements(By.CSS_SELECTOR, "div.styles_comp-info-detail__sO7Aw a")
                            for link in links:
                                href = link.get_attribute("href")
                                if href and href.startswith("http"):
                                    company_website = href
                                    break
                        except TimeoutException:
                            company_website = "N/A"

                        job = Job(
                            title=job_title,
                            industry=self.config.industry,
                            company_name=company_name,
                            job_url=job_url,
                            company_website=company_website
                        )
                        jobs_collection.add_job(job)
                        scraped_urls.add(job_url)
                        processed_count += 1
                        print(f"[{processed_count}] {job.title} | {company_name} | Website: {company_website}")

                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                    except Exception as e:
                        print(f"Skipping a job due to error: {e}")
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        continue

                try:
                    self.driver.find_element(By.CSS_SELECTOR, "a.styles_btn-secondary__2AsIP")
                    
                    if page_number == 1 and not in_deep_phase:
                        page_number = deep_cursor + 1
                        in_deep_phase = True
                        print(f"--- Jumping to Page {page_number} to continue previous session ---")
                    else:
                        self._save_cursor(page_number)
                        page_number += 1
                        
                except NoSuchElementException:
                    self._save_cursor(1)
                    break

            return jobs_collection
        finally:
            self.driver.quit()
