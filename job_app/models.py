from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField


# Create your models here.

class User(AbstractUser):
    TYPE_CHOICES = [
        ('S', 'Seeker'),
        ('E', 'Employer')
    ]
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='images/avatars/', default = 'images/avatar.svg')
    user_type = models.CharField(
        max_length = 2,
        choices = TYPE_CHOICES,
        default = 'S'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
class Company(models.Model):
    company_name = models.CharField(max_length=250)
    main_service = models.CharField(max_length=200, default="IT Service")
    founder = models.CharField(max_length=400, default="Aryush Khatri")
    founded = models.DateField(null=True, blank=True)
    company_description = models.TextField(blank=True, null=True)
    motto = models.TextField(default="Please insert Company short motto")
    company_size = models.CharField(default="1+")
    services = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=200)
    company_link = models.URLField(blank=True, null=True)
    company_picture = models.ImageField(default="images/company_default.png")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.company_name
    
    
    
    

    
    
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
    company = models.ForeignKey('Company', on_delete=models.SET_NULL,null=True,blank=True)
    job_post = models.CharField(max_length=100)
    job_description = models.TextField()
    job_status = models.CharField(max_length=1,choices=STATUS_CHOICES)
    salary_range = models.CharField(max_length=100)
    job_type=models.CharField(max_length=1,choices=JOB_TYPE_CHOICES)
    post_logo = models.ImageField(default = "images/job_default.jpg")
    job_responsibility = models.TextField(default="DO your job anyhow")
    requirements = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.job_post
    
class Apply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)  
    email = models.EmailField(max_length=200,default="email@gmail.com")
    linkedin = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    address = models.CharField(max_length =200, default="address")
    full_name = models.CharField(max_length=300, default="fullname")
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} applied for {self.job}"
    
    class Meta:
        constraints =[
            models.UniqueConstraint(fields=("user","job"), name="unique_apply")
        ]