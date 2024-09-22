from django.urls import path
from .views import AuthPage, LoginPageView

urlpatterns = [
    path('', AuthPage.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
]
