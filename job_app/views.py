from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .models import Apply, Job, Company
from .serializers import ApplySerializer, JobSerializer

# Create your views here.

def home(request):
    return render(request, 'job_app/home.html')
def job(request):
    jobs = Job.objects.all()
    return render(request, 'job_app/job.html',{'jobs':jobs})
def company(request):
    companies = Company.objects.all()
    return render(request, 'job_app/company.html',{'companies':companies})

class ApplyViewSet(ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
    
class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
