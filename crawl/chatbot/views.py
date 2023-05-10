import openai
import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

@csrf_exempt
def chatbot(request):
    context = {}
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        openai.api_key = openai_api_key
        model_engine = "text-davinci-002"
        prompt = f"User: {user_input}\nAI:"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        context["response"] = response.choices[0].text.strip()
        context["user_input"] = user_input

    return render(request, "chatbot.html", context)
