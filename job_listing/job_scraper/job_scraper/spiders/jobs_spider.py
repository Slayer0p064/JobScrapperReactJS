import scrapy
import requests
import json
from datetime import datetime

class JobSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?q=Software&countryCode2=US&radius=30&radiusUnit=mi&page=1&pageSize=20'
    ]

    def start_requests(self):
        headers = {
            "x-api-key": "1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8"
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        if response.status == 403:
            self.logger.error("Access forbidden. Check headers or API requirements.")
        elif response.status == 200:
            try:
                # Parse the JSON response
                data = json.loads(response.text)  # Convert JSON string to Python dictionary
                jobs = data.get('data', [])
                self.logger.info(f"Found {len(jobs)} jobs.")

                for job in jobs:
                    # Reformat posted_date to YYYY-MM-DD format
                    raw_posted_date = job.get('postedDate')
                    try:
                        posted_date = datetime.strptime(raw_posted_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                    except (ValueError, TypeError):
                        posted_date = None  # Set to None if parsing fails

                    job_data = {
                        'title': job.get('title'),
                        'company_name': job.get('companyName'),
                        'location': job.get('jobLocation', {}).get('displayName'),
                        'posted_date': posted_date,
                        'job_url': job.get('detailsPageUrl'),
                    }

                    # POST to Django backend
                    try:
                        django_response = requests.post(
                            'http://localhost:8000/api/jobs/add/',
                            json=job_data
                        )
                        if django_response.status_code == 201:
                            self.logger.info(f"Successfully posted job: {job_data['title']}")
                        else:
                            self.logger.error(f"Failed to post job: {django_response.text}")
                    except requests.RequestException as e:
                        self.logger.error(f"Error posting job to Django backend: {e}")
            except json.JSONDecodeError:
                self.logger.error("Failed to decode JSON response.")
        else:
            self.logger.error(f"Unexpected status code {response.status}: {response.text}")
