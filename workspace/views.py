from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from serpapi import GoogleSearch
from google import genai

# Create your views here.
from .models import StartupIdea, StartupEvaluation


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
    startup_obj, created = StartupEvaluation.objects.get_or_create(startup=startup)

    if not startup.tags or startup.tags == 'General':
        assign_startup_tags(startup)

    if not startup_obj.evaluation_text:
        create_evaluation_summary(startup, startup_obj)

    if not startup_obj.market_trends:
        get_market_trends(startup, startup_obj)

    if not startup_obj.swot_analysis:
        create_swot_analysis(startup, startup_obj)

    if not startup_obj.overall_score:
        create_overall_rating(startup, startup_obj)

    if not startup_obj.areas_for_improvement:
        suggest_areas_for_improvement(startup, startup_obj)

    return render(request, 'workspace/startup_evaluation.html', {'startup':startup, 'startup_obj':startup_obj})

# Functions to produce various startup reports based on startup ideas. Not views, but utility functions to be used in views.

def load_gemini_response(prompt):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = f"{prompt}. Do not use code blocks or markdown formatting. Use linebreaks where and if appropriate. If the idea is too broad or silly, respond sensibly and shortly and/or not applicable.",
    )
    return response

def assign_startup_tags(startup):
    prompt = f"Generate a tag for the following startup idea called {startup.startup_name}. EG engineering, music, food, technology...: The description is: {startup.description}. Format your response as a single descriptive word/tag of which field the idea falls into. Never respond with more than one word."
    response = load_gemini_response(prompt)
    # Save the response text as tags for the startup
    startup.tags = response.text
    startup.save()

def create_evaluation_summary(startup, startup_obj):
    prompt = f"Critically evaluate the following startup idea: {startup.description}, under the name '{startup.startup_name}'. Format your response as plain text (no markdown, no code blocks). Provide a detailed analysis including strengths, weaknesses, and potential market impact, viability and all other factors. Keep answer informative, but concise. 1 paragraph maximum."
    response = load_gemini_response(prompt)

    startup_obj.evaluation_text = response.text
    startup_obj.save()

def get_market_trends(startup, startup_obj):
    params = {
        "engine": "google_trends",
        "q": startup.tags,  # Use the startup's tags for the query
        "data_type": "TIMESERIES",
        "api_key": settings.SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    market_trend = results["interest_over_time"]

    prompt = f"Analyze the following market trend data for the startup idea '{startup.startup_name}': {market_trend}. Provide a concise summary of the market trends, including any significant patterns or insights that could impact the startup's success. Ensure all numbers provided have context, dont just say numbers, explain their meaning. Make sure each section is separated by a line break and is at max 3 sentences. Do not try to condense multiple sections (or dates of interest) into one however. Explain each section individually yet concisely. In your overview, ensure you talk about the implications the data has for the startup idea. EG demand..."
    response = load_gemini_response(prompt)

    startup_obj.market_trends = response.text
    startup_obj.save() # Save text version of the market trends analysis

def create_swot_analysis(startup, startup_obj):
    prompt = f"Perform a SWOT analysis for the startup idea '{startup.startup_name}' with the description: {startup.description}. Provide a detailed analysis including strengths, weaknesses, opportunities, and threats. Format your response as plain text. Keep answer informative, but concise. 1 paragraph maximum, with appropriate line breaks, after strengths section, weaknesses section, oppurtunities section, and threats section."
    response = load_gemini_response(prompt)

    startup_obj.swot_analysis = response.text
    startup_obj.save()

def create_overall_rating(startup,  startup_obj):
    prompt = f"Provide an overall rating for the startup idea '{startup.startup_name}' with the description {startup.description} based on the following evaluation: {startup_obj.evaluation_text}. Consider factors such as market potential, innovation, and feasibility. Rate the startup on a scale of 1 to 10, with 10 being the highest. Do not respond with a fraction. A integer only. No words. If you cannot give a rating, respond with 0."
    response = load_gemini_response(prompt)

    startup_obj.overall_score = int(response.text)
    startup_obj.save()

def suggest_areas_for_improvement(startup, startup_obj):
    prompt = f"Suggest areas for improvement for the startup idea '{startup.startup_name}' with the description {startup.description}. Provide specific recommendations that could enhance the startup's viability and success. Format your response as plain tex. Keep answer informative, but concise. 1 paragraph maximum."
    response = load_gemini_response(prompt)

    startup_obj.areas_for_improvement = response.text
    startup_obj.save()