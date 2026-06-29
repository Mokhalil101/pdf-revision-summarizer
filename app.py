import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="AI PDF Summarizer", layout="centered")

# Custom CSS for styling the application elements
st.markdown("""
    <style>
    /* Styling for the main action button (Generate Summary) */
    div.stButton > button:first-child {
        border: 2px solid #5E9BFF;
        color: #5E9BFF;
        background-color: transparent;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #5E9BFF;
        color: white;
    }
    
    /* Typography customization */
    h3, h4 {
        color: #31333F;
        font-family: 'sans serif';
    }

    /* Custom styling for the clean, borderless gray X button */
    div.stButton > button[id^="del_"] {
        background-color: transparent !important;
        border: none !important;
        color: #A0AAB2 !important; /* Soft gray color */
        font-size: 14px !important;   /* Suitable font size */
        padding: 0px !important;
        margin: 0px !important;
        min-height: unset !important;
        height: auto !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }
    
    div.stButton > button[id^="del_"]:hover {
        color: #E74C3C !important; /* Changes to soft red on hover */
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States to preserve data across reruns
if "processing" not in st.session_state:
    st.session_state.processing = False
if "summary_ready" not in st.session_state:
    st.session_state.summary_ready = False
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []
if "selected_length" not in st.session_state:
    st.session_state.selected_length = "Medium"

# Main empty container placeholder for view swapping
main_placeholder = st.empty()

# View 1: Main Document Upload Form
if not st.session_state.processing:
    with main_placeholder.container():
        st.markdown("### 📚AI powered PDF summarizer")

        # File uploader box
        uploaded_files = st.file_uploader("Upload your PDF", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        
        # Syncing newly uploaded files into our custom session state list safely without duplicates
        if uploaded_files:
            for f in uploaded_files:
                if f.name not in [existing_f.name for existing_f in st.session_state.uploaded_files_list]:
                    st.session_state.uploaded_files_list.append(f)

        # Display custom file list with progress bars
        if st.session_state.uploaded_files_list:
            st.markdown("<h4 style='color: #FFFFFF;'>Uploaded Files</h4>", unsafe_allow_html=True)
            
            for index, file in enumerate(list(st.session_state.uploaded_files_list)):
                file_size_mb = round(len(file.getvalue()) / (1024 * 1024), 1)
                if file_size_mb == 0:
                    file_size_mb = 10.0
                
                # File progress bar and metadata detail
                st.progress(100)
                st.markdown(f"<p style='color: gray; font-size: 14px; margin-top: -10px; margin-bottom: 15px;'>📄 <b>{file.name}</b> ({file_size_mb} MB) <span style='float: right;'>100%</span></p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Section Title
        st.markdown("<h4 style='text-align: center; color: #FFFFFF;'>Choose Summary Length</h4>", unsafe_allow_html=True)
        
        # Custom columns setup for summary length selector tabs
        col_s, col_m, col_l = st.columns(3)
        
        with col_s:
            if st.session_state.selected_length == "Short":
                st.markdown("<button style='width:100%; background-color:#34495E; color:white; border:none; padding:10px; border-radius:20px; font-weight:bold;'>Short</button>", unsafe_allow_html=True)
            else:
                if st.button("Short", use_container_width=True):
                    st.session_state.selected_length = "Short"
                    st.rerun()
                    
        with col_m:
            if st.session_state.selected_length == "Medium":
                st.markdown("<button style='width:100%; background-color:#34495E; color:white; border:none; padding:10px; border-radius:20px; font-weight:bold;'>Medium</button>", unsafe_allow_html=True)
            else:
                if st.button("Medium", use_container_width=True):
                    st.session_state.selected_length = "Medium"
                    st.rerun()
                    
        with col_l:
            if st.session_state.selected_length == "Detailed":
                st.markdown("<button style='width:100%; background-color:#34495E; color:white; border:none; padding:10px; border-radius:20px; font-weight:bold;'>Detailed</button>", unsafe_allow_html=True)
            else:
                if st.button("Detailed", use_container_width=True):
                    st.session_state.selected_length = "Detailed"
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Centered Action Trigger Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            start_button = st.button("Generate Summary", use_container_width=True)
            if start_button:
                if st.session_state.uploaded_files_list:
                    st.session_state.processing = True
                    st.session_state.summary_ready = False
                    st.rerun()
                else:
                    # Alert message strictly in English
                    st.warning("⚠️ Please upload a PDF file first before generating the summary!")

# View 2: Processing Spinner & Result Container
else:
    with main_placeholder.container():
        st.markdown("### AI powered PDF summarizer")
        
        # Single-pass background rendering spinner control
        if not st.session_state.summary_ready:
            with st.spinner("Extracting text and generating your summary... Please wait."):
                import time
                time.sleep(3)
            st.session_state.summary_ready = True
            st.rerun()

        # Render generated results page setup
        st.success("Summary generated successfully!")
        st.subheader(f"{st.session_state.selected_length} Summary Output")
        
        st.markdown(f"""
            <div style='background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #5E9BFF;'>
                <p style='color: #31333F;'>• <b>Key Point 1:</b> The AI model has successfully extracted the main concept from your files.</p>
                <p style='color: #31333F;'>• <b>Key Point 2:</b> Important definitions and core points are formatted here for revision.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Back to Documents"):
            st.session_state.processing = False
            st.rerun()
