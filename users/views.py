from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(students_group())
            user.is_staff = True
            user.save()
            return redirect('/login/?next=/')
        return render(request, 'users/register.html', {'form': form})
    else: 
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})



def students_group():
    return Group.objects.filter(name='Students').first()