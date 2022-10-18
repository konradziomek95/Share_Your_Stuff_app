import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm
from .models import Category, Donation, Institution, User


# Create your views here.

class LandingPage(TemplateView):
    template_name = 'share_app/index.html'

    def get_context_data(self, **kwargs):
        institutions = Institution.objects.all()
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        charity = Institution.objects.filter(type=3)
        donations = Donation.objects.all()
        number_of_bags = 0
        for donation in donations:
            number_of_bags += donation.quantity

        ctx = {'number': number_of_bags,
               'institutions': institutions,
               'foundations': foundations,
               'organizations': organizations,
               'charity': charity}
        return ctx


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


class AddDonation(LoginRequiredMixin, View):
    login_url = '/login/'
    form_class = 1

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories,
               'institutions': institutions}
        return render(request, 'share_app/form.html', ctx)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = json.load(request)
        obj = Donation.objects.create(user=user,
                                      institution_id=int(data['organization']),
                                      quantity=int(data['bags']),
                                      address=data['address'],
                                      city=data['city'],
                                      zip_code=data['postcode'],
                                      phone_number=data['phone'],
                                      pick_up_date=data['data'],
                                      pick_up_time=data['time'],
                                      pick_up_comment=data['more_info']
                                      )
        categories = data['categories'].split(',')
        for elem in categories:
            category_object = Category.objects.get(pk=int(elem))
            obj.categories.add(category_object)
        obj.save()
        return redirect('success')


class SuccessFormView(TemplateView):
    template_name = 'share_app/form-confirmation.html'


class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user = request.user
        donations = Donation.objects.filter(user=user)
        if donations:
            return render(request, 'share_app/user.html', {'donations': donations})
        return render(request, 'share_app/user.html')
