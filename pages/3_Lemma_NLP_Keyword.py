import streamlit as st
import pandas as pd
import spacy

# Unused fun idea, but not useful

meaning_keywords_dict = {
    "wh_basic": ["who", "what", "when", "where", "which"],
    "why": ["why"],
    "how": ["how"],
    "sequence_temporal": [
        "first",
        "second",
        "third",
        "next",
        "last",
        "begin",
        "beginning",
        "middle",
        "end",
        "after",
        "earlier",
        "before",
        "final",
        "finally",
        "day",
        "yesterday",
        "today",
        "tomorrow",
        "time",
        "meantime",
        "sometime",
        "minute",
        "second",
        "morning",
        "daytime",
        "evening",
        "nighttime",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ],
    "compare_contrast": [
        "like",
        "likewise",
        "similar",
        "same",
        "different",
        "difference",
        "opposites",
        "contrast",
        "compare",
        "comparison",
        "alike",
        "not alike",
    ],
    "cognition": [
        "learn",
        "think",
        "know",
        "believe",
        "make believe",
        "plan",
        "pretend",
        "doubt",
        "marvel",
        "remember",
        "recall",
        "forget",
        "guess",
        "dream",
        "visualize",
        "imagine",
        "understand",
        "figure it out",
        "have in mind",
        "change mind",
        "realize",
        "consider",
        "come up with",
        "decide",
        "decision",
        "pick",
        "choice",
        "choose",
    ],
    "desires_preferences": [
        "dislike",
        "don’t like",
        "love",
        "fond",
        "keen",
        "enjoy",
        "want",
        "prefer",
        "favorite",
        "hate",
        "can’t stand",
        "hope",
        "wish",
    ],
    "feelings_emotions": [
        "feel",
        "feeling",
        "feelings",
        "emotion",
        "emotions",
        "happy",
        "joyful",
        "serene",
        "calm",
        "relaxed",
        "ecstatic",
        "glad",
        "gleeful",
        "proud",
        "confident",
        "sad",
        "grumpy",
        "pensive",
        "serious",
        "solemn",
        "grieving",
        "depressed",
        "lonely",
        "discouraged",
        "disappointed",
        "fear",
        "worried",
        "apprehensive",
        "scared",
        "afraid",
        "frightened",
        "terrified",
        "anxious",
        "concerned",
        "shy",
        "self-conscious",
        "embarrassed",
        "angry",
        "annoyed",
        "stressed",
        "overwhelmed",
        "frustrated",
        "upset",
        "irritated",
        "mad",
        "furious",
        "crabby",
        "contempt",
        "hatred",
        "aggressive",
        "jealous",
        "anticipation",
        "interested",
        "vigilant",
        "optimistic",
        "surprised",
        "excited",
        "startled",
        "dazed",
        "confused",
        "awe",
        "disgusted",
        "bored",
        "apathetic",
        "loathing",
        "remorseful",
        "sorry",
        "trusting",
        "admiration",
        "accepted",
        "secure",
        "loved",
        "thankful",
        "forgiven",
        "miss",
    ],
    "judgments_perspectives": [
        "mean",
        "nice",
        "boss",
        "bossy",
        "bossing",
        "compliant",
        "fair",
        "unfair",
        "fun",
        "boring",
        "beautiful",
        "ugly",
        "brave",
        "timid",
        "scaredy cat",
        "egotistic",
        "impulsive",
        "obedient",
        "risky",
        "agreeable",
        "cool",
        "amazing",
        "awesome",
        "friendly",
        "fancy",
        "intelligent",
        "smart",
        "stupid",
        "creative",
        "faithful",
        "dishonest",
        "honest",
        "loving",
        "nurturing",
        "important",
        "inferior",
        "respectful",
        "powerful",
        "successful",
        "bully",
        "Acceptable",
        "inadequate",
        "good",
        "bad",
        "okay",
        "best",
        "worst",
        "perfect",
        "wonderful",
        "horrible",
        "terrible",
        "disaster",
        "should",
        "supposed to",
        "must",
        "Agree",
        "disagree",
        "doesn’t make sense",
        "argue",
        "reject",
        "accept",
        "contend",
        "claim",
        "submit",
    ],
    "causaleffects_problemsolve": [
        "because",
        "‘cause",
        "cuz",
        "why",
        "since",
        "cause",
        "effect",
        "reason",
        "if-then",
        "if",
        "then",
        "solve",
        "solution",
        "problem",
        "challenge",
        "trouble",
        "dilemma",
        "conundrum",
        "work out",
        "resolve",
        "attempt",
        "fix",
        "mend",
        "repair",
    ],
    "predictions_forecast": [
        "expect",
        "anticipate",
        "will happen next",
        "could happen next",
    ],
}

# Set up NLP pipeline
nlp = spacy.load("en_core_web_sm")


def preprocess_keywords(keywords):
    """Lemmatize keywords."""
    return [nlp(keyword.lower())[0].lemma_ for keyword in keywords]


preprocessed_keywords_dict = {
    category: preprocess_keywords(keywords)
    for category, keywords in meaning_keywords_dict.items()
}


def preprocess_texts(texts):
    """Tokenize and lemmatize a list of texts using Spacy."""
    # Process the texts in batches for efficiency
    docs = list(nlp.pipe(texts))
    # Extract lemmatized tokens, avoiding punctuation and white spaces
    preprocessed_texts = [
        [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
        for doc in docs
    ]
    return preprocessed_texts


def contains_keywords_preprocessed(tokens, lemmatized_keywords):
    """Check if preprocessed tokens contain any of the lemmatized keywords."""
    return 1 if any(keyword in tokens for keyword in lemmatized_keywords) else "X"


# Keyword Coding Functions


def code_wh_basic_question(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["wh_basic"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_why_question(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["why"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_how_question(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["how"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


# Meaning Codes Functions
def code_sequence_temporal(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["sequence_temporal"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_compare_contrast(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["compare_contrast"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_cognition(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["cognition"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_desires_preferences(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["desires_preferences"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_feelings_emotions(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["feelings_emotions"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_judgments_perspectives(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["judgments_perspectives"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_causaleffects_problemsolve(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["causaleffects_problemsolve"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


def code_predictions_forecast(preprocessed_tokens):
    preprocessed_keywords = preprocessed_keywords_dict["predictions_forecast"]
    return contains_keywords_preprocessed(preprocessed_tokens, preprocessed_keywords)


# Define a dictionary mapping column name with their check function
form_code_functions = {
    "Wh- basic": code_wh_basic_question,
    "Why": code_why_question,
    "How": code_how_question,
}

meaning_code_functions = {
    "Sequence_Temporal": code_sequence_temporal,
    "Compare_Contrast": code_compare_contrast,
    "Cognition": code_cognition,
    "Desires_Preferences": code_desires_preferences,
    "Feelings_Emotions": code_feelings_emotions,
    "Judgments_Perspectives": code_judgments_perspectives,
    "CausalEffects_ProblemSolve": code_causaleffects_problemsolve,
    "Predictions_Forecast": code_predictions_forecast,
}

st.title("Keyword SABR Coding")
st.markdown("Check utterances for keywords and return a 1 for true and x for false")
st.markdown(
    "This uses a NLP library to break down each word into lemma and tags its part of speech then checks each word against a keyowrd lists. Very simple, and does not catch nuance."
)


uploaded_file = st.file_uploader("Choose an excel file")
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df["Utterance/Idea Units"] = df["Utterance/Idea Units"].fillna(
        ""
    )  # Fill empty cells with a space

    # Apply preprocessing to your DataFrame's utterances
    df["Preprocessed"] = preprocess_texts(df["Utterance/Idea Units"].str.lower())

    # Let users choose which form codes to apply
    selected_form_codes = st.multiselect(
        "Select form codes to apply:",
        options=list(form_code_functions.keys()),
    )
    # Let users choose which meaning codes to apply
    selected_meaning_codes = st.multiselect(
        "Select meaning codes to apply:",
        options=list(meaning_code_functions.keys()),
    )

    # Apply coding functions to preprocessed data
    for code_name in selected_form_codes:
        code_function = form_code_functions[code_name]
        df[code_name] = df["Preprocessed"].apply(code_function)

    for code_name in selected_meaning_codes:
        code_function = meaning_code_functions[code_name]
        df[code_name] = df["Preprocessed"].apply(code_function)

    # Display the DataFrame in the app
    st.dataframe(df)

    # Remove the 'Preprocessed' column before downloading
    download_df = df.drop(columns=["Preprocessed"])

    # Convert DataFrame to CSV for downloading
    csv = download_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download coded data as CSV",
        data=csv,
        file_name="coded_data.csv",
        mime="text/csv",
    )
