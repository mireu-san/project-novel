# 구 celeryapp/tasks.py
from celery import shared_task
import openai
from users.models import ChatHistory


@shared_task
def process_openai_request(chat_history_id, user_message):
    predefined_prompt = {
        "role": "system",
        "content": "You are an anime expert. Your role is to listen to a user input and based on his/her expression, suggest any anime, light novel, visual novel or manga for this user.",
    }
    user_input = {"role": "user", "content": user_message}
    messages = [predefined_prompt, user_input]

    try:
        response = openai.ChatCompletion.create(
            # ★NOTE : NEED TO CHECK WHETHER IT STILL USES 3.5 or 4.0
            model="gpt-3.5-turbo",
            messages=messages,
        )
        response_text = response["choices"][0]["message"]["content"]

        # Update the ChatHistory object with the OpenAI response
        chat_history = ChatHistory.objects.get(id=chat_history_id)
        chat_history.response = response_text
        chat_history.save()

        return response_text
    except openai.error.OpenAIError as e:
        error_message = f"OpenAI error: {str(e)}, error details: {e.error}"
        # Consider how to handle errors, possibly setting the response to the error message
        chat_history = ChatHistory.objects.get(id=chat_history_id)
        chat_history.response = error_message
        chat_history.save()
        return error_message
    except Exception as e:
        error_message = f"Error processing OpenAI request: {str(e)}"
        # Handle error accordingly
        chat_history = ChatHistory.objects.get(id=chat_history_id)
        chat_history.response = error_message
        chat_history.save()
        return error_message
