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
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_registration(request):
    if request.method == 'GET':
        return render(request, 'job_app/user_register.html')

    if request.method == 'POST':
        # Collect fields
        first_name = request.POST.get('firstName', '').strip()
        last_name = request.POST.get('lastName', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
    
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists.'}, status=400)
        # Check email duplication
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'}, status=400)
        
        hash_password= make_password(password)
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
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
        messages.success(request, "User created successfully.")
        return redirect('user_log')
def login_view_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Invalid email or password.")

        return render(request, 'job_app/user_login.html')



def index(request):

 
    return render(request, 'job_app/index.html')


@login_required
def home(request):
    # checking if the user is authenticated
    print("Authenticated:", request.user.is_authenticated)
    print("User:", request.user)

    return render(request, 'job_app/home.html')

@login_required
def job(request):
    jobs = Job.objects.all()
 
    return render(request, 'job_app/job.html',{'jobs':jobs})

@login_required
def job_detail(request, job_id):
    jobs = Job.objects.get(pk=job_id)
    return render(request, 'job_app/details_job.html',{'jobs':jobs})

@login_required
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

@login_required
def company(request):
    companies = Company.objects.all()
    return render(request, 'job_app/company.html',{'companies':companies})

@login_required
def company_detail(request, company_id):
    companies = Company.objects.get(pk = company_id)
    return render(request, 'job_app/company_detail.html',{'companies':companies})
def forgot_password(request):
    pass

class ApplyViewSet(ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
    
class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        # Get the new username
        new_username = request.POST.get('username')

        # Check if the new username already exists in other users
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            messages.error(request, "This username is already taken by another user.")
            return redirect('user-profile')

        # Update the user's profile if the username is unique
        user.username = new_username
        user.first_name = request.POST.get('first_name')
        
        user.last_name = request.POST.get('last_name')

        #Builds the path where uploaded images (avatar, voter ID) will be saved — under static/user_images/
        upload_dir = os.path.join(settings.BASE_DIR, 'media/user_images/')
        #Makes sure the directory exists. If not, it creates it.
        os.makedirs(upload_dir, exist_ok=True)
        #  Creates a file system handler to save files to that directory.
        fs = FileSystemStorage(location=upload_dir)

        # Update the avatar 
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            avatar_name = fs.save(avatar_file.name, avatar_file)
            user.avatar = f'user_images/{avatar_name}'

        
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('home')
    return render(request, 'job_app/user_profile.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('index')



import json
def company_registration(request):
    if request.method == 'GET':
        return render(request, 'job_app/company_register.html')

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
        services_input = request.POST.get('services', '[]').strip()
        location = request.POST.get('location', '').strip()
        company_link = request.POST.get('company_link', '').strip()

        try:
            services = json.loads(services_input)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid services JSON.'}, status=400)

        if Company.objects.filter(company_name=company_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Company with this name already exists.'}, status=400)
        # Check email duplication
        if Company.objects.filter(company_email=company_email).exists():
            return JsonResponse({'status': 'error', 'message': 'Company with this email already exists.'}, status=400)
        if Company.objects.filter(company_email=company_email).exists():
            return JsonResponse({'status': 'error', 'message': 'Company with this email already exists.'}, status=400)

        
        # Generate credentials
        generated_password = generate_random_password()
        company_id = generate_random_unique_id()
        
        # Create User
        user = User.objects.create_user(
            username=company_name.replace(" ", "_")[:30],  # limit username length
            email=company_email,
            password=generated_password,
            user_type='E'
        )

        # Create company
        company = Company.objects.create(
            user=user,
            company_name=company_name,
            company_email=company_email,
            company_id=company_id,
            main_service=main_service,
            founder=founder,
            founded=founded,
            company_description=company_description,
            motto=motto,            
            company_size=company_size,
            services=services,
            location=location,
            company_link=company_link,

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
        messages.success(request, f"{company_name}'s account created successfully.")
        return redirect('company_log')
def login_view_company(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Invalid email or password.")

        return render(request, 'job_app/company_login.html')
    
    
    
@login_required
def company_home(request):
    jobs = Job.objects.filter(company_name= request.user.company_name)
 
    return render(request, 'job_app/company_home.html',{'jobs':jobs})