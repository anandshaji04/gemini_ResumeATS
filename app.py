import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
from google.generativeai import types

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("API_KEY is not set in the .env file.")

# Initialize the Generative AI client
genai.configure(api_key=API_KEY)

def gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel(name="gemini-pro-vision")
    response= model.generate_content(input,pdf_content[0],prompt)
    return response.text

def input_pdf(uploaded_file):
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    # Check if a file has been uploaded and convert it to images
    if uploaded_file is not None:
        pdf_content = pdf2image.convert_from_bytes(uploaded_file.read())
        return pdf_content
    return None
