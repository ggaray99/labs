from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('setup/', views.setup, name='setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/appointments/new/', views.appointment_new, name='appointment_new'),
    path('dashboard/appointments/<uuid:appointment_id>/status/', views.appointment_status, name='appointment_status'),
    path('dashboard/patients/', views.patient_list, name='patient_list'),
    path('dashboard/patients/new/', views.patient_new, name='patient_new'),
    path('dashboard/patients/<uuid:patient_id>/', views.patient_detail, name='patient_detail'),
    path('dashboard/landing/', views.landing_admin, name='landing_admin'),
    path('p/<slug:slug>/', views.public_landing, name='public_landing'),
    path('p/<slug:slug>/booking/', views.booking, name='booking'),
    path('p/<slug:slug>/review/<str:token>/', views.public_review, name='public_review'),
    path('api/patients/search/', views.patient_search_api, name='patient_search_api'),
]
