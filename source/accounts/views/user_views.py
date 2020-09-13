from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.utils.http import urlencode

from accounts.forms import MyUserCreationForm
from django.views.generic import CreateView, View, DetailView, ListView

from accounts.models import AuthToken
from webapp.forms import SimpleSearchForm


class RegisterView(CreateView):
    model = User
    template_name = 'user/user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next:
            next_url = self.request.POST.get('next')
        if not next:
            next_url = reverse('index')
        return next_url


class RegisterActivateView(View):
    def get(self, request, *args, **kwargs):
        token = AuthToken.get_token(self.kwargs.get('token'))
        if token:
            if token.is_alive():
                user = token.user
                user.is_active = True
                user.save()
                login(request, user)
            token.delete()
        return redirect('index')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user/user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = self.object.projects.order_by('-start_date')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserIndexView(ListView, PermissionRequiredMixin):
    context_object_name = 'users'
    model = User
    template_name = 'user/user_list.html'
    paginate_by = 5
    paginate_orphans = 1
    permission_required = 'view_profile'

    # def has_permission(self):
    #     user = get_object_or_404(User, pk=self.kwargs.get('pk'))
    #     return super().has_permission() and self.request.user in user.groups.filter(
    #         name=['Project manager', 'Team leader'])

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
            query = Q(username__icontains=self.search_value) | Q(first_name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None
