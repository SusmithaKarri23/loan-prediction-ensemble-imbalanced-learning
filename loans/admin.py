from django.contrib import admin
from .models import LoanApplication, LoanRecommendation

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'loan_type', 'loan_amount', 'status', 'prediction_score', 'created_at']
    list_filter = ['status', 'loan_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'purpose']
    readonly_fields = ['created_at', 'updated_at', 'prediction_score']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'loan_type', 'loan_amount', 'loan_duration_months', 'purpose')
        }),
        ('Financial Details', {
            'fields': ('employment_status', 'annual_income', 'existing_debts', 'credit_score', 'collateral')
        }),
        ('Review', {
            'fields': ('status', 'prediction_score', 'admin_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(LoanRecommendation)
class LoanRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_loan_type', 'recommended_amount', 'interest_rate', 'created_at']
    search_fields = ['user__username']
