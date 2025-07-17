from django.shortcuts import render, redirect

# Create your views here.
from .models import StartupIdea, StartupEvaluation
from django.contrib.auth.decorators import login_required
from google import genai
from django.conf import settings

@login_required
def dashboard(request):
    startups = StartupIdea.objects.filter(user=request.user)
    context = {'startups': startups}
    return render(request, 'workspace/dashboard.html', context)

@login_required
def add_startup(request):
    if request.method == 'POST':
        startup_name = request.POST.get('startup_name')
        description = request.POST.get('description')
        StartupDetails = StartupIdea(startup_name=startup_name, description=description, user=request.user)
        StartupDetails.save()
        return redirect("workspace:dashboard")
    return render(request, 'workspace/add_startup.html')

@login_required
def startup_evaluation(request, StartupIdea_id):
    startup = StartupIdea.objects.get(user=request.user, id=StartupIdea_id)

    evaluation = create_evaluation(startup)

    return render(request, 'workspace/startup_evaluation.html', {'startup':startup, 'evaluation':evaluation})

def create_evaluation(startup):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Critically evaluate the following startup idea: {startup.description}. Format your response as plain text (no markdown, no code blocks). Provide a detailed analysis including strengths, weaknesses, and potential market impact, viability and all other factors. Keep answer informative, but concise. 1 paragraph maximum."
    )
    evaluation = StartupEvaluation(startup=startup, evaluation_text=response.text)
    evaluation.save()
    return evaluation