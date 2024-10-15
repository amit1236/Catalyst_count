from django.db import models
from django.contrib.auth.models import User  # Import User model

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link each company to a user
    revenue = models.BigIntegerField()
    name = models.CharField(max_length=255, db_index=True)
    domain = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    year_founded = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    size_range = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True, db_index=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True, db_index=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
