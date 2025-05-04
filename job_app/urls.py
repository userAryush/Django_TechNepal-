
from django.urls import path, include
from job_app.views import ApplyViewSet, JobViewSet ,home,job, company,job_detail

urlpatterns = [

    path('job_apply/', ApplyViewSet.as_view({'post':'create','get':'list'})),
    path('',home, name='home'),
    path('jobs/',job, name='job'),
    path('companies/',company, name='company'),
    path('job-detail/<int:pk>/',job_detail, name='job_detail'),
]
