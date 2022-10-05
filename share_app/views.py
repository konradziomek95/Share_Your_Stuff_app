from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


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
    def get(self, request, *args, **kwargs):
        return render(request, 'share_app/register.html')
