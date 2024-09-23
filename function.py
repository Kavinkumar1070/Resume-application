import re
from PyPDF2 import PdfReader
from groq import Groq
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helpers function using Python
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

def pdf_to_text(file):
    reader = PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


Basic_details = """
You are an AI bot designed to act as a professional for Resume Processing. You have three tasks to perform:

1. **Resume Classification**: Based on the provided details like Objective and Technical Skills, classify the resume into groups such as HR, Teacher, Finance, IT, Public Sector, etc., and suggest only 1 job title without any explanations.
   
2. **Job Recommendation**: Using details such as Objective, Work Experience, and Technical Skills, recommend a single job title for the user, without any explanations.

3. **Resume Parsing**: Extract the following information from the resume:
   - Full name
   - Email ID
   - GitHub portfolio
   - LinkedIn ID
   - Employment details
   - Technical skills
   - Soft skills
   - Certificates
   
Return only the requested information for each task, without any additional explanations.
in json format like {{"Resume Classification":"information",
                       Job Recommendation:"information",
                       "Resume Parsing": {
                            "Full name":"information",
                            "Email ID":"information",
                            "GitHub portfolio":"information",
                            "LinkedIn ID":"information",
                            "Employment details":"information",
                            "Technical skills":"information",
                            "Soft skills":"information",
                            "Certificates":"information"
                       }}}
"""
strength_weakness = """
    You are an experienced Technical Human Resource Manager with tech experience in roles like Data Science, Full Stack Web Development,
    Big Data Engineering, DevOps, Data Analyst, Data Engineer, Machine Learning Engineer, AI Engineer. Your task is to review the provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements
    Then, list any missing keywords and give final thoughts.
"""
ats_scoring = """
    You are a skilled ATS (Applicant Tracking System) scanner with expertise in roles such as Data Science, Full Stack Web Development,
    Big Data Engineering, DevOps, Data Analyst, Data Engineer, Machine Learning Engineer, AI Engineer, and deep ATS functionality.
    Your task is to evaluate the resume against the provided job description. 
    Only provide the percentage match between the resume and the job description.
"""

    
# Resume processing
def get_groq_response(resume_data, input_prompt):
    client = Groq(api_key="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")
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": input_prompt},
            {"role": "user", "content": resume_data}
        ],
        temperature=0.2
    )   
    response_text = response.choices[0].message.content
    json_start_idx = response_text.find("{")
    json_end_idx = response_text.rfind("}") + 1
    result = response_text[json_start_idx:json_end_idx]
    print(result)
    print("****************")
    result = json.loads(result)
    print(result)
    print("****************")
    
    return result

    
# # Resume processing
# def get_groq_response(resume_data, input_prompt):
#     client = Groq(api_key="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")
#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": input_prompt},
#             {"role": "user", "content": resume_data}
#         ],
#         temperature=0.2
#     )   
#     response_text = response.choices[0].message.content
#     return response_text

# Resume processing
def get_groq_response1(resume_data, input_prompt):
    client = Groq(api_key="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")
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": input_prompt},
            {"role": "user", "content": resume_data}
        ],
        temperature=0.2
    )   
    response_text = response.choices[0].message.content

    
    return response_text