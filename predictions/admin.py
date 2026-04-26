from django.contrib import admin
from .models import PredictionModel, PredictionLog

@admin.register(PredictionModel)
class PredictionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'is_active', 'trained_on']
    list_filter = ['is_active', 'trained_on']
    search_fields = ['name', 'version']

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'prediction_result', 'model_used', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
