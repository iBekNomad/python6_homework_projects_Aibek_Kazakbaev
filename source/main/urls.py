"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import IndexView, IssueCreateView, IssueView, \
    IssueUpdateView, IssueDeleteView, ProjectIndexView, ProjectView, ProjectCreateView, ProjectUpdateView, \
    ProjectDeleteView

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue_view'),
    path('projects/<int:pk>/issues/add/', IssueCreateView.as_view(), name='issue_create'),
    path('issue/<int:pk>/update/', IssueUpdateView.as_view(), name='issue_update'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),

    path('projects/', ProjectIndexView.as_view(), name='project_index'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('projects/add/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
