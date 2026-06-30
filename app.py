import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="AI PDF Summarizer", layout="centered")

# Custom CSS for styling the application elements
st.markdown("""
<style>
/* Main action button (Generate Summary) */
div.stButton > button:first-child {
    border: 2px solid #89CFF0;
    color: #89CFF0;
    background-color: transparent;
    border-radius: 8px;
    padding: 0.5rem 2rem;
    font-weight: bold;
}
div.stButton > button:first-child:hover {
    background-color: #89CFF0;
    color: white;
}

/* Typography */
h3, h4 {
    color: #31333F;
    font-family: 'sans serif';
}

/* Delete (X) button */
div.stButton > button[id^="del_"] {
    background-color: transparent !important;
    border: none !important;
    color: #A0AAB2 !important;
    font-size: 14px !important;
    padding: 0px !important;
    margin: 0px !important;
    min-height: unset !important;
    height: auto !important;
    line-height: 1 !important;
    box-shadow: none !important;
}
div.stButton > button[id^="del_"]:hover {
    color: #E74C3C !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "processing" not in st.session_state:
    st.session_state.processing = False
if "summary_ready" not in st.session_state:
    st.session_state.summary_ready = False
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []
if "selected_length" not in st.session_state:
    st.session_state.selected_length = "Medium"

# Placeholder
main_placeholder = st.empty()

# =========================
# View 1: Upload Page
# =========================
if not st.session_state.processing:
    with main_placeholder.container():
        st.markdown("### 📚 AI powered PDF summarizer")

        # File uploader
        uploaded_files = st.file_uploader(
            "Upload your PDF",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

        # Sync uploaded files
        if uploaded_files:
            for f in uploaded_files:
                if f.name not in [existing_f.name for existing_f in st.session_state.uploaded_files_list]:
                    st.session_state.uploaded_files_list.append(f)

        # Uploaded files list
        if st.session_state.uploaded_files_list:
            st.markdown("<h4 style='color:#89CFF0;'>Uploaded Files</h4>", unsafe_allow_html=True)

            for file in st.session_state.uploaded_files_list:
                file_size_mb = round(len(file.getvalue()) / (1024 * 1024), 1)
                if file_size_mb == 0:
                    file_size_mb = 10.0

                st.progress(100)
                st.markdown(
                    f"<p style='color:gray; font-size:14px; margin-top:-10px; margin-bottom:15px;'>"
                    f"📄 <b>{file.name}</b> ({file_size_mb} MB)"
                    f"<span style='float:right;'>100%</span></p>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Summary length title
        st.markdown(
            "<h4 style='text-align:center; color:#89CFF0;'>Choose Summary Length</h4>",
            unsafe_allow_html=True
        )

        # Summary length tabs
        col_s, col_m, col_l = st.columns(3)

        def summary_tab(label):
            selected = st.session_state.selected_length == label
            color = "#6CB4EE" if selected else "#EAF6FF"
            text_color = "white" if selected else "#6CB4EE"

            if selected:
                st.markdown(
                    f"""
                    <button style='
                    width:100%;
                    background-color:{color};
                    color:{text_color};
                    border:none;
                    padding:10px;
                    border-radius:20px;
                    font-weight:bold;
                    '>{label}</button>
                    """,
                    unsafe_allow_html=True
                )
            else:
                if st.button(label, use_container_width=True):
                    st.session_state.selected_length = label
                    st.rerun()

        with col_s:
            summary_tab("Short")
        with col_m:
            summary_tab("Medium")
        with col_l:
            summary_tab("Detailed")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate Summary", use_container_width=True):
                if st.session_state.uploaded_files_list:
                    st.session_state.processing = True
                    st.session_state.summary_ready = False
                    st.rerun()
                else:
                    st.warning("⚠️ Please upload a PDF file first before generating the summary!")

# =========================
# View 2: Processing + Result
# =========================
else:
    with main_placeholder.container():
        st.markdown("### 📚 AI powered PDF summarizer")

        if not st.session_state.summary_ready:
            with st.spinner("Extracting text and generating your summary... Please wait."):
                import time
                time.sleep(3)
            st.session_state.summary_ready = True
            st.rerun()

        st.success("Summary generated successfully!")
        st.subheader(f"{st.session_state.selected_length} Summary Output")

        st.markdown(f"""
        <div style='
        background-color:#FFFFFF;
        padding:20px;
        border-radius:8px;
        border-left:5px solid #89CFF0;
        '>
            <p style='color:#31333F;'>• <b>Key Point 1:</b> The AI model has successfully extracted the main concept.</p>
            <p style='color:#31333F;'>• <b>Key Point 2:</b> Important definitions and core points are formatted for revision.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Back to Documents"):
            st.session_state.processing = False
            st.rerun()
