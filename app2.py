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


def get_gemini_response(prompt, pdf_content, input):
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content([prompt, pdf_content, input])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        text = "this is the text in resume of a person who applied for the job,"
        # with open(uploaded_file., "rb") as file:
        #     # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
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

Automatically adjust the spacing between the words in the response.

"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
the percentage of resume is calculated with 50% for skills and 50 % persent for experience

formula for skills nof skills in resume/skills in job description * 50
check the year in resume with least year and recent year
Experience=calculate between the year and months and calculate
formula for experence number of experience in resume/experience in job description * 50

UG refered for Under Graduate, PG refered for Post Graduate in education.

And Understand the domain of the resume and job description and how they are matching.

Automatically adjust the spacing between the words in the response.
"""

input_prompt3 = """
Your role as my chatbot assistant is to provide accurate responses to specific questions by referring to the information available in the resume. If a question is asked that can be answered using details from the resume, you'll provide that answer. However, if the information is not present in the resume, you'll simply reply with "Not mentioned in resume."


To help ensure accuracy, here are some guidelines:

Use "UG" to indicate Under Graduate education and "PG" for Post Graduate education.
Any sequence of ten digits in the resume should be recognized as a phone number.
If a string starts with 'github.com/' or 'https://github.com/', it should be considered a GitHub link.
Strings starting with 'https://' should be identified as websites or links.
With these guidelines in mind, you'll be able to accurately respond to questions based on the content of the resume. If you encounter any uncertainties or need clarification, feel free to ask!

Question: {}

Automacally adjust the spacing in answer.
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
