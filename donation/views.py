from django.shortcuts import render
from django.views import View

from donation.models import Institution, Donation
from django.contrib.auth.models import User


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


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        username = name+surname
        password = request.POST['password']
        re_password = request.POST['password2']
        if password == re_password:
            User.objects.create(username=username, password=password)
            return render(request, 'login.html')
        else:
            return render(request, 'add_user.html', {'username': username, 'message': 'hasła nie sa te same'})