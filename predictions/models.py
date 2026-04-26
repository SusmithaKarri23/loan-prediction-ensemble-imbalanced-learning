from django.db import models
from accounts.models import User

class PredictionModel(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=50)
    model_file = models.FileField(upload_to='ml_models/')
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=False)
    trained_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - v{self.version}"

class PredictionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_data = models.JSONField()
    prediction_result = models.DecimalField(max_digits=5, decimal_places=2)
    model_used = models.ForeignKey(PredictionModel, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prediction for {self.user.username} at {self.created_at}"
