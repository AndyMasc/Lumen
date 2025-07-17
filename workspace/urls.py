from django.urls import path
from . import views

app_name = 'workspace'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_startup/', views.add_startup, name='add_startup'),
    path('startup_evaluation/<int:StartupIdea_id>/', views.startup_evaluation, name='startup_evaluation'),
]