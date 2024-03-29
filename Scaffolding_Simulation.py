import streamlit as st
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

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

st.title("Scaffolding Practice Simulation")

col1, col2 = st.columns(2)
# UI for selecting vocabulary word and scaffold direction
chosen_vocab = col1.selectbox(
    "Vocabulary word:", options=list(extension_questions_dict.keys())
)
scaffold_direction = col2.selectbox(
    "Scaffold Direction:", ["Random", "Upward", "Downward"]
)

st.markdown(f"Copy Question:  \n**{extension_questions_dict[chosen_vocab]}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(extension_questions_dict[chosen_vocab]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
