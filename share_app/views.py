from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .forms import RegisterForm
from .models import User


# Create your views here.

class LandingPage(TemplateView):
    template_name = 'share_app/index.html'


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/form.html')


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/login.html')


class Register(View):
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):

        return render(request, 'share_app/register.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            print(form.cleaned_data)
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
