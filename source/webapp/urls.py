from django.urls import path, include
from webapp.views import IndexView, IssueCreateView, IssueView, \
    IssueUpdateView, IssueDeleteView, ProjectIndexView, ProjectView, ProjectCreateView, ProjectUpdateView, \
    ProjectDeleteView, UserAddView, project_mass_action_view


urlpatterns = [
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
]
