
from django.urls import path, include
from job_app.views import ApplyViewSet, JobViewSet ,home,job

urlpatterns = [

    path('job_apply/', ApplyViewSet.as_view({'post':'create','get':'list'})),
    path('',home, name='home'),
    path('jobs/',job, name='job')
]
