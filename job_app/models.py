from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    TYPE_CHOICES = [
        ('S', 'Seeker'),
        ('E', 'Employer')
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', default = 'images/avatar.svg')
    user_type = models.CharField(
        max_length = 2,
        choices = TYPE_CHOICES,
        default = 'S'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type']
    
    
class Company(models.Model):
    company_name = models.CharField(max_length=250)
    company_description = models.TextField()
    location = models.CharField(max_length=200)
    company_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class Apply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    linkedin = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Job(models.Model):
    STATUS_CHOICES = [
        ('O', 'Open'),
        ('C', 'Closed'),
    ]
    JOB_TYPE_CHOICES = [
        ('F', 'Full-time'),
        ('P', 'Part-time'),
        ('R', 'Remote'),
        ('I', 'Internship')
    ]
    company = models.ForeignKey('Company', on_delete=models.SET_NULL,null=True)
    job_post = models.CharField(max_length=100)
    job_description = models.TextField()
    job_status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    salary_range = models.CharField(max_length=100)
    job_type=models.CharField(max_length=1,choices=JOB_TYPE_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
