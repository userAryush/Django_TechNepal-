import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet 
from .models import Apply, Job, Company, User
from .serializers import ApplySerializer, JobSerializer
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.dateparse import parse_date
from django.utils.dateparse import parse_datetime
from django.utils.http import urlsafe_base64_decode 
from .utils import generate_random_password, generate_random_unique_id
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def user_registration(request):
    if request.method == 'GET':
        return render(request, 'vote/registration.html')

    if request.method == 'POST':
        # Collect fields
        first_name = request.POST.get('firstName', '').strip()
        middle_name = request.POST.get('middleName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        dob = parse_date(request.POST.get('dob', ''))
        user_photo = request.FILES.get('userPhotoUpload')
        user_type = request.POST.get('email', '').strip()


        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'}, status=400)
        # Check email duplication
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'}, status=400)
        # Save uploaded images to static/images/user_image/
        upload_dir = os.path.join(settings.BASE_DIR, 'static/images/user_image/')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)

        user_photo_name = fs.save(user_photo.name, user_photo)


        user_photo_path = f'user_images/{user_photo_name}'
      


        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            dob=dob,
            avatar=user_photo_path,
            user_type=user_type
        )
        # Send welcome email
        subject = "Welcome to Techनेपाल:!"
        body = (
            f"Dear {user.first_name} {user.last_name},\n\n"
            f"Your account has been created.\n"
            f"Username: {user.username}\n"
            f"If you have any questions, feel free to reach out.\n\n"
            "Best regards,\nTechनेपाल:! Team"
        )
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception as e:
            user.delete()  # Rollback user creation if email fails
            return JsonResponse({'status': 'error', 'message': f'Failed to send email to {user.email}: {e}'}, status=500)
        return JsonResponse({'status': 'success', 'message': 'Registration successful! Check your email for login details.', 'redirect_url': reverse('login_view')})


def company_registration(request):
    if request.method == 'GET':
        return render(request, 'vote/registration.html')

    if request.method == 'POST':
        # Collect fields
        company_name = request.POST.get('company_name', '').strip()
        company_email = request.POST.get('company_email', '').strip()
        main_service = request.POST.get('main_service', '').strip()
        founder = request.POST.get('founder', '').strip()
        founded = parse_date(request.POST.get('founded', ''))
        company_description = request.POST.get('company_description', '').strip()
        motto = request.POST.get('motto', '').strip()
        company_size = request.POST.get('company_size', '').strip()
        services = request.POST.get('services', '').strip()
        location = request.POST.get('location', '').strip()
        company_link = request.POST.get('company_link', '').strip()
        company_picture = request.FILES.get('CompanyPhotoUpload')
        

        if Company.objects.filter(company_name=company_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Company with this name already exists.'}, status=400)
        # Check email duplication
        if Company.objects.filter(company_email=company_email).exists():
            return JsonResponse({'status': 'error', 'message': 'Company with this email already exists.'}, status=400)
        # Save uploaded images to static/images/user_images/
        upload_dir = os.path.join(settings.BASE_DIR, 'static/images/company_picture/')
        os.makedirs(upload_dir, exist_ok=True)
        fs = FileSystemStorage(location=upload_dir)

        company_picture_name = fs.save(company_picture.name, company_picture)
        

        company_picture_path = f'company_picture/{company_picture_name}'
        

        # Generate credentials
        generated_password = generate_random_password()
        company_id = generate_random_unique_id()

        # Create company
        company = User.objects.create_user(
            company_name=company_name,
            company_email=company_email,
            company_id=company_id,
            main_service=main_service,
            founder=founder,
            founded=founded,
            company_description=company_description,
            motto=motto,
            company_description=company_description,
            
            company_size=company_size,
            services=services,
            location=location,
            company_link=company_link,
            company_picture=company_picture_path,
            password=generated_password,
        )
        # Send welcome email
        subject = "Welcome to Techनेपाल:!"
        body = (
            f"Warm Welcome to {company.company_name} ,\n\n"
            f"Your account has been created.\n\n\n"
            f"Email: {company.company_email}\n"
            f"Password: {generated_password}\n"
            f"Unique Company Id: {company_id}\n\n"
            f"Please login and change your password immediately.\n"
            f"Please copy or write down the Unique Company Id as it is necessary to Post, Edit and Delete Jobs.\n\n"

            f"If you have any questions, feel free to reach out.\n\n"
            "Best regards,\nTechनेपाल: Team"
        )
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        except Exception as e:
            company.delete()  # Rollback user creation if email fails
            return JsonResponse({'status': 'error', 'message': f'Failed to send email to {company.company_email}: {e}'}, status=500)
        return JsonResponse({'status': 'success', 'message': 'Registration successful! Check your email for login details.', 'redirect_url': reverse('login_view')})

def login_view_company(request):
    if 'next' in request.GET:
        messages.warning(request, 'User should be logged in to view this page.')
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        email = request.POST.get("company_email")
        password = request.POST.get("password")
        try:
            company = Company.objects.get(company_email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': "Company not found."})
        company = authenticate(request, email=email, password=password)
        if company is not None:
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful.',
                
            })
        else:
            return JsonResponse({'success': False, 'error': "Invalid credentials."})
    return render(request, 'vote/login.html')

def login_view_user(request):
    if 'next' in request.GET:
        messages.warning(request, 'User should be logged in to view this page.')
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(company_email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': "User not found."})
        user = authenticate(request, email=email, password=password)
        if user is not None:
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful.',
                
            })
        else:
            return JsonResponse({'success': False, 'error': "Invalid credentials."})
    return render(request, 'vote/login.html')
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

