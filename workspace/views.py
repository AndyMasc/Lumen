from django.shortcuts import render, redirect

# Create your views here.
from .models import StartupIdea, StartupEvaluation
from django.contrib.auth.decorators import login_required
from google import genai
from django.conf import settings
from serpapi import GoogleSearch

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
    market_trends = get_market_trends(startup).market_trends

    return render(request, 'workspace/startup_evaluation.html', {'startup':startup, 'evaluation':evaluation, 'market_trends':market_trends})

# Functions to produce various startup reports based on startup ideas. Not views, but utility functions to be used in views.
def load_gemini_response(prompt):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    return response

def assign_startup_tags(startup):
    prompt = f"Generate a tag for the following startup idea called {startup.startup_name}. EG engineering, music, food, technology...: The description is: {startup.description}. Format your response as a single descriptive word/tag of which field the idea falls into."
    response = load_gemini_response(prompt)
    # Save the response text as tags for the startup
    startup.tags = response.text
    startup.save()

def create_evaluation_summary(startup):
    prompt = f"Critically evaluate the following startup idea: {startup.description}, under the name '{startup.startup_name}'. Format your response as plain text (no markdown, no code blocks). Provide a detailed analysis including strengths, weaknesses, and potential market impact, viability and all other factors. Keep answer informative, but concise. 1 paragraph maximum."
    response = load_gemini_response(prompt)
    # Save the evaluation to the database
    evaluation = StartupEvaluation(startup=startup, evaluation_text=response.text)
    evaluation.save()
    return evaluation

def get_market_trends(startup):
    params = {
        "engine": "google_trends",
        "q": startup.tags,  # Use the startup's tags for the query
        "data_type": "TIMESERIES",
        "api_key": settings.SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    market_trend = results["interest_over_time"]

    prompt = f"Analyze the following market trend data for the startup idea '{startup.startup_name}': {market_trend}. Provide a concise summary of the market trends, including any significant patterns or insights that could impact the startup's success. Format your response as plain text (no md), with appropriate line breaks. Ensure all numbers provided have context, dont just say numbers, explain their meaning."
    response = load_gemini_response(prompt)

    trends = StartupEvaluation(startup=startup, market_trends=response.text)
    trends.save()
    return trends