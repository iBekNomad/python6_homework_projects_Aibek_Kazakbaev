from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from accounts.forms import MyUserCreationForm
from django.views.generic import CreateView


# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             context['has_error'] = True
#     return render(request, 'registration/login.html', context=context)
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('index')


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
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
