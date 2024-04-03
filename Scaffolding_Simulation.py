import streamlit as st
import random
import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def begin_scaffold(prompt, direction):
    # Clarifying the scaffolding direction in the instruction.
    if direction == "Upward":
        scaffold_direction_instruction = "Assist the teacher in practicing upward scaffolding by responding correctly as if you were a 4th-grade student. \
            This means you should show understanding of the vocabulary word, allowing the teacher to introduce more complex or related concepts."
    else:  # Assuming the alternative direction is downward for simplification.
        scaffold_direction_instruction = "Assist the teacher in practicing downward scaffolding by responding incorrectly as if you were a 4th-grade student. \
            This indicates a need for the teacher to simplify the concept or provide more foundational support to help you understand the vocabulary word."

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"In this exercise, you'll simulate a 4th grader in a one-on-one vocabulary lesson, designed to give teachers practice with scaffolding techniques. \
                    {scaffold_direction_instruction} \
                    Remember, your role is strictly that of the student; wait for the instructor's (user's) response before proceeding with the simulation.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def continue_scaffold(prompt, chat_history):
    try:
        # Start with the system message
        messages = [
            {
                "role": "system",
                "content": "You will continue to simulate a 4th grader in a one-on-one vocabulary lesson. This exercise is meant to give teachers practice with scaffolding. \
                Based on your previous interactions, if you feel the teacher has effectively built upon your understanding, provide a correct answer. \
                If the explanation or question seems confusing or too complex, indicate misunderstanding or provide an incorrect response. \
                Remember, your role is strictly that of the student; evaluate the teacher's last message to decide your response.",
            }
        ]

        # Extend the messages list with the entire chat_history
        messages.extend(chat_history)

        # Append the final user's prompt
        messages.append({"role": "user", "content": prompt})

        # Make the call to the API with the constructed messages list
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=200,
        )

        print(messages)  # debugging

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def assess_scaffolding(chat_history, direction):
    try:
        # Start with the system message
        messages = [
            {
                "role": "system",
                "content": f"Your task is to review the conversation and provide the instructor with feedback on their {direction} scaffolding techniques. \
                Analyze how effectively they employed {direction} scaffolding strategies. \
                Offer balanced feedback, highlighting strengths and identifying areas for improvement with clear, actionable suggestions.",
            }
        ]

        # Extend the messages list with the entire chat_history
        messages.extend(chat_history)

        # Append the final user's prompt
        messages.append(
            {
                "role": "user",
                "content": "Please review my scaffolding in this session. Provide feedback on what I did that was effective and what could be improved, keep this short and do it in 3 bullet points one sentece each.",
            }
        )

        # Make the call to the API with the constructed messages list
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=1000,
        )

        print(messages)  # debugging

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# Extension questions

extension_questions_dict = {
    "Disturb": "Can you think of places where it is important to be quiet so that you don't disturb others?",
    "Pattern": "Can you create a sound pattern by clapping your hands and stomping your feet? Show me one.",
    "Range": "Can you think of a range of sports that you can play at school?",
    "Refuge": "Can you think of a time you had to take refuge during a big storm or hurricane? Tell us about it.",
    "Vigilant": "Can you think of a place where you would need to be vigilant of your surroundings?",
    "Journey": "What other type of transportation can we use to go on a long journey?",
    "Moist": "Can you think of another animal that lives in a moist environment?",
    "Preserve": "What else can we do to preserve the environment we live in?",
    "Territorial": "Do you feel territorial when someone touches the things on your desk?Tell us why?",
    "Visible": "Which fruit does not have seeds visible on the inside when you cut it in half? An orange, an apple or a strawberry.",
}

up_scaffold_examples = {
    "Disturb": "Why is it important to be quiet in the library?  \nWhat are other places where it is important to be quiet and not disturb others?  \nWhat will happen if you are not quiet at church?",
    "Pattern": "Can you think of a pattern using colors?  \nWhat makes it a pattern?",
    "Range": "Are you good at it? Why?  \nWhat is your favorite sport?  \nWhat is your favorite sports team?  \nWhy are they a pattern?",
    "Refuge": "How did you take refuge from the hurricane?  \nHow did you prepare for the storm?  \nHow did you feel during that time?  \nWhere did you go? Why was this a safe refuge?  \nWhat are some school drills that show you how to take refuge?",
    "Vigilant": "What do you need to do before crossing the street?  \nWhy is it important to be vigilant when crossing the street?  \nHow are you vigilant when playing outside in your neighborhood?  \nWhat are some ways you can be vigilant?",
    "Journey": "Can you think of another type of transportation we can use for a long journey?  \nHave you ever been to a journey using that form of transportation? Where did you go? How was it?  \nHow would you prepare for a long journey in a car (or other response)?",
    "Moist": "Can you think of another animal that lives in a moist environment?  \nWhy do you think they live in a moist environment?  \nHow do you think it helps to have wet skin?",
    "Preserve": "How would you clean the ocean?  \nCan you think of something else we can do to preserve the environment?  \nDo you recycle at home or school? How do you do it?  \nWhat kinds of things can you recycle?  \nWhy is important to not-litter?",
    "Territorial": "What is something else you feel territorial about?  \nWhat would you say to someone who touches your thing on your desk?  \nCan you think of anything else you are territorial about?",
    "Visible": "Can you think of a fruit or vegetable that DOES have seeds visible on the inside when you cut in half?  \nWhere does strawberries have their visible seeds?",
}

down_scaffold_examples = {
    "Disturb": "Do you think it is important to be quiet in the library or the playground (park)?",
    "Pattern": "Having child choose between a pattern or no pattern example.",
    "Range": "What is a range of sports you can play at school…Soccer and football or painting and drawing?  \nWhat is a range of sports you guys play in PE…basket weaving or basketball?",
    "Refuge": "During a big storm or hurricane where did you take refuge, at home or did you have to evacuate (leave)?  \nDuring a hurricane…would you rather leave Florida or hide under a palm tree?",
    "Vigilant": "Which place would you need to be vigilant of your surroundings…the park or your home?  \n…playing outside or doing laundry?",
    "Journey": "What type of transportation can we use to go on a long journey…airplane or train (bicycle)?",
    "Moist": "What animal lives in a moist environment  \n…an alligator or a goat?",
    "Preserve": "What can we do to preserve the environment we live in?  \nRecycle or throw trash on the ground?",
    "Territorial": "If someone touches the things on your desks making you feel territorial that means you are upset or happy?  \nWould you feel territorial about someone touching your pencils or notebooks?",
    "Visible": "A fruit that does not have seeds visible on the inside would be a banana or apple?",
}

st.title("Scaffolding Practice Simulation")
st.caption("Week 5")

col1, col2 = st.columns(2)
# UI for selecting vocabulary word and scaffold direction
chosen_vocab = col1.selectbox(
    "Vocabulary word:", options=list(extension_questions_dict.keys())
)

scaffold_direction = col2.selectbox(
    "Scaffold Direction:", ["Random", "Upward", "Downward"]
)

if scaffold_direction == "Random":
    # Check if a random choice has already been made
    if "random_scaffold_direction" not in st.session_state:
        # If not, make a new random choice and store it in the session state
        st.session_state.random_scaffold_direction = random.choice(["Upward", "Downward"])
    # Use the stored random choice
    scaffold_direction = st.session_state.random_scaffold_direction
else:
    # If the user selects a specific direction, clear the random choice from the session state
    if "random_scaffold_direction" in st.session_state:
        del st.session_state.random_scaffold_direction
(
    col3,
    col4,
) = st.columns(2)

# if col3.button("Review", help="Still a work in progress."):
#     with st.spinner("Reviewing..."):
#         # Call assess_scaffolding with the current conversation
#         assess_scaffolding_response = assess_scaffolding(
#             chat_history=st.session_state.messages, direction=scaffold_direction
#         )

#     # Here you should extract the response content from the assess_scaffolding_response
#     # and display it or process it as needed. For this example, let's just print it.
#     if assess_scaffolding_response:
#         assessment_content = assess_scaffolding_response  # Simplification: actual extraction depends on API response structure
#         st.session_state.messages.append(
#             {"role": "system", "content": assessment_content}
#         )

if col3.button("Restart"):
    st.session_state.messages = []
    st.session_state.used_begin_scaffold = False  # Reset the flag on restart
    st.rerun()


with col4.expander("Scaffolding Hints:"):
    if scaffold_direction == "Upward":
        hint_examples = up_scaffold_examples[chosen_vocab]
    else:
        hint_examples = down_scaffold_examples[chosen_vocab]
    st.caption(f"**{scaffold_direction} Examples**  \n {hint_examples}")

st.caption(f"Extension Question:  \n**{extension_questions_dict[chosen_vocab]}**")

# Initialize session state variables if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
if "used_begin_scaffold" not in st.session_state:
    st.session_state.used_begin_scaffold = False  # Track the first usage begin_scaffold


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Copy and paste extension question here."):
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
                    prompt=prompt, chat_history=st.session_state.messages
                )

            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
