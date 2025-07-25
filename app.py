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

# Gemini Vision response
def gemini_response(resume_image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([
        prompt,
        resume_image
    ])
    return response.text

# PDF processing to image
def input_pdf(uploaded_file):
    if uploaded_file is not None:
        # Add Poppler path
        poppler_path = r"C:\Users\anand\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
        pdf_content = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
        first_page = pdf_content[0]

        # Convert image to bytes
        import io
        img_bytes = io.BytesIO()
        first_page.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        # Gemini-compatible format
        pdf_parts = [
        {
        "mime_type": "image/jpeg",
        "data": img_bytes
        }
        ]

        return pdf_parts
    else:
        st.warning("Please upload a PDF file.")
        return None

# Streamlit app layout
st.title("ATS Resume Analyzer")
st.write("Upload your resume in PDF format.")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    pdf_parts = input_pdf(uploaded_file)

    if pdf_parts:
        st.image(pdf_parts[0]["data"], caption="First Page of PDF", use_container_width=True)

        prompt = st.text_area(
            "Enter Job Description",
            placeholder="Paste the job description here...",
            height=200
        )

        if st.button("Analyze"):
            if prompt.strip() == "":
                st.warning("Please enter a job description.")
            else:
                with st.spinner("Analyzing resume with Gemini AI..."):
                    response = gemini_response(pdf_parts[0], prompt)
                    st.success("✅ Analysis Complete!")
                    st.subheader("📊 Gemini AI Response:")
                    st.write(response)
else:
    st.warning("Please upload a PDF file to analyze.")
