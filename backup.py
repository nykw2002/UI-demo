import streamlit as st
import pandas as pd
import time
from PIL import Image
import base64
import io
import os
import random
import matplotlib.pyplot as plt
import networkx as nx

# Function to generate a light, pastel color
def generate_pastel_color():
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)
    return f"rgb({r},{g},{b})"

# Function to display PDF preview
def display_pdf(pdf_path):
    try:
        st.write(f"PDF: {pdf_path.split('\\')[-1]}")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64.b64encode(open(pdf_path, "rb").read()).decode()}" width="700" height="1000" type="application/pdf"></iframe>', unsafe_allow_html=True)
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
    
    time.sleep(0.5)  # Reduced thinking time
    
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
        time.sleep(0.01)  # Increased typing speed

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
        }}
        .streamlit-expanderContent {{
            background-color: rgba(255,255,255,0.7) !important;
            color: black !important;
        }}
        p, h1, h2, h3, h4, h5, h6 {{
            color: black !important;
            font-size: 18px;
        }}
        .stTextInput > div > div > input {{
            font-size: 18px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to create and display the animated vertical project pipeline
def create_project_pipeline(stages, pipeline_placeholder):
    G = nx.DiGraph()
    pos = {}
    colors = []
    
    for i, (stage, details) in enumerate(stages.items()):
        G.add_node(stage)
        pos[stage] = (0, -i)
        colors.append(details['color'])
        if i > 0:
            G.add_edge(list(stages.keys())[i-1], stage)
    
    for i in range(len(stages) + 1):
        fig, ax = plt.subplots(figsize=(3, 10))
        sub_G = nx.DiGraph(G.subgraph(list(stages.keys())[:i]))
        sub_colors = colors[:i]
        
        nx.draw(sub_G, pos, with_labels=True, node_color=sub_colors, node_size=3000, node_shape='s', ax=ax, 
                arrows=True, arrowsize=20, edge_color='gray')
        nx.draw_networkx_labels(sub_G, pos, {node: f"{node}\n{stages[node]['status']}" for node in sub_G.nodes()}, font_size=8)
        
        ax.set_title("Project Pipeline")
        plt.axis('off')
        
        pipeline_placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.5)

# Set the background
set_background("C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\white-paper-texture_1194-5306.jpg")

# Sidebar
st.sidebar.title("🎨 Theme Customization")
st.sidebar.color_picker("Choose accent color", "#00BFFF")

st.sidebar.title("📚 Knowledge Base")
uploaded_files = st.sidebar.file_uploader("Add files to Knowledge Base", accept_multiple_files=True)
if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} file(s) added successfully!")
    for file in uploaded_files:
        st.sidebar.write(f"Added: {file.name}")

# Main content area
st.title("🤖 AI Project Team Chat")

# Initialize chat history and project stages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.show_files = False
    st.session_state.project_stages = {
        "Planning": {"status": "Completed", "color": "#66c2a5"},
        "Design": {"status": "In Progress", "color": "#fc8d62"},
        "Development": {"status": "Not Started", "color": "#8da0cb"},
        "Testing": {"status": "Not Started", "color": "#e78ac3"},
        "Deployment": {"status": "Not Started", "color": "#a6d854"}
    }

# User input
user_input = st.text_input("💬 Enter your message to the AI Project Team:", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.show_files = False  # Reset file display
    
    # Display user message with unique color and adjusted icon
    user_color = generate_pastel_color()
    st.markdown(
        f"""
        <div style="background-color: {user_color}; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-height: 120px;">
            <img src="data:image/png;base64,{get_image_base64('C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\logistica-fill.png')}" style="width:80px; height:100px; float:left; margin-right:15px; border-radius: 50%; object-fit: cover;">
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
        time.sleep(1)
    
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
    
    # Update project stages based on the conversation
    st.session_state.project_stages["Design"]["status"] = "Completed"
    st.session_state.project_stages["Development"]["status"] = "In Progress"
    
    st.session_state.show_files = True

# Display file previews
if st.session_state.show_files:
    st.header("📊 Project Files")

    # Excel file preview
    st.subheader("Excel Data Preview")
    excel_path = "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\Solution_Prices_for_Different_Company_Sizes.csv"
    try:
        if excel_path.endswith('.csv'):
            df = pd.read_csv(excel_path)
        elif excel_path.endswith('.xlsx'):
            df = pd.read_excel(excel_path)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")
        
        # Convert all columns to string type to avoid Arrow serialization issues
        df = df.astype(str)
        
        # Use st.dataframe with styling
        st.dataframe(
            df.style
            .highlight_max(axis=0)
            .highlight_min(axis=0),
            height=300
        )
        
        # Show summary statistics
        st.write("Summary Statistics:")
        st.write(df.describe())
        
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        st.warning("Please make sure the file path is correct and the file is not corrupted.")

    # PDF files
    st.subheader("📄 PDF Reports")
    pdf_files = [
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\3.Declaratie-privind-eligibilitatea-societatii-in-vederea-acordarii-ajutorului-de-minimis.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\AIPRO VISION S.R.L..pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\auction1.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\auction2.pdf",
        "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\Licitatie.pdf"
    ]

    for i, pdf_path in enumerate(pdf_files, 1):
        with st.expander(f"PDF Report {i}"):
            display_pdf(pdf_path)

    # Image file
    st.subheader("📈 Data Visualization")
    image_path = "C:\\Users\\vasil\\Desktop\\UI-Files_crewai\\sales_graph.png"
    try:
        image = Image.open(image_path)
        st.image(image, caption="Data Visualization", use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")
        st.warning("Please make sure the image file path is correct.")

# Pipeline section
st.header("Project Pipeline")
pipeline_placeholder = st.empty()

# Generate the animated pipeline after the chat ends
if st.session_state.show_files:
    create_project_pipeline(st.session_state.project_stages, pipeline_placeholder)