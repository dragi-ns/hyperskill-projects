from django.views import View
from django.shortcuts import render, redirect, HttpResponse

from vacancy.forms import VacancyForm
from vacancy.models import Vacancy


class VacancyView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        return render(
            request,
            'vacancy/vacancies.html',
            context={'items': vacancies}
        )


class AddVacancyView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse(status=403)
        form = VacancyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Vacancy.objects.create(
                description=data['description'],
                author=request.user
            )
        return redirect('/home')

