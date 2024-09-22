from django.urls import path
from .views import IndexView, ShopView, ThankYouView, AboutView, ContactView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('th/', ThankYouView.as_view(), name='th'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]
