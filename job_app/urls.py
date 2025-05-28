from django.urls import path, include
from job_app.views import ApplyViewSet, JobViewSet ,home,job, company,job_detail, job_apply, company_detail,login_view_user,login_view_company,company_registration,user_registration, forgot_password

urlpatterns = [

    path('job_apply/', ApplyViewSet.as_view({'post':'create','get':'list'})),
    
    path('login-user/',login_view_user, name='user_log'),
    path('login-company/',login_view_company, name='company_log'),
    path('company-registration/',company_registration, name='company_registration'),
    path('user-registration/',user_registration, name='user_registration'),
    path('forgot_password/',forgot_password, name='forgot_password'),
    path('',home, name='home'),
    path('jobs/',job, name='job'),
    path('companies/',company, name='company'),
    path('apply/<int:job_id>/',job_apply, name='job_apply'),
    path('job-detail/<int:job_id>/',job_detail, name='job_detail'),
    path('company-detail/<int:company_id>/',company_detail, name='company_detail'),
    
]
