# users/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    """
    Kullanıcı kaydı (UserCreationForm kullanarak).
    """
    template_name = 'users/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Kullanıcı profili (giriş yapılmış olmalı).
    Basitçe kullanıcı bilgilerini gösteririz, ileride sipariş geçmişi vb. ekleyebilirsiniz.
    """
    template_name = 'users/profile.html'
    login_url = reverse_lazy('login')
