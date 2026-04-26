from django.urls import path
from . import views

app_name = 'simulator'

urlpatterns = [
    path('run/', views.run_simulation, name='run_simulation'),
    path('results/<int:pk>/', views.simulation_results, name='simulation_results'),
    path('history/', views.simulation_history, name='simulation_history'),
]
