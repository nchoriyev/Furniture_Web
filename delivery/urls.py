from django.urls import path
from .views import DeliveryView

urlpatterns = [
    path('delivery/', DeliveryView.as_view(), name='delivery'),
]
