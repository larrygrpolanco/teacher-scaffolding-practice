import openai


class ChatGPTCoder:
    def __init__(self, openai_api_key):
        self.client = openai.OpenAI(api_key=openai_api_key)
        openai.api_key = openai_api_key


extension_questions_dict = {
    "disturb": "Can you think of places where it is important to be quiet so that you don't disturb others?",
    "pattern": "Can you create a sound pattern by clapping your hands and stomping your feet? Show me one.",
    "range": "Can you think of a range of sports that you can play at school?",
    "refuge": "Can you think of a time you had to take refuge during a big storm or hurricane? Tell us about it.",
    "vigilant": "Can you think of a place where you would need to be vigilant of your surroundings?",
    "journey": "What other type of transportation can we use to go on a long journey?",
    "moist": "Can you think of another animal that lives in a moist environment?",
    "preserve": "What else can we do to preserve the environment we live in?",
    "territorial": "Do you feel territorial when someone touches the things on your desk?Tell us why?",
    "visible": "Which fruit does not have seeds visible on the inside when you cut it in half? An orange, an apple or a strawberry.",
}
