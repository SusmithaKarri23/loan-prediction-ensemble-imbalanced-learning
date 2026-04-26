from django import forms
from .models import SimulationScenario

class SimulationForm(forms.ModelForm):
    class Meta:
        model = SimulationScenario
        fields = ['scenario_name', 'simulated_income', 'simulated_expenses', 'simulated_loan_amount',
                  'simulated_credit_score', 'simulated_existing_debts', 'simulated_duration']
        widgets = {
            'scenario_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., What if I earn 20% more?'}),
            'simulated_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'simulated_expenses': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'simulated_loan_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'simulated_credit_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'simulated_existing_debts': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'simulated_duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
