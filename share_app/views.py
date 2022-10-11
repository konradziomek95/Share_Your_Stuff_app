from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, logout, login
from .forms import LoginForm, RegisterForm
from .models import User, Institution


# Create your views here.

class LandingPage(TemplateView):
    template_name = 'share_app/index.html'

    def get_context_data(self, **kwargs):
        institutions = Institution.objects.all()
        ctx = {'number': 1,
               'institutions': institutions}
        return ctx


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/form.html')


class Login(View):
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/login.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            password = cd['password']
            user = authenticate(email=email, password=password)
            login(self.request, user)
            return redirect('index')
        return redirect('register')


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class Register(View):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/register.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            password = cd['password1']
            User.objects.create_user(email=email,
                                     password=password,
                                     first_name=first_name,
                                     last_name=last_name)
            return redirect('/login/')
        return redirect('register')
