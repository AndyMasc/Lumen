from django.shortcuts import render, redirect

# Create your views here.
from .models import startupIdea
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    startups = startupIdea.objects.filter(user=request.user)

    context = {'startups': startups}
    return render(request, 'workspace/dashboard.html', context)

@login_required
def add_startup(request):
    if request.method == 'POST':
        startupName = request.POST.get('startupName')
        description = request.POST.get('description')
        startupDetails = startupIdea(startupName=startupName, description=description, user=request.user)
        startupDetails.save()
        return redirect("workspace:dashboard")
    return render(request, 'workspace/add_startup.html')