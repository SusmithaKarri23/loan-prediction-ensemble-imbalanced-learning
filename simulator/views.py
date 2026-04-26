from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SimulationScenario
from .forms import SimulationForm
from predictions.utils import predict_loan_eligibility

@login_required
def run_simulation(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit=False)
            simulation.user = request.user
            
            # Run prediction
            data = {
                'annual_income': float(simulation.simulated_income),
                'loan_amount': float(simulation.simulated_loan_amount),
                'credit_score': simulation.simulated_credit_score,
                'existing_debts': float(simulation.simulated_existing_debts),
                'loan_duration': simulation.simulated_duration,
            }
            simulation.eligibility_score = predict_loan_eligibility(data)
            
            # Generate recommendation
            if simulation.eligibility_score >= 70:
                simulation.recommended_action = "High approval probability. You can proceed with the loan application."
            elif simulation.eligibility_score >= 50:
                simulation.recommended_action = "Moderate approval probability. Consider improving credit score or reducing existing debts."
            else:
                simulation.recommended_action = "Low approval probability. Improve financial health before applying."
            
            simulation.save()
            messages.success(request, 'Simulation completed successfully!')
            return redirect('simulator:simulation_results', pk=simulation.pk)
    else:
        # Pre-fill with current profile
        initial_data = {
            'simulated_income': request.user.profile.annual_income,
            'simulated_credit_score': request.user.profile.credit_score,
            'simulated_existing_debts': request.user.profile.existing_loans,
            'simulated_expenses': request.user.profile.monthly_expenses * 12,
        }
        form = SimulationForm(initial=initial_data)
    
    return render(request, 'simulator/run_simulation.html', {'form': form})

@login_required
def simulation_results(request, pk):
    simulation = SimulationScenario.objects.get(pk=pk, user=request.user)
    return render(request, 'simulator/simulation_results.html', {'simulation': simulation})

@login_required
def simulation_history(request):
    simulations = SimulationScenario.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'simulator/simulation_history.html', {'simulations': simulations})
