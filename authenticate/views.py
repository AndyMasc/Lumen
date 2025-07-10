from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

def register(request):
    form = CreateUserForm()
    context = {'form':form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authenticate:login')
        else:
            return render(request, 'authenticate/register.html', context)
    return render(request, 'authenticate/register.html', context)

def login(request):
    return HttpResponse('Login')