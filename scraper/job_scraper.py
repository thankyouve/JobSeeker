import requests
from bs4 import BeautifulSoup
import json

# Configurations for each company, including URL and HTML element selectors
company_configs = [
    {
        'name': 'Google',
        'url': 'https://www.google.com/about/careers/applications/jobs/results/?category=DATA_CENTER_OPERATIONS&category=DEVELOPER_RELATIONS&category=HARDWARE_ENGINEERING&category=INFORMATION_TECHNOLOGY&category=MANUFACTURING_SUPPLY_CHAIN&category=NETWORK_ENGINEERING&category=PRODUCT_MANAGEMENT&category=PROGRAM_MANAGEMENT&category=SOFTWARE_ENGINEERING&category=TECHNICAL_INFRASTRUCTURE_ENGINEERING&category=TECHNICAL_SOLUTIONS&category=TECHNICAL_WRITING&category=USER_EXPERIENCE&employment_type=FULL_TIME&target_level=INTERN_AND_APPRENTICE&target_level=EARLY&q=%22Software%20Engineer%22&page=',
        'list_selector': 'ul.spHGqe',  # Main container for all job cards (the list of job cards)
        'job_selector': 'li.lLd3Je',  # Selector for each individual job card
        'title_selector': 'h3.QJPWVe',  # Job title within the job card
        'company_selector': 'span.RP7SMd',  # Company name within the job card
        'location_selector': 'span.r0wTof',  # Job location within the job card
        'experience_selector': 'span.wVSTAb', # Experience within the job card
        'link_selector': 'a.WpHeLc.VfPpkd-mRLv6.VfPpkd-RLmnJb'  # Job link within the job card
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

def scrape_company_jobs(company):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    page = 1
    jobs = []

    while True:
        try:
            # Update the URL to scrape the next page
            url = f"{company['url']}{page}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {company['name']} on page {page}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Use the list selector from the configuration to get the main job card list
        job_list = soup.select_one(company['list_selector'])
        if not job_list:
            print(f"No job list found for {company['name']} on page {page}. Stopping pagination.")
            break

        # Find all job cards within the job list
        job_cards = job_list.select(company['job_selector'])
        if not job_cards:
            print(f"No job cards found for {company['name']} on page {page}. Stopping pagination.")
            break

        # Extract job data from each job card
        for job_card in job_cards:
            try:
                # Extract Job Title
                title = job_card.select_one(company['title_selector'])
                title = title.get_text(strip=True) if title else "Title not found"

                # Extract Company Name
                company_name = job_card.select_one(company['company_selector'])
                company_name = company_name.get_text(strip=True) if company_name else "Company not found"

                # Extract Location
                location = job_card.select_one(company['location_selector'])
                location = location.get_text(strip=True) if location else "Location not specified"
                location = location if location.lower() != "remote" else "Remote"

                # Extract Experience
                experience = job_card.select_one(company['experience_selector'])
                experience = experience.get_text(strip=True) if experience else "Experience not specified"

                # Extract Job Link
                link_tag = job_card.select_one(company['link_selector'])
                link = f"https://www.google.com/about/careers/applications/{link_tag['href']}" if link_tag else "Link not found"

                job = {
                    "company": company_name,
                    "title": title,
                    "location": location,
                    "experience": experience,
                    "link": link,
                    "jobType": "Full-Time",
                }
                jobs.append(job)
            except AttributeError as e:
                print(f"Error parsing a job card for {company['name']} on page {page}: {e}")

        print(f"Scraped {len(job_cards)} jobs from {company['name']} on page {page}")
        page += 1

    return jobs

def post_jobs_to_backend(jobs):
    url = "http://localhost:5000/jobs"
    headers = {'Content-Type': 'application/json'}

    for job in jobs:
        try:
            response = requests.post(url, data=json.dumps(job), headers=headers)
            if response.status_code == 201:
                print(f"Successfully added job: {job['title']}")
            else:
                print(f"Failed to add job: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending job to backend: {e}")

def main():
    # Step 1: Delete all existing jobs
    delete_all_jobs()

    # Step 2: Scrape and post new jobs
    all_jobs = []
    for company in company_configs:
        jobs = scrape_company_jobs(company)
        all_jobs.extend(jobs)

    if all_jobs:
        post_jobs_to_backend(all_jobs)

if __name__ == "__main__":
    main()
