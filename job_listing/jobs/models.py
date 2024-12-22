from django.db import models

class Job(models.Model):
    job_id = models.CharField(max_length=255, null=True, unique=True)
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    posted_date = models.CharField( null=True, max_length=255)
    details_url = models.CharField(max_length=1024, null=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)
    location_type = models.CharField(max_length=255, null=True)
    employement = models.CharField(max_length=255, null=True)
    updated_date= models.CharField( null=True, max_length=255)



    def __str__(self):
        return self.title