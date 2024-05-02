from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import openai
from openai import OpenAI


def get_openai_response(input, pdf_content, prompt):
    openai.api_key = st.secrets['openai_key']
    client = OpenAI(api_key=st.secrets['openai_key'])

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": pdf_content + " " + input},
        ]
    )

    response = response.choices[0].message.content
    return response
    # print("***************** AI RESPONSE ****************************")
    # print(response)


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
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("How Can I Improvise my Skills")

submit2 = st.button("Percentage match")

with st.sidebar:
    # with st.form(key='my_form'):
    query = st.sidebar.text_area(
        label="Ask me about the resume",
        max_chars=50,
        key="query"
    )

    submit3 = st.button(label='Submit', type="primary")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """
Your my chat bot assistant to answer only the given questions where the answers are present in resume and if not resume simple say 'Not mentioned in resume'

UG refered for Under Graduate, PG refered for Post Graduate in education.

Question:{}
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if query:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_prompt3.format(query), pdf_content, input_text)
        st.subheader("Answer : ")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
