from django.urls import path
from accounts.views import SignUpView, user_login

urlpatterns = [
    path('accounts/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', user_login, name='login'),

]
