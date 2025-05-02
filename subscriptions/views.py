from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscription, Category
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm, UserProfileForm
from subscriptions import models
from django.db.models import Sum

# Список всех подписок текущего пользователя
@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/list.html', {'subscriptions': subscriptions})

# Добавление новой подписки
@login_required
def subscription_add(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/form.html', {'form': form, 'title': 'Добавить подписку'})

# Редактирование подписки
@login_required
def subscription_edit(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('subscription_list')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'subscriptions/form.html', {'form': form, 'title': 'Редактировать подписку'})

# Удаление подписки
@login_required
def subscription_delete(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        subscription.delete()
        return redirect('subscription_list')
    return render(request, 'subscriptions/delete_confirm.html', {'subscription': subscription})


from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

from django.utils import timezone
from datetime import date
from .models import Notification
from datetime import timedelta

@login_required
def profile(request):
    user = request.user
    subscriptions = Subscription.objects.filter(user=user)
    payments = Payment.objects.filter(subscription__user=user)

    # Общее количество подписок
    total_subs = subscriptions.count()

    # Активные подписки
    active_subs = subscriptions.filter(is_active=True).count()

    # Сумма всех подписок (ежемесячных)
    total_sum = subscriptions.filter(is_active=True).aggregate(
        total=Sum('price'))['total'] or 0

    # Сумма оплат в текущем месяце
    today = date.today()
    monthly_spent = payments.filter(
        paid_date__year=today.year,
        paid_date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # 🔔 Уведомления: за 3 дня до оплаты
    upcoming = subscriptions.filter(
        next_payment_date__lte=today + timedelta(days=3),
        is_active=True
    )

    for sub in upcoming:
        # не создавать повторное уведомление
        Notification.objects.get_or_create(
            user=user,
            message=f"Напоминание: подписка на {sub.name} скоро требует оплату.",
            is_read=False
        )

    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]


    context = {
        'user': user,
        'total_subs': total_subs,
        'active_subs': active_subs,
        'total_sum': total_sum,
        'monthly_spent': monthly_spent,
        'notifications': notifications,
    }

    return render(request, 'auth/profile.html', context)

from .models import Payment
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def pay_now(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    # Создаём новый платёж
    Payment.objects.create(
        subscription=subscription,
        amount=subscription.price
    )

    return redirect('subscription_list')

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('/subscriptions/')

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'auth/profile_edit.html', {'form': form})


from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import OperationalError

def create_admin(request):
    try:
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@example.com'
            )
            return HttpResponse("✅ Суперпользователь создан: admin / admin123")
        else:
            return HttpResponse("ℹ️ Пользователь 'admin' уже существует")
    except OperationalError as e:
        return HttpResponse(f"❌ Ошибка базы данных: {str(e)}")
    except Exception as e:
        return HttpResponse(f"❌ Ошибка: {str(e)}")

