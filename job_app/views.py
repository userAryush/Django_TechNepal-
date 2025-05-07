from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet 
from .models import Apply, Job, Company
from .serializers import ApplySerializer, JobSerializer

# Create your views here.

def home(request):
    return render(request, 'job_app/home.html')
def job(request):
    jobs = Job.objects.all()
 
    return render(request, 'job_app/job.html',{'jobs':jobs})
def job_detail(request, job_id):
    jobs = Job.objects.get(pk=job_id)
    return render(request, 'job_app/details_job.html',{'jobs':jobs})

def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        portfolio_link = request.POST.get('portfolio')
        linkedin_link = request.POST.get('linkedin')
        resume = request.POST.get('resume')
        
        Apply.objects.create(user = request.user,job=job,email=email,linkedin = linkedin_link,portfolio_link=portfolio_link, resume=resume,address=address,full_name=fullname)
        
        return redirect('job_detail',job_id)
    
    
    return render(request, 'job_app/job_apply.html')
def company(request):
    companies = Company.objects.all()
    return render(request, 'job_app/company.html',{'companies':companies})
def company_detail(request, company_id):
    companies = Company.objects.get(pk = company_id)
    return render(request, 'job_app/company_detail.html',{'companies':companies})

class ApplyViewSet(ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
    
class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

