from django.urls import path
from . import views

urlpatterns = [
    path('fetch-jobs/', views.fetch_jobs, name='fetch_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_details'),
    path('search-jobs/', views.search_jobs, name='search_jobs')
]
