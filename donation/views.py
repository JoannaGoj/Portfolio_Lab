from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.urls import reverse
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


class AddDonation1(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        categories = Category.objects.all()
        institution = Institution.objects.all()
        return render(request, 'form.html', {'user': user, 'categories': categories, 'institution': institution})

    def post(self, request):
        categories = request.POST.getlist('categories')
        user_form_dictionary = {'categories': categories}
        request.session['user_form_dictionary'] = user_form_dictionary
        return redirect(reverse('add_donation2'))


class AddDonation2(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'form2.html', {'user': user})

    def post(self, request):
        how_many_bags = request.POST.getlist('bags')
        user_form_dictionary = request.session['user_form_dictionary']
        user_form_dictionary.update({'how_many_bags':how_many_bags})
        return redirect('add_donation4')


class AddDonation4(LoginRequiredMixin, View):
    def get(self, request):
        user_form_dictionary = request.session['user_form_dictionary']
        categories = user_form_dictionary.get('categories')
        institutions = Institution.objects.filter(categories__in=categories)
        return render(request, 'form4.html', {'user': request.user, 'institutions':institutions})

    def post(self, request):
        user_form_dictionary = request.session['user_form_dictionary']
        chosen_organization = request.POST.getlist('organization')
        user_form_dictionary.update({'chosen_organization': chosen_organization})
        return redirect('add_donation5')

# class AddDonation5(LoginRequiredMixin, View):
#     def get(self, request):
#         user = request.user
#         user_form_dictionary = request.session['user_form_dictionary']
#
#         return render(request, 'form5.html', {'user': user})
#
#     def post(self, request):
#         user_form_dictionary = request.session['user_form_dictionary']
#         institutions = Institution.objects.filter(type='1')
#         return redirect('add_donation5')
#
# class AddDonation6(LoginRequiredMixin, View):
#     def get(self, request):
#         user = request.user
#         user_form_dictionary = request.session['user_form_dictionary']
#         categories = user_form_dictionary.get('categories')
#         institutions = Institution.objects.filter(categories__institution__in=categories)
#         print(institutions)
#         return render(request, 'form4.html', {'user': user, 'institutions':institutions})
#
#     def post(self, request):
#         user_form_dictionary = request.session['user_form_dictionary']
#         types = user_form_dictionary.get('types')
#         institutions = Institution.objects.filter(type='1')
#         print(institutions)
#         print(f'3333333333{user_form_dictionary}')
#         return redirect('add_donation5')

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
