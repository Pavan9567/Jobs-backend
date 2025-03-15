from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from jobs.models import Job
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q


def fetch_jobs(request):
    # Path to ChromeDriver
    chrome_driver_path = r"C:\chromedriver\chromedriver-win64\chromedriver.exe"  # Windows

    # Set up ChromeDriver
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--window-size=1920,1080")  # Set window size
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Navigate to LinkedIn jobs page
        driver.get("https://www.linkedin.com/jobs/search/")

        # Wait for the page to load
        time.sleep(10)  # Adjust the sleep time as needed

        print(driver.page_source)

        with open("linkedin_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Scroll to load more jobs (optional)
        for _ in range(3):  # Scroll 3 times to load more jobs
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new jobs to load


        # Extract job details
        job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list > li")

        jobs = []

        for job_element in job_elements:
            try:
                title = job_element.find_element(By.CSS_SELECTOR, "div.base-search-card__info > h3").text.strip()
                company = job_element.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle a").text.strip()
                location = job_element.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
                application_link = job_element.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")

                # Save job to the database
                if title != "" and company != "" and location != "":
                    job = Job.objects.create(
                    title=title,
                    company=company,
                    location=location,
                    experience="Not specified",  # LinkedIn does not always specify experience
                    application_link=application_link
                )
                else:
                    print(f"Skipping invalid job: {job_element}")

                jobs.append(job)

                print(f"Found job: {title} at {company}")
            except Exception as e:
                print(f"Error parsing job: {e}")

    finally:
        # Close the browser
        driver.quit()

    jobs = Job.objects.all()

    jobs_data = [{
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "application_link": job.application_link
    } for job in jobs]

    return JsonResponse({'status': 'success', 'jobs': jobs_data})



def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return JsonResponse({
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'experience': job.experience,
        'application_link': job.application_link
    })

def search_jobs(request):
    query = request.GET.get('query', '')
    jobs = Job.objects.filter(Q(title__icontains=query))
    job_list = [{
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'experience': job.experience,
        'application_link': job.application_link
    } for job in jobs]

    return JsonResponse({'jobs': job_list})