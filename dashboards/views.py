from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncDate
import json
from django.core.serializers.json import DjangoJSONEncoder

from loans.models import LoanApplication
from accounts.models import User
from predictions.models import PredictionLog


@login_required
def user_dashboard(request):
    if request.user.is_admin:
        return redirect('dashboards:admin_dashboard')
    
    # User statistics
    total_applications = LoanApplication.objects.filter(user=request.user).count()
    pending_applications = LoanApplication.objects.filter(user=request.user, status='pending').count()
    approved_loans = LoanApplication.objects.filter(user=request.user, status='approved').count()
    recent_applications = LoanApplication.objects.filter(user=request.user)[:5]
    
    context = {
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_loans': approved_loans,
        'recent_applications': recent_applications,
        'profile': request.user.profile,
    }
    return render(request, 'dashboards/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboards:user_dashboard')
    
    # Admin statistics
    total_users = User.objects.filter(user_type='user').count()
    total_applications = LoanApplication.objects.count()
    pending_applications = LoanApplication.objects.filter(status='pending').count()
    approved_applications = LoanApplication.objects.filter(status='approved').count()
    rejected_applications = LoanApplication.objects.filter(status='rejected').count()
    
    # Recent applications
    recent_applications = LoanApplication.objects.all()[:10]
    
    # Loan type distribution
    loan_type_stats = LoanApplication.objects.values('loan_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'total_users': total_users,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'rejected_applications': rejected_applications,
        'recent_applications': recent_applications,
        'loan_type_stats': loan_type_stats,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

@login_required
def admin_review_loans(request):
    if not request.user.is_admin:
        return redirect('dashboards:user_dashboard')
    
    pending_loans = LoanApplication.objects.filter(status='pending')
    return render(request, 'dashboards/admin_review_loans.html', {'pending_loans': pending_loans})

@login_required
def admin_approve_loan(request, pk):
    if not request.user.is_admin:
        return redirect('dashboards:user_dashboard')
    
    loan = get_object_or_404(LoanApplication, pk=pk)
    loan.status = 'approved'
    loan.reviewed_by = request.user
    loan.reviewed_at = timezone.now()
    
    if request.method == 'POST':
        loan.admin_notes = request.POST.get('admin_notes', '')
    
    loan.save()
    messages.success(request, f'Loan application #{loan.id} approved successfully!')
    return redirect('dashboards:admin_review_loans')

@login_required
def admin_reject_loan(request, pk):
    if not request.user.is_admin:
        return redirect('dashboards:user_dashboard')
    
    loan = get_object_or_404(LoanApplication, pk=pk)
    loan.status = 'rejected'
    loan.reviewed_by = request.user
    loan.reviewed_at = timezone.now()
    
    if request.method == 'POST':
        loan.admin_notes = request.POST.get('admin_notes', '')
    
    loan.save()
    messages.success(request, f'Loan application #{loan.id} rejected.')
    return redirect('dashboards:admin_review_loans')

@login_required
def admin_users_list(request):
    if not request.user.is_admin:
        return redirect('dashboards:user_dashboard')
    
    users = User.objects.filter(user_type='user')
    return render(request, 'dashboards/admin_users_list.html', {'users': users})

@login_required
def admin_analytics(request):
    if not request.user.is_admin:
        return redirect('dashboards:user_dashboard')
    
    from django.db.models import Avg, Sum, Count, Q
    from django.db.models.functions import TruncDate
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    from datetime import timedelta
    from django.utils import timezone
    
    # Calculate metrics
    total_applications = LoanApplication.objects.count()
    total_users = User.objects.filter(user_type='user').count()
    
    avg_loan_amount = LoanApplication.objects.aggregate(Avg('loan_amount'))['loan_amount__avg']
    avg_credit_score = LoanApplication.objects.aggregate(Avg('credit_score'))['credit_score__avg']
    
    approved_count = LoanApplication.objects.filter(status='approved').count()
    pending_count = LoanApplication.objects.filter(status='pending').count()
    rejected_count = LoanApplication.objects.filter(status='rejected').count()
    
    approval_rate = (approved_count / total_applications * 100) if total_applications > 0 else 0
    
    # Status distribution data for Chart.js
    status_data = {
        'labels': ['Pending', 'Approved', 'Rejected'],
        'data': [pending_count, approved_count, rejected_count],
        'colors': ['#F59E0B', '#10B981', '#EF4444']
    }
    
    # Loan type distribution
    loan_types = LoanApplication.objects.values('loan_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    loan_type_data = {
        'labels': [dict(LoanApplication.LOAN_TYPE_CHOICES).get(lt['loan_type'], lt['loan_type']) for lt in loan_types] if loan_types else [],
        'data': [lt['count'] for lt in loan_types] if loan_types else []
    }
    
    # Applications over time (last 30 days) - FIXED VERSION
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Use a simpler approach without TruncDate to avoid timezone issues
    applications_by_date = {}
    applications = LoanApplication.objects.filter(
        created_at__gte=thirty_days_ago
    ).order_by('created_at')
    
    for app in applications:
        if app.created_at:
            date_str = app.created_at.strftime('%Y-%m-%d')
            applications_by_date[date_str] = applications_by_date.get(date_str, 0) + 1
    
    # Generate all dates in the last 30 days for timeline
    date_labels = []
    date_counts = []
    current_date = thirty_days_ago.date()
    today = timezone.now().date()
    
    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')
        date_labels.append(date_str)
        date_counts.append(applications_by_date.get(date_str, 0))
        current_date += timedelta(days=1)
    
    timeline_data = {
        'labels': date_labels,
        'data': date_counts
    }
    
    # Credit score distribution
    credit_ranges = [
        ('300-549', 300, 549),
        ('550-649', 550, 649),
        ('650-749', 650, 749),
        ('750-850', 750, 850),
    ]
    
    credit_distribution = []
    for label, min_score, max_score in credit_ranges:
        count = LoanApplication.objects.filter(
            credit_score__gte=min_score,
            credit_score__lte=max_score
        ).count()
        credit_distribution.append({'label': label, 'count': count})
    
    credit_score_data = {
        'labels': [item['label'] for item in credit_distribution],
        'data': [item['count'] for item in credit_distribution]
    }
    
    # Average loan amount by type
    loan_amount_by_type = LoanApplication.objects.values('loan_type').annotate(
        avg_amount=Avg('loan_amount')
    ).order_by('-avg_amount')
    
    avg_amount_data = {
        'labels': [dict(LoanApplication.LOAN_TYPE_CHOICES).get(lt['loan_type'], lt['loan_type']) for lt in loan_amount_by_type] if loan_amount_by_type else [],
        'data': [float(lt['avg_amount']) if lt['avg_amount'] else 0 for lt in loan_amount_by_type] if loan_amount_by_type else []
    }
    
    context = {
        'avg_loan_amount': avg_loan_amount,
        'avg_credit_score': avg_credit_score,
        'approval_rate': approval_rate,
        'total_users': total_users,
        'total_applications': total_applications,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        
        # Serialize data for Chart.js (safe JSON encoding)
        'status_data_json': json.dumps(status_data, cls=DjangoJSONEncoder),
        'loan_type_data_json': json.dumps(loan_type_data, cls=DjangoJSONEncoder),
        'timeline_data_json': json.dumps(timeline_data, cls=DjangoJSONEncoder),
        'credit_score_data_json': json.dumps(credit_score_data, cls=DjangoJSONEncoder),
        'avg_amount_data_json': json.dumps(avg_amount_data, cls=DjangoJSONEncoder),
    }
    
    return render(request, 'dashboards/admin_analytics.html', context)
