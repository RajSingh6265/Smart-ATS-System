from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import PyPDF2 as pdf
import google.generativeai as genai
import time
st.set_page_config(page_title="ATS Resume Expert", layout="wide")   
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Input  prompts
input_prompt1 = """
As an experienced Technical Human Resource Manager, AI Engineer, Data Scientist, Generative AI Engineer, 
and Data Analyst, your task is to thoroughly review the provided resume against the given job description and provide a detailed analysis of its strengths and weaknesses.  Consider factors such as keyword optimization, formatting, clarity, and overall effectiveness in conveying the candidate's skills and experience.  Provide specific examples from the resume to support your analysis.
"""

input_prompt2 = """
You are an experienced AI/Generative AI/Machine Learning/NLP/Computer Vision Engineer reviewing a resume against a job description. Identify areas where the resume could be improved to better highlight the candidate's skills and experience relevant to the target job. Suggest specific improvements to wording, formatting, and content organization. Prioritize suggestions based on their potential impact on the candidate's success in the application process.
"""

input_prompt3 = """
You are a highly skilled Applicant Tracking System (ATS) expert. Analyze the provided resume against the job description to determine the likelihood of the resume being successfully parsed and ranked by an ATS.  Calculate a match percentage based on keyword overlap, skills alignment, and overall resume structure.  Explain your scoring rationale and provide specific examples of areas where the resume excels or falls short in terms of ATS compatibility.
"""

input_prompt4 = """
You are a keyword analysis expert. Analyze the provided resume and job description to identify keywords and phrases that are present in both.  Provide a list of these keywords, along with their frequency in both the resume and the job description.  Highlight any keywords that are missing from the resume but are prevalent in the job description.  Suggest ways to incorporate these missing keywords naturally into the resume to improve its searchability and relevance.
"""

# CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea {
        background-color: #000000;
        color: #FFFFFF;    
        border-radius: 10px;
    }
    .upload-box {
        border: 2px dashed #FF4B4B;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .css-1v0mbdj.etr89bj1 {
        width: 100%;
    }
    .title-text {
        color: #FF4B4B;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    .subtitle-text {
        font-size: 20px;
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    else:
        raise FileNotFoundError("Please Upload the PDF File")


 

st.markdown("# 🎯 Smart ATS Resume Analyzer")

# Input Section
st.markdown("## 1️⃣ Input Your Information")
col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area("Job Description:", height=200)

with col2:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")

#Analysis Options
st.markdown("## 2️⃣ Choose Analysis Type")
submit1, submit2, submit3, submit4 = None, None, None, None  # Initialize button variables

if uploaded_file and input_text:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        submit1 = st.button("📊 Basic Analysis")
    with col2:
        submit2 = st.button("💡 Improvement Tips")
    with col3:
        submit3 = st.button("📈 Match Score")
    with col4:
        submit4 = st.button("🎯 Keyword Analysis")

#Results Section
st.markdown("## 3️⃣ Analysis Results")
if submit1 or submit2 or submit3 or submit4:
    with st.spinner("Analyzing your resume..."):
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text) if submit1 else (get_gemini_response(input_prompt2, pdf_content, input_text) if submit2 else (get_gemini_response(input_prompt3, pdf_content, input_text) if submit3 else get_gemini_response(input_prompt4, pdf_content, input_text)))
        st.write(response)





