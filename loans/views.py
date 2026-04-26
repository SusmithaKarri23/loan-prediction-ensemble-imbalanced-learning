from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LoanApplication, LoanRecommendation
from .forms import LoanApplicationForm
from predictions.utils import predict_loan_eligibility

@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            
            # Get prediction score
            prediction_data = {
                'annual_income': float(loan.annual_income),
                'loan_amount': float(loan.loan_amount),
                'credit_score': loan.credit_score,
                'existing_debts': float(loan.existing_debts),
                'loan_duration': loan.loan_duration_months,
            }
            loan.prediction_score = predict_loan_eligibility(prediction_data)
            loan.save()
            
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loans:loan_status', pk=loan.pk)
    else:
        # Pre-fill from user profile
        initial_data = {
            'annual_income': request.user.profile.annual_income,
            'credit_score': request.user.profile.credit_score,
            'existing_debts': request.user.profile.existing_loans,
        }
        form = LoanApplicationForm(initial=initial_data)
    return render(request, 'loans/apply_loan.html', {'form': form})

@login_required
def loan_status(request, pk):
    loan = get_object_or_404(LoanApplication, pk=pk, user=request.user)
    return render(request, 'loans/loan_status.html', {'loan': loan})

@login_required
def my_loans(request):
    loans = LoanApplication.objects.filter(user=request.user)
    return render(request, 'loans/my_loans.html', {'loans': loans})

@login_required
def check_eligibility(request):
    if request.method == 'POST':
        # Quick eligibility check without saving
        data = {
            'annual_income': float(request.POST.get('annual_income')),
            'loan_amount': float(request.POST.get('loan_amount')),
            'credit_score': int(request.POST.get('credit_score')),
            'existing_debts': float(request.POST.get('existing_debts')),
            'loan_duration': int(request.POST.get('loan_duration')),
        }
        score = predict_loan_eligibility(data)
        return render(request, 'loans/eligibility_result.html', {'score': score, 'data': data})
    return render(request, 'loans/check_eligibility.html')
