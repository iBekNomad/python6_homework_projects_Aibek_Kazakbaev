from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, RegisterActivateView, UserDetailView, UserIndexView, UserChangeView, \
    UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='create'),
    path('activate/<uuid:token>/', RegisterActivateView.as_view(), name='activate'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('', UserIndexView.as_view(), name='user_list'),
    path('<int:pk>/change/', UserChangeView.as_view(), name='change'),
    path('<int:pk>/password_change/', UserPasswordChangeView.as_view(), name='password_change')
]
