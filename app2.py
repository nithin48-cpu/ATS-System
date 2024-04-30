from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        text = "this is the text in resume, "
        # with open(uploaded_file., "rb") as file:
        #     # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        print(len(pdf_reader.pages))
        # Iterate through each page of the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Extract text from the current page
            page = pdf_reader.pages[0]
            text += page.extract_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = "this is job description, "
input_text += st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage match")
with st.sidebar:
    # with st.form(key='my_form'):
    query = st.sidebar.text_area(
        label="Ask me about the resume",
        max_chars=50,
        key="query"
    )

    submit3 = st.button(label='Submit',type="primary")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
the percentage of resume is calculated with 50% for skills and 50 % persent for experience

formula for skills nof skills in resume/skills in job description * 50
check the year in resume with least year and recent year
Experience=recent year- least year
formula for experence number of experience in resume/experience in job description * 50,if experience is less than in job description then percentage of experence is 0% 

UG refered for Under Graduate, PG refered for Post Graduate in education.

And Understand the domain of the resume and job description and how they are matching
"""

input_prompt3 = """
Your my chat bot assistant to answer only the given questions where the answers are present in resume and if not resume simple say 'Not mentioned in resume'

UG refered for Under Graduate, PG refered for Post Graduate in education.

Question:{}
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if query:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3.format(query), pdf_content, input_text)
        st.subheader("Answer : ")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
