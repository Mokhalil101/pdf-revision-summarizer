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

/* Dynamic Text Adjustment for Custom HTML elements */
.dynamic-title {
    text-align: center;
    font-weight: bold;
    margin-bottom: 10px;
}
.dynamic-box {
    padding: 20px;
    border-radius: 8px;
    border-left: 5px solid #89CFF0;
    background-color: rgba(137, 207, 240, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "processing" not in st.session_state:
    st.session_state.processing = False
if "summary_ready" not in st.session_state:
    st.session_state.summary_ready = False
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

        # Bound to Session State using 'key' to preserve file on view toggle
        uploaded_file = st.file_uploader(
            "Upload your PDF",
            type=["pdf"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            key="pdf_uploader"
        )

        # Progress bar and file details show ONLY when file exists in the native uploader
        if uploaded_file is not None:
            st.markdown("#### Uploaded File")

            file_size_mb = round(len(uploaded_file.getvalue()) / (1024 * 1024), 1)
            if file_size_mb == 0:
                file_size_mb = 0.1

            st.progress(100)
            st.markdown(
                f"<p style='color:#888888; font-size:14px; margin-top:-10px; margin-bottom:15px;'>"
                f"📄 <b>{uploaded_file.name}</b> ({file_size_mb} MB)"
                f"<span style='float:right;'>100%</span></p>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Summary length title
        st.markdown("<h4 class='dynamic-title'>Choose Summary Length</h4>", unsafe_allow_html=True)

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
                if st.session_state.pdf_uploader is not None:
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
        <div class='dynamic-box'>
            <p>• <b>Key Point 1:</b> The AI model has successfully extracted the main concept.</p>
            <p>• <b>Key Point 2:</b> Important definitions and core points are formatted for revision.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Back to Documents"):
            st.session_state.processing = False
            st.rerun()
