from django import forms
from .models import LoanApplication

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'loan_amount', 'loan_duration_months', 'purpose', 
                  'employment_status', 'annual_income', 'existing_debts', 'credit_score', 'collateral']
        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'loan_duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'employment_status': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'existing_debts': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'credit_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'collateral': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
