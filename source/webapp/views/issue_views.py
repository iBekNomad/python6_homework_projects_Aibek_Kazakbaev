from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlencode
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.urls import reverse, reverse_lazy

from webapp.models import Issue, Project
from webapp.forms import IssueForm, SimpleSearchForm


class IndexView(ListView):
    context_object_name = 'issues'
    model = Issue
    template_name = 'issue/index.html'
    ordering = ['-create_at']
    paginate_by = 9
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
            query = Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class IssueView(DetailView):
    template_name = 'issue/issue_view.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IssueCreateView(CreateView):
    template_name = 'issue/issue_create.html'
    form_class = IssueForm
    model = Issue

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect('project_view', pk=project.pk)


class IssueUpdateView(UpdateView):
    model = Issue
    template_name = 'issue/issue_update.html'
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.object.pk})


class IssueDeleteView(DeleteView):
    template_name = 'issue/issue_delete.html'
    model = Issue
    success_url = reverse_lazy('index')
