from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('apply/', views.apply_loan, name='apply_loan'),
    path('status/<int:pk>/', views.loan_status, name='loan_status'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('check-eligibility/', views.check_eligibility, name='check_eligibility'),
]
