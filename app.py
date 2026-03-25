import streamlit as st

from resume_parser import (
    save_uploaded_file,
    parse_resume_file,
    results_to_json,
    results_to_csv,
)

st.set_page_config(page_title="Resume Reader", page_icon="📄", layout="wide")

st.title("Resume Reader")
st.write("Upload a PDF or DOCX resume to extract skills, summarize experience, and export results.")

uploaded_file = st.file_uploader("Upload a resume", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume..."):
            temp_path = save_uploaded_file(uploaded_file)
            result = parse_resume_file(temp_path)

        skills = result.get("skills", [])
        sections = result.get("sections", {})
        experience_summary = result.get("experience_summary", [])
        experience_blocks = result.get("experience_blocks", [])
        stats = result.get("stats", {})
        ocr_used = result.get("ocr_used", False)

        with st.sidebar:
            st.header("Resume Stats")
            st.metric("Skills", stats.get("skills_count", len(skills)))
            st.metric("Sections", stats.get("sections_count", len(sections)))
            st.metric("Experience Lines", stats.get("experience_lines", len(experience_summary)))
            st.metric("Words", stats.get("word_count", 0))
            st.metric("Experience Blocks", stats.get("experience_blocks_count", len(experience_blocks)))
            st.write("OCR Used:", "Yes" if ocr_used else "No")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Skills")
            if result["skills"]:
                st.write(", ".join(result["skills"]))
            else:
                st.write("No skills found.")

            st.subheader("Section Breakdown")
            if sections:
                for section_name, section_text in sections.items():
                    with st.expander(section_name.title(), expanded=False):
                        st.write(section_text)
            else:
                st.write("No sections detected.")

        with c2:
            st.subheader("Work Experience Summary")
            if experience_summary:
                for item in experience_summary:
                    st.markdown(f"- {item}")
            else:
                st.write("No experience summary found.")

            st.subheader("Experience Blocks")
            if experience_blocks:
                for block in experience_blocks:
                    with st.expander(block["title"], expanded=False):
                        st.write(block["content"])
            else:
                st.write("No experience blocks found.")

        st.subheader("Raw Text Preview")
        st.text_area("Resume text", result.get("raw_text", ""), height=320)

        json_data = results_to_json(result)
        csv_data = results_to_csv(result)

        st.subheader("Download Results")
        d1, d2 = st.columns(2)

        with d1:
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="resume_analysis.json",
                mime="application/json",
            )

        with d2:
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="resume_analysis.csv",
                mime="text/csv",
            )

