from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import SubscriptionViewSet, CategoryViewSet, UserViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
