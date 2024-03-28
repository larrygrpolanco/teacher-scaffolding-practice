import streamlit as st
import pandas as pd


def load_dataframe(file):
    """Load a dataframe from a file upload."""
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if file type is unknown


def calculate_agreement(df1, df2, columns_to_compare):
    """Calculate agreement percentage for the selected columns."""
    agreement_results = {}
    for col in columns_to_compare:
        non_null_mask = ~df1[col].isnull() & ~df2[col].isnull()
        if non_null_mask.sum() > 0:
            agreement = (
                (df1[col] == df2[col]) & non_null_mask
            ).sum() / non_null_mask.sum()
            agreement_results[col] = agreement * 100  # Convert to percentage
        else:
            agreement_results[col] = None  # No data to compare
    return agreement_results


def highlight_disagreements(row, df2, columns_to_compare):
    """Highlight cells where values don't match."""
    disagreement_style = []
    for col in row.index:
        if col in columns_to_compare and row[col] != df2.at[row.name, col]:
            disagreement_style.append("background-color: yellow")
        else:
            disagreement_style.append("")
    return disagreement_style


st.title("Coding Agreement")


# File uploaders in an expander
with st.sidebar.expander("Load CSV files"):
    file1 = st.file_uploader(
        "Choose the first spreadsheet file", key="file1", type=["csv", "xlsx"]
    )
    file2 = st.file_uploader(
        "Choose the second spreadsheet file", key="file2", type=["csv", "xlsx"]
    )
    if file1 and file2:
        st.session_state["df1"] = load_dataframe(file1)
        st.session_state["df2"] = load_dataframe(file2)
        st.success("Data loaded. You can minimize this box.")

if "df1" in st.session_state and "df2" in st.session_state:
    df1 = st.session_state["df1"]
    df2 = st.session_state["df2"]
    common_columns = df1.columns.intersection(df2.columns)

    # Use an expander to hold the checklist
    with st.sidebar.expander("Select columns to compare"):
        columns_to_compare = []
        for column in common_columns:
            # Create a checkbox for each common column
            if st.checkbox(column, key=column):
                columns_to_compare.append(column)

    if st.button("Calculate Agreement"):
        if df1.shape[0] == df2.shape[0]:
            agreement_results = calculate_agreement(df1, df2, columns_to_compare)
            st.session_state["agreement_results"] = agreement_results
            st.session_state["show_df1"] = False
            st.session_state["show_df2"] = False
        else:
            st.error(
                "The files do not have the same number of rows and cannot be directly compared for agreement."
            )

    if "agreement_results" in st.session_state:
        display_agreement = pd.DataFrame(
            list(st.session_state["agreement_results"].items()),
            columns=["Column", "Agreement (%)"],
        )
        st.dataframe(display_agreement)

    if st.button("Show First Spreadsheet"):
        st.session_state["show_df1"] = True
        st.session_state["show_df2"] = False

    if st.button("Show Second Spreadsheet"):
        st.session_state["show_df2"] = True
        st.session_state["show_df1"] = False

    if st.session_state.get("show_df1"):
        df1_style = df1.style.apply(
            highlight_disagreements,
            df2=df2,
            columns_to_compare=columns_to_compare,
            axis=1,
        )
        st.caption("First Spreadsheet")
        st.dataframe(df1_style)

    if st.session_state.get("show_df2"):
        df2_style = df2.style.apply(
            highlight_disagreements,
            df2=df1,
            columns_to_compare=columns_to_compare,
            axis=1,
        )
        st.caption("Second Spreadsheet")
        st.dataframe(df2_style)
