from django.urls import path, include
from rest_framework import routers

from .views import CarViewSet, RateView, PopularView

router = routers.DefaultRouter()
router.register('cars', CarViewSet, basename='cars')

urlpatterns = [
    path('', include((router.urls, 'rating'))),
    path('rate/<pk>', RateView.as_view(), name='rate'),
    path('popular/', PopularView.as_view(), name='popular')
]