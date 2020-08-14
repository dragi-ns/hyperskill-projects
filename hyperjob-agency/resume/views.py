from django.views import View
from django.shortcuts import render, redirect, HttpResponse

from resume.forms import ResumeForm
from resume.models import Resume


class ResumeView(View):
    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()
        return render(
            request,
            'resume/resumes.html',
            context={'items': resumes}
        )


class AddResumeView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            return HttpResponse(status=403)
        form = ResumeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Resume.objects.create(
                description=data['description'],
                author=request.user
            )
        return redirect('/home')




