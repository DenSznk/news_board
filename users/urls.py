from django.urls import path

from users.views import (EmailVerificationView, login, logout, profile,
                         registration)

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
