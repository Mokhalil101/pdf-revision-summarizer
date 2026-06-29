import streamlit as st

st.set_page_config(page_title="PDF Revision Summarizer", layout="centered")

st.title("📄 PDF Revision Summarizer")
st.write("Upload your academic PDF and get a smart revision-focused summary.")

pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

summary_length = st.selectbox(
    "Select summary length",
    ["Short", "Medium", "Detailed"]
)

if st.button("Generate Summary"):
    if pdf_file is None:
        st.error("❌ Please upload a PDF file first.")
    else:
        with st.spinner("Summarizing..."):
            # Dummy summary for now
            st.subheader("📌 Key Concepts")
            st.write("- Artificial Intelligence\n- Machine Learning\n- Deep Learning")

            st.subheader("📘 Definitions")
            st.write("AI: The simulation of human intelligence in machines.")

            st.subheader("⭐ Important Points")
            st.write("• Useful for exam revision\n• Saves study time")
