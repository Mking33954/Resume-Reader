import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("About this app")
st.write("This app reads PDF and DOCX resumes, extracts text, finds skills, and summarizes experience.")

st.subheader("Features")
st.markdown(
    """
    - PDF upload support.
    - DOCX upload support.
    - Skills extraction.
    - Experience summarization.
    - Section breakdown.
    - JSON and CSV export.
    """
)
