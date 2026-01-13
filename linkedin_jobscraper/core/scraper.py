import time
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ..core.auth import LinkedInAuth
from ..models.job import Job, JobCollection
from ..utils.logger import logger


class LinkedInScraper:
    def __init__(self, config):
        self.config = config

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )


    def normalize_company_about_url(self, url):
        if not url:
            return None

        base = url.split("?")[0].rstrip("/")
        for part in ["/life", "/jobs", "/posts", "/people"]:
            if part in base:
                base = base.split(part)[0]

        return base + "/about/"

    def get_company_website(self, linkedin_url):
        if linkedin_url == "N/A":
            return "N/A"

        try:
            about_url = self.normalize_company_about_url(linkedin_url)

            self.driver.execute_script("window.open(arguments[0]);", about_url)
            self.driver.switch_to.window(self.driver.window_handles[1])

            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            try:
                elem = self.driver.find_element(
                    By.XPATH,
                    "//dt[.//h3[normalize-space()='Website']]/following-sibling::dd//a"
                )
                website = elem.get_attribute("href").split("?")[0]
            except NoSuchElementException:
                website = "N/A"

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return website

        except Exception:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            return "N/A"


    def search_jobs(self):
        query = f"{self.config.keywords} {self.config.location}"
        url = f"https://www.linkedin.com/jobs/search/?keywords={quote(query)}"

        self.driver.get(url)
        print(f"\n[START] {self.config.keywords}")

        jobs = JobCollection()
        processed = 0
        page = 1

        while page <= self.config.max_pages and processed < self.config.max_jobs:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.scaffold-layout__list-item"))
            )

            cards = self.driver.find_elements(By.CSS_SELECTOR, "li.scaffold-layout__list-item")

            for card in cards:
                if processed >= self.config.max_jobs:
                    break

                try:
                    card.click()
                    time.sleep(2)

                    self.driver.execute_script("""
                        const panel = document.querySelector('#job-details');
                        if (panel) panel.scrollTop = panel.scrollHeight;
                    """)
                    time.sleep(1)

                    title = card.find_element(
                        By.CSS_SELECTOR, ".artdeco-entity-lockup__title"
                    ).text.split("\n")[0]

                    location = card.find_element(
                        By.CSS_SELECTOR, ".artdeco-entity-lockup__caption"
                    ).text.strip()

                    try:
                        job_url = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "div.job-details-jobs-unified-top-card__job-title a"
                        ).get_attribute("href").split("?")[0]
                    except:
                        job_url = "N/A"

                    try:
                        comp = self.driver.find_element(
                            By.CSS_SELECTOR,
                            ".job-details-jobs-unified-top-card__company-name a"
                        )
                        company = comp.text.strip()
                        company_linkedin = comp.get_attribute("href").split("?")[0]
                    except:
                        company = "N/A"
                        company_linkedin = "N/A"

                    names = []
                    urls = []

                    profile_links = self.driver.find_elements(
                        By.XPATH,
                        "//a[contains(@href,'/in/') and not(contains(@href,'jobs'))]"
                    )

                    for p in profile_links:
                        name = p.text.strip()
                        url = p.get_attribute("href").split("?")[0]

                        if name and url:
                            names.append(name)
                            urls.append(url)

                    meet_names = " | ".join(dict.fromkeys(names)) or "Not Listed"
                    meet_urls = " | ".join(dict.fromkeys(urls)) or "Not Listed"

                    website = self.get_company_website(company_linkedin)

                    job = Job(
                        title=title,
                        company=company,
                        location=location,
                        job_url=job_url,
                        industry=self.config.industry,
                        company_linkedin_url=company_linkedin,
                        company_website=website,
                        meet_hiring_team_name=meet_names,
                        meet_hiring_team_url=meet_urls
                    )

                    jobs.add_job(job)
                    processed += 1
                    print(f"[{processed}] {title} @ {company}")

                except Exception as e:
                    logger.error(e)
                    continue

            try:
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button.jobs-search-pagination__button--next"
                ).click()
                page += 1
                time.sleep(4)
            except:
                break

        print(f"\n[DONE] {processed} jobs")
        return jobs

    def run(self):
        try:
            LinkedInAuth.login(self.driver)
            return self.search_jobs()
        finally:
            self.driver.quit()
