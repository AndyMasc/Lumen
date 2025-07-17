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

@login_required()
def startup_evaluation(request, StartupIdea_id):
    startup = StartupIdea.objects.get(user=request.user, id=StartupIdea_id)

    assign_startup_tags(startup)
    evaluation = create_evaluation_summary(startup)

    return render(request, 'workspace/startup_evaluation.html', {'startup':startup, 'evaluation':evaluation})

# Functions to produce various startup reports based on startup ideas. Not views, but utility functions to be used in views.
def load_gemini_response(prompt):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    return response

def assign_startup_tags(startup):
    response = load_gemini_response(f"Generate a tag for the following startup idea called {startup.startup_name}. EG engineering, music, food, technology...: The description is: {startup.description}. Format your response as a single descriptive word/tag of which field the idea falls into.")
    # Save the response text as tags for the startup
    startup.tags = response.text
    startup.save()

def create_evaluation_summary(startup):
    response = load_gemini_response(f"Critically evaluate the following startup idea: {startup.description}, under the name '{startup.startup_name}'. Format your response as plain text (no markdown, no code blocks). Provide a detailed analysis including strengths, weaknesses, and potential market impact, viability and all other factors. Keep answer informative, but concise. 1 paragraph maximum.")
    # Save the evaluation to the database
    evaluation = StartupEvaluation(startup=startup, evaluation_text=response.text)
    evaluation.save()
    return evaluation