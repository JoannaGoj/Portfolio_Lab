from django.shortcuts import render
from django.views import View

from donation.models import Institution, Donation


# Create your views here.


class LandingPage(View):
    def get(self, request):
        institutions_count = Institution.objects.all().count()
        donations_count = Donation.objects.all().count()
        return render(request, 'index.html',
                      {'institutions_count': institutions_count, 'donations_count': donations_count})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')
