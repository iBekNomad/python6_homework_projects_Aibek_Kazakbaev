from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views.generic import View, TemplateView, FormView, ListView
from django.urls import reverse

from webapp.models import Issue
from .forms import IssueForm, SimpleSearchForm


# class IndexView(View):
#     def get(self, request):
#         data = Issue.objects.all()
#         return render(request, 'index.html', context={
#             'issues': data
#         })


class IndexView(ListView):
    context_object_name = 'issues'
    model = Issue
    template_name = 'index.html'
    ordering = ['-create_at']
    paginate_by = 5
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


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=pk)

        context['issue'] = issue
        return context


class IssueCreateView(FormView):
    template_name = 'issue_create.html'
    form_class = IssueForm

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})


class IssueUpdateView(FormView):
    template_name = 'issue_update.html'
    form_class = IssueForm

    def dispatch(self, request, *args, **kwargs):
        self.issue = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = self.issue
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('initial')
        kwargs['instance'] = self.issue
        return kwargs

    def form_valid(self, form):
        self.issue = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('issue_view', kwargs={'pk': self.issue.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Issue, pk=pk)


class IssueDeleteView(TemplateView):
    template_name = 'issue_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        issue = get_object_or_404(Issue, pk=pk)

        context['issue'] = issue
        return context

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')
