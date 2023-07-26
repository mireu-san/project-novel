from django.shortcuts import render

# Create your views here.

# OpenAI - chatGPT
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()