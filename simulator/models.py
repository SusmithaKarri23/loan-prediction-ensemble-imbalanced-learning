from django.db import models
from accounts.models import User

class SimulationScenario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations')
    scenario_name = models.CharField(max_length=200)
    
    # Input parameters
    simulated_income = models.DecimalField(max_digits=12, decimal_places=2)
    simulated_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    simulated_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    simulated_credit_score = models.IntegerField()
    simulated_existing_debts = models.DecimalField(max_digits=12, decimal_places=2)
    simulated_duration = models.IntegerField()
    
    # Results
    eligibility_score = models.DecimalField(max_digits=5, decimal_places=2)
    recommended_action = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.scenario_name}"
