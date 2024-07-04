import streamlit as st
import pandas as pd
import time
from PIL import Image
import base64
import random
import numpy as np
import plotly.graph_objects as go

# Set page config at the very beginning
st.set_page_config(layout="wide")

# Function to generate a light, pastel color
def generate_pastel_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

# Function to display PDF preview
def display_pdf(pdf_path):
    try:
        st.write(f"PDF: {pdf_path.split('/')[-1]}")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64.b64encode(open(pdf_path, "rb").read()).decode()}" width="100%" height="800" type="application/pdf"></iframe>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")

# Function to create a message box with unique color and adjusted icon
def create_message_box(role, message, icon_path):
    message_placeholder = st.empty()
    full_text = ""
    background_color = generate_pastel_color()
    
    message_placeholder.markdown(
        f"""
        <div style="background-color: {background_color}; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-height: 120px;">
            <img src="data:image/png;base64,{get_image_base64(icon_path)}" style="width:80px; height:100px; float:left; margin-right:15px; border-radius: 50%; object-fit: cover;">
            <div style="margin-left: 115px; color: black;">
                <strong style="font-size: 18px;">{role}</strong><br>
                <span style="font-size: 16px;">Thinking...</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(0.1)  # Reduced thinking time
    
    for char in message:
        full_text += char
        message_placeholder.markdown(
            f"""
            <div style="background-color: {background_color}; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-height: 120px;">
                <img src="data:image/png;base64,{get_image_base64(icon_path)}" style="width:80px; height:100px; float:left; margin-right:15px; border-radius: 50%; object-fit: cover;">
                <div style="margin-left: 115px; color: black;">
                    <strong style="font-size: 18px;">{role}</strong><br>
                    <span style="font-size: 16px;">{full_text}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.000005)  # Increased typing speed

# Function to get base64 encoded image
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Function to set a background image
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        .stApp > header {{
            background-color: rgba(0,0,0,0.5);
        }}
        .stApp .block-container {{
            background-color: rgba(255,255,255,0.7);
            padding: 20px;
            border-radius: 15px;
        }}
        .streamlit-expanderHeader {{
            color: black !important;
            background-color: rgba(255,255,255,0.7) !important;
            font-size: 18px;
        }}
        .streamlit-expanderContent {{
            background-color: rgba(255,255,255,0.7) !important;
            color: black !important;
            font-size: 18px;
        }}
        p, h1, h2, h3, h4, h5, h6 {{
            color: black !important;
            font-size: 18px;
        }}
        .stTextInput > div > div > input {{
            font-size: 18px;
        }}
        .sidebar .sidebar-content {{
            color: white !important;
        }}
        .sidebar-content > div > label {{
            color: white !important;
            font-size: 18px;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 2px 5px;
        }}
        .sidebar-content > div > div > div > label {{
            color: white !important;
            font-size: 18px;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 2px 5px;
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: white !important;
        }}
        [data-testid="stSidebar"] {{
            color: white !important;
        }}
        .stButton > button {{
            color: white !important;
            background-color: rgba(0, 0, 0, 0.5) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background
set_background("white-paper-texture_1194-5306.jpg")

# Initialize session state for graph data
if 'df' not in st.session_state:
    csv_path = "pdf3.csv"
    st.session_state.df = pd.read_csv(csv_path, skiprows=1)  # Skip the first row as it's a title
    st.session_state.edited_df = st.session_state.df.copy()

# Sidebar
with st.sidebar:
    st.markdown('<h1 style="color: white;"></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: white;">📚 Baza interna documente</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("", accept_multiple_files=True, key="file_uploader")
    if uploaded_files:
        st.markdown(f'<p style="color: white;">{len(uploaded_files)} file(s) added successfully!</p>', unsafe_allow_html=True)
        for file in uploaded_files:
            st.markdown(f'<p style="color: white;">Added: {file.name}</p>', unsafe_allow_html=True)

    st.markdown('<h1 style="color: white;"></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: white;">📂 Adauga fisiere pentru autocompletare</p>', unsafe_allow_html=True)
    uploaded_files_temp = st.file_uploader("", accept_multiple_files=True, key="file_uploader_temp")
    if uploaded_files_temp:
        st.markdown(f'<p style="color: white;">{len(uploaded_files_temp)} file(s) added successfully!</p>', unsafe_allow_html=True)
        for file in uploaded_files_temp:
            st.markdown(f'<p style="color: white;">Added: {file.name}</p>', unsafe_allow_html=True)

# Main content area
st.title("🤖 AI Project Team Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.show_files = False

# Layout columns
col1, col2 = st.columns([3, 1])

with col1:
    # User input
    user_input = st.text_input("💬 Scrie aici mesajul pentru echipa AI:", key="user_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.show_files = False  # Reset file display
        
        # Display user message with unique color and adjusted icon
        user_color = generate_pastel_color()
        st.markdown(
            f"""
            <div style="background-color: {user_color}; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-height: 120px;">
                <img src="data:image/png;base64,{get_image_base64('logistica-fill.png')}" style="width:80px; height:100px; float:left; margin-right:15px; border-radius: 50%; object-fit: cover;">
                <div style="margin-left: 115px; color: black;">
                    <strong style="font-size: 18px;">You</strong><br>
                    <span style="font-size: 16px;">{user_input}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Simulate AI team's response
        with st.spinner("Thinking..."):
            time.sleep(0.5)
        
        # AI team responses with icons
        responses = [
            ("Agent Management", "Thank you for your input. I'll coordinate with the team to address your request.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\manager-fill.png"),
            ("AI Researcher", "Based on recent advancements, we can implement a transformer-based model for this task.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\scrape-fill.png"),
            ("Software Developer", "I'll start working on a prototype using PyTorch. We should have a working model soon.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\suport-fill.png"),
            ("Technical Writer", "I'll begin drafting the documentation for our new model, including its architecture and usage instructions.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\marketing-fill.png"),
            ("Agent Management", "Excellent progress, team. Let's schedule a review meeting to discuss the prototype.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\manager-fill.png"),
            ("AI Researcher", "I've completed the initial analysis. The model shows promising results in early tests.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\scrape-fill.png"),
            ("Software Developer", "The prototype is ready for testing. I've implemented the core functionalities as discussed.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\suport-fill.png"),
            ("Technical Writer", "The first draft of the documentation is complete. I'll need input from the team for technical details.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\marketing-fill.png"),
            ("Agent Management", "Great work, everyone. Let's prepare for a client presentation next week.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\manager-fill.png"),
            ("AI Researcher", "I've optimized the model further. We're seeing a 15% improvement in performance.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\scrape-fill.png"),
            ("Software Developer", "I've addressed the feedback from testing. The model is now more robust and efficient.", "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\suport-fill.png")
        ]
        
        for role, message, icon_path in responses:
            create_message_box(role, message, icon_path)
        
        st.session_state.show_files = True

    # Display file previews
    if st.session_state.show_files:
        st.header("📊 Project Files")

        # Excel file previews
        excel_files = [
            "pdf1.csv",
            "pdf2.csv",
            "pdf3.csv"
        ]

        for i, excel_path in enumerate(excel_files, 1):
            st.subheader(f"Calcul DEVIZ Ofertare {i}")
            try:
                df = pd.read_csv(excel_path)
                st.dataframe(df, height=300)
            except Exception as e:
                st.error(f"Error reading Excel file {i}: {str(e)}")
                st.warning(f"Please make sure the file path for Excel {i} is correct and the file is not corrupted.")

        # Adding an interactive Plotly chart at the end
        st.header("📊 Interactive Plotly Chart")
        
        try:
            # Allow user to edit data
            st.subheader("Edit Chart Data")
            edited_df = st.data_editor(st.session_state.edited_df, num_rows="dynamic")
            
            # Update button
            if st.button("Update Chart"):
                st.session_state.edited_df = edited_df
            
            # Create the interactive graph
            fig = go.Figure()
            
            for column in st.session_state.edited_df.columns[1:]:  # Skip the first column
                fig.add_trace(go.Bar(
                    y=[column],
                    x=[st.session_state.edited_df[column].iloc[0]],
                    name=column,
                    orientation='h'
                ))
            
            fig.update_layout(
                title="Profitabilitate Proiect",
                yaxis_title="Categorie",
                xaxis_title="Valoare",
                barmode='group',
                height=600  # Make the chart taller
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing graph data: {str(e)}")
            st.warning("Please make sure the data is in the correct format.")

        # PDF files
        st.subheader("📄 PDF Reports")
        pdf_files = [
            "3.Declaratie-privind-eligibilitatea-societatii-in-vederea-acordarii-ajutorului-de-minimis.pdf",
            "AIPRO VISION S.R.L..pdf",
            "auction1.pdf",
            "auction2.pdf",
            "Licitatie.pdf"
        ]

        for i, pdf_path in enumerate(pdf_files, 1):
            with st.expander(f"PDF Report {i}"):
                display_pdf(pdf_path)

with col2:
    # Add any additional content for the right column here
    pass
