import streamlit as st
import random
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def begin_scaffold(prompt, direction):
    if direction == "Upward":
        scaffold_direction_instruction = "Assist the teacher practice upward scaffolding by answering the question correctly as a 4th grader"
    else:
        scaffold_direction_instruction = "Assist the teacher practice upward scaffolding by answering the question incorrectly as a 4th grader"

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"You will simulate 4th grader student in a 1 on 1 vocabular lesson. This excersise is meant to give teachers pracice with scaffolding. {scaffold_direction_instruction} Remember, your role is strictly the student’s; wait for the user response before moving forward with the simulation",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def continue_scaffold(prompt, chat_history):
    messages = chat_history + [
        {"role": "user", "content": prompt}
    ]  # Append the latest user message to the history
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You will simulate 4th grader student in a 1 on 1 vocabular lesson. This excersise is meant to give teachers pracice with scaffolding. After, conclude by giving the user feedback on their use of scaffolding techniques. Offer specific insights on how effectively I employed upward and downward scaffolding strategies and suggest areas for improvement.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
        )
        return response.choices[0].message.content
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

if scaffold_direction == "Random":
    scaffold_direction = random.choice(["Upward", "Downward"])

st.markdown(f"Copy Question:  \n**{extension_questions_dict[chosen_vocab]}**")

if st.button("Restart"):
    st.session_state.messages = []
    st.session_state.used_begin_scaffold = False  # Reset the flag on restart
    st.experimental_rerun()


# Initialize session state variables if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
if "used_begin_scaffold" not in st.session_state:
    st.session_state.used_begin_scaffold = False  # Track the first usage begin_scaffold


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(extension_questions_dict[chosen_vocab]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Decide which function to use based on whether begin_scaffold has been used
            if not st.session_state.used_begin_scaffold:
                response = begin_scaffold(prompt=prompt, direction=scaffold_direction)
                st.session_state.used_begin_scaffold = (
                    True  # Mark that begin_scaffold has been used
                )
            else:
                # Assuming continue_scaffolding takes the ongoing chat as input
                response = continue_scaffold(
                    prompt=prompt,
                    chat_history=continue_scaffold(st.session_state.messages),
                )

            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
