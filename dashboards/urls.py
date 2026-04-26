from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    # User dashboard
    path('user/', views.user_dashboard, name='user_dashboard'),
    
    # Admin dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/review-loans/', views.admin_review_loans, name='admin_review_loans'),
    path('admin/approve/<int:pk>/', views.admin_approve_loan, name='admin_approve_loan'),
    path('admin/reject/<int:pk>/', views.admin_reject_loan, name='admin_reject_loan'),
    path('admin/users/', views.admin_users_list, name='admin_users_list'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),
]
