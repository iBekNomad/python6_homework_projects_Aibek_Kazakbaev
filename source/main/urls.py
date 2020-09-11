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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from webapp.views import IndexView, IssueCreateView, IssueView, \
    IssueUpdateView, IssueDeleteView, ProjectIndexView, ProjectView, ProjectCreateView, ProjectUpdateView, \
    ProjectDeleteView, UserAddView, project_mass_action_view

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('issue/', include([
        path('<int:pk>/', IssueView.as_view(), name='issue_view'),
        path('<int:pk>/update/', IssueUpdateView.as_view(), name='issue_update'),
        path('<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    ])),

    path('projects/', include([
        path('<int:pk>/issues/add/', IssueCreateView.as_view(), name='issue_create'),
        path('', ProjectIndexView.as_view(), name='project_index'),
        path('<int:pk>/', ProjectView.as_view(), name='project_view'),
        path('add/', ProjectCreateView.as_view(), name='project_create'),
        path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
        path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
        path('mass-action/', project_mass_action_view, name='project_mass_action'),
        path('<int:pk>/user/add', UserAddView.as_view(), name='add_user')
    ])),

    path('accounts/', include('accounts.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
