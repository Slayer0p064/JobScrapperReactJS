from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.get_jobs),
    path('jobs/add/', views.add_job),
]
