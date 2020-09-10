from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.urls import reverse, reverse_lazy

from webapp.models import Project
from webapp.forms import ProjectForm, SimpleSearchForm, UserForm


class ProjectIndexView(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'project/project_index.html'
    ordering = ['-start_date']
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectView(DetailView):
    template_name = 'project/project_view.html'
    model = Project
    paginate_issues_by = 5
    paginate_issues_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        issues, page, is_paginated = self.paginate_issues(self.object)
        context['issues'] = issues
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_issues(self, project):
        issues = project.issues.all().order_by('-create_at')
        if issues.count() > 0:
            paginator = Paginator(issues, self.paginate_issues_by, orphans=self.paginate_issues_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return issues, None, False


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/project_create.html'
    form_class = ProjectForm
    model = Project

    def form_valid(self, form):
        user = get_user_model().objects.filter(pk=self.request.user.pk)
        project = form.save(commit=False)
        project.save()
        project.user.set(user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'webapp.change_project'

    def has_permission(self):
        project = self.get_object()
        return super().has_permission() or project.user == self.request.user

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    permission_required = 'webapp.delete_project'
    success_url = reverse_lazy('project_index')


class UserAddView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = UserForm
    template_name = 'project/add_user.html'
    permission_required = 'auth.add_user'

    def has_permission(self):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in self.project.user.all()

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.project
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})
