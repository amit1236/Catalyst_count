from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('query/', views.query_builder, name='query_builder'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('check_insertion_progress/<str:cache_key>/', views.check_insertion_progress, name='check_insertion_progress'),
    path('api/companies/', views.company_list, name='company_list'),
]
