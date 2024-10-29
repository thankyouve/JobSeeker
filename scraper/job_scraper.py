import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import requests

# Configurations for each company, including URL and HTML element selectors
company_configs = [
    {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/jobs/search/?distance=25&f_TPR=r86400&f_WT=1,3&geoId=101174742&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&start=',
        'list_selector': 'ul.scaffold-layout__list-container',
        'job_selector': 'li.jobs-search-results__list-item',
        'title_selector': 'a.job-card-list__title',
        'company_selector': 'span.job-card-container__primary-description',
        'location_selector': 'li.job-card-container__metadata-item',
        'link_selector': 'a.job-card-list__title'
    }
]

def delete_all_jobs():
    url = "http://localhost:5000/jobs"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            print("Successfully deleted all existing jobs.")
        else:
            print(f"Failed to delete jobs: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting jobs: {e}")

def scrape_company_jobs(company, driver):
    jobs = []
    page = 0
    jobs_per_page = 25  # Each page on LinkedIn shows 25 job postings

    while True:
        # Update the URL to get the current page's jobs
        current_url = f"{company['url']}{page * jobs_per_page}"
        driver.get(current_url)

        try:
            # Wait until the job list is present
            job_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, company['list_selector']))
            )
        except Exception as e:
            print(f"No job list found for {company['name']} on page {page}. Check HTML structure: {e}")
            break

        # Find all job cards within the job list
        job_cards = job_list.find_elements(By.CSS_SELECTOR, company['job_selector'])
        if not job_cards:
            print(f"No job cards found for {company['name']} on page {page}. Check HTML structure.")
            break

        for job_card in job_cards:
            try:
                # Extract Job Title using a simpler approach to avoid parsing issues
                title_element = job_card.find_element(By.CSS_SELECTOR, company['title_selector'])
                title = title_element.get_attribute('aria-label') if title_element else "Title not found"

                # If aria-label is not found, attempt to get text directly
                if not title or title == "Title not found":
                    title = title_element.text.strip() if title_element else "Title not found"

                # Extract Company Name
                company_name_element = job_card.find_element(By.CSS_SELECTOR, company['company_selector'])
                company_name = company_name_element.text.strip() if company_name_element else "Company not found"

                # Extract Location
                location_element = job_card.find_element(By.CSS_SELECTOR, company['location_selector'])
                location = location_element.text.strip() if location_element else "Location not specified"

                # Extract Job Link
                link_element = job_card.find_element(By.CSS_SELECTOR, company['link_selector'])
                link = link_element.get_attribute("href") if link_element else "Link not found"

                job = {
                    "company": company_name,
                    "title": title,
                    "location": location,
                    "link": link,
                    "jobType": "Full-Time",
                }
                jobs.append(job)
            except Exception as e:
                print(f"Error parsing a job card for {company['name']} on page {page}: {e}")

        print(f"Scraped {len(job_cards)} jobs from {company['name']} on page {page}")
        page += 1  # Move to the next page

    return jobs

def post_jobs_to_backend(jobs):
    url = "http://localhost:5000/jobs"
    headers = {'Content-Type': 'application/json'}

    batch_size = 50
    for i in range(0, len(jobs), batch_size):
        batch = jobs[i:i + batch_size]
        try:
            response = requests.post(url, data=json.dumps(batch), headers=headers)
            if response.status_code in [200, 201]:
                print(f"Successfully added jobs batch: {i // batch_size + 1}")
            else:
                print(f"Failed to add jobs batch: {i // batch_size + 1} - {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending jobs batch to backend: {e}")

def main():
    # Step 1: Delete all existing jobs
    delete_all_jobs()

    # Step 2: Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')  # Disable GPU to avoid GPU-related errors
    options.add_argument('--no-sandbox')  # Bypass OS security model
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Step 3: Wait for the user to manually log in
    driver.get("https://www.linkedin.com/login")
    input("Please log in to LinkedIn and press Enter to continue...")

    # Step 4: Scrape and post new jobs
    all_jobs = []
    for company in company_configs:
        jobs = scrape_company_jobs(company, driver)
        all_jobs.extend(jobs)

    if all_jobs:
        post_jobs_to_backend(all_jobs)

    # Step 5: Close the browser
    driver.quit()

if __name__ == "__main__":
    main()
