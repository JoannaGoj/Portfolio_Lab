from django.shortcuts import render, redirect
from django.views import View

from donation.models import Institution, Donation, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all()
        donations = Donation.objects.all()
        institutions_count = institutions.count()
        donations_count = donations.all().count()
        return render(request, 'index.html',
                      {'institutions_count': institutions_count, 'institutions': institutions, 'donations': donations,
                       'donations_count': donations_count})


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        categories = Category.objects.all()
        institution = Institution.objects.all()
        return render(request, 'form.html', {'user': user, 'categories': categories, 'institution': institution})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'register.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('first_name', False)
        surname = request.POST.get('surname', False)
        email = request.POST['email']
        password = request.POST.get('password', False)
        re_password = request.POST.get('password2', False)
        if password == re_password:
            User.objects.create_user(username=email, email=email, password=password, last_name=surname,
                                     first_name=first_name)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'message': 'hasła nie są takie same'})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')
