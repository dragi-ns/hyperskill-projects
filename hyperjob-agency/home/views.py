from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from resume.forms import ResumeForm
from vacancy.forms import VacancyForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': None,
            'form': None,
            'action_url': None
        }

        if not request.user.is_authenticated:
            return redirect('/login')

        if request.user.is_staff:
            context['title'] = 'Add new vacancy'
            context['form'] = VacancyForm
            context['action_url'] = '/vacancy/new'
        else:
            context['title'] = 'Add new resume'
            context['form'] = ResumeForm
            context['action_url'] = '/resume/new'

        return render(request, 'home/profile.html', context)


class HyperLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'home/login.html'


class HyperSignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'home/signup.html'
