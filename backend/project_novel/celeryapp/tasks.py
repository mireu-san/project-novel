from celery import shared_task
import openai
import os


@shared_task
def process_openai_request(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
    )
    return response['choices'][0]['text'].strip()
