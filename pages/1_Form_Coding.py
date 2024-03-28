import streamlit as st
import pandas as pd
import time
from chatgpt_coder import ChatGPTCoder

# Initialize the ChatGPTCoder with your OpenAI API key
gpt_coder = ChatGPTCoder(st.secrets["OPENAI_API_KEY"])


st.title("Auto SABR Coding")
st.markdown("Prototype app for testing automatic SABR coding using LLMs.")


# File uploader widget
uploaded_file = st.file_uploader("Choose an Excel file")
if uploaded_file is not None:
    # Check file extension
    if not uploaded_file.name.endswith(".xlsx") and not uploaded_file.name.endswith(
        ".xls"
    ):
        st.error("Unsupported file format! Please upload an Excel file.")
    else:
        df = pd.read_excel(uploaded_file)

    # Convert every column into a string for consistent processing
    for column in df.columns:
        df[column] = df[column].astype(str)

    # Display the DataFrame for the user to review
    st.dataframe(df)

    form_code_options = [
        "Comment",
        "Directive",
        "Question",
    ]
    selected_form_codes = st.multiselect(
        "Select the form codes to apply:", form_code_options, default=form_code_options
    )

    question_code_options = [
        "Single Word",
        "Multiple Words",
        "Wh- basic",
        "Why",
        "How"
        "Auxiliary-fronted",
        "Yes/No",
        "Real",
        "Test",
    ]
    selected_question_codes = st.multiselect(
        "Select the question codes to apply:", question_code_options, default=question_code_options
    )

    child_code_options = [
        "Child Singe Word",
        "Child Multiple Word",
    ]
    selected_child_codes = st.multiselect(
        "Select the child codes to apply:", child_code_options, default=child_code_options
    )


code_method_mapping = {
    "Comment": gpt_coder.code_comment,
    "Directive": gpt_coder.code_directive,
    "Question": gpt_coder.code_question,
}

# Toggle for explanations
include_explanations = st.checkbox("Include explanations with codes")


# Button to start coding process
if st.button("Apply Coding"):
    start_time = time.time()
    with st.spinner("Coding in progress... Please wait."):
        for i, row in df.iterrows():
            utterance = row["Utterance/Idea Units"]

            for form_code in selected_form_codes:
                # Get the corresponding coding method based on the selected form code
                if form_code in code_method_mapping:
                    code_method = code_method_mapping[form_code]
                    code_response, explanation = code_method(utterance)
                    df.at[i, form_code] = code_response  # Use form_code as column name
                    if include_explanations:
                        df.at[i, f"{form_code} Explanation"] = explanation



        end_time = time.time()
        st.success(f"Coding completed in {end_time - start_time:.2f} seconds.")

    # Display the updated DataFrame
    st.dataframe(df)
