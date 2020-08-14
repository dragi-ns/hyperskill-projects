"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

import home.views
import resume.views
import vacancy.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumes/', resume.views.ResumeView.as_view()),
    path('resume/new', resume.views.AddResumeView.as_view()),
    path('vacancies/', vacancy.views.VacancyView.as_view()),
    path('vacancy/new', vacancy.views.AddVacancyView.as_view()),
    path('login', home.views.HyperLoginView.as_view()),
    path('signup', home.views.HyperSignupView.as_view()),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('home/', home.views.UserProfileView.as_view()),
    path('', home.views.HomeView.as_view())
]
