from django.db import models
from django.contrib.auth.models import AbstractUser

# Пользователь (с дополнением: телефон и аватар)
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)

# Категория подписки (например, Развлечения, Образование)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Подписка (основная таблица)
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period = models.CharField(max_length=20, choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')])
    next_payment_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# История платежей
class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField(auto_now_add=True)

# Уведомления
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
