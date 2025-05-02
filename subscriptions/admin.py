from django.contrib import admin
from .models import User, Subscription, Category, Payment, Notification

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(Notification)
