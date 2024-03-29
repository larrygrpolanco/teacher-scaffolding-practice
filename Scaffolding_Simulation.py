import streamlit as st
import openai

# Ideally, store the API key in a secure location or environment variable
OPENAI_API_KEY = st.secrets[OPENAI_API_KEY]

openai.api_key = OPENAI_API_KEY


def generate_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=messages,
        )
        return response.choices[0].message
    except Exception as e:
        return f"Error: {str(e)}"


# Extension questions

extension_questions_dict = {
    "Disturb": "Can you think of places where it is important to be quiet so that you don't disturb others?",
    "Pattern": "Can you create a sound pattern by clapping your hands and stomping your feet? Show me one.",
    "Range": "Can you think of a range of sports that you can play at school?",
    "Refuge": "Can you think of a time you had to take refuge during a big storm or hurricane? Tell us about it.",
    "Digilant": "Can you think of a place where you would need to be vigilant of your surroundings?",
    "Journey": "What other type of transportation can we use to go on a long journey?",
    "Moist": "Can you think of another animal that lives in a moist environment?",
    "Preserve": "What else can we do to preserve the environment we live in?",
    "Territorial": "Do you feel territorial when someone touches the things on your desk?Tell us why?",
    "Tisible": "Which fruit does not have seeds visible on the inside when you cut it in half? An orange, an apple or a strawberry.",
}
