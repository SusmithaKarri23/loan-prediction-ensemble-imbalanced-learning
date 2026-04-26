from django.contrib import admin
from .models import SimulationScenario

@admin.register(SimulationScenario)
class SimulationScenarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario_name', 'eligibility_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'scenario_name']
    readonly_fields = ['created_at']
