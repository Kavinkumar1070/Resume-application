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
   - Education details (multiple entries should be returned in a list)
   - Employment details (multiple entries should be returned in a list)
   - Technical skills
   - Soft skills
   - Certificates
   
Return only the requested information for each task, without any additional explanations. Do not make any assumptions by yourself. If details are not found, return 'Information not available'. 

For Education details, return a list of dictionaries where each dictionary contains:
   - "college": "information"
   - "degree": "information"
   - "year": "information"

For Employment details, return a list of dictionaries where each dictionary contains:
   - "company name": "information"
   - "Year of experience": "information"

**JSON Response Format:** Return only the payload JSON response in the following format, enclosed with `~~~` before and after the response.
~~~ {
    "Resume Classification": "classification result",
    "Job Recommendation": "recommendation result",
    "Resume Parsing": {
        "Full name": "information",
        "Email ID": "information",
        "GitHub portfolio": "information",
        "LinkedIn ID": "information",
        "Education details": [
            {
                "college": "information",
                "degree": "information",
                "year": "information"
            },
            {
                "college": "information",
                "degree": "information",
                "year": "information"
            }
        ],
        "Employment details": [
            {
                "company name": "information",
                "Year of experience": "information"
            },
            {
                "company name": "information",
                "Year of experience": "information"
            }
        ],
        "Technical skills": "information",
        "Soft skills": "information",
        "Certificates": "information"
    }
} ~~~

Ensure the response is formatted as valid JSON and nothing else.
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

import json

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
    
    try:
        # Extract the full response text
        response_text = response.choices[0].message.content.strip()
        print(response_text)
        # Find the starting and ending positions of the JSON portion enclosed by `~~~`
        json_start_idx = response_text.find("~~~")
        json_end_idx = response_text.rfind("~~~")
        
        # If no valid JSON block is found, raise an error
        if json_start_idx == -1 or json_end_idx == -1:
            raise ValueError("No valid JSON enclosed in `~~~` markers found.")
        
        # Extract JSON portion by trimming off `~~~`
        json_string = response_text[json_start_idx + 3:json_end_idx].strip()
        
        # Load the JSON content
        result = json.loads(json_string)
        print(result)  # For debugging
        
        return result
    
    except json.JSONDecodeError:
        print("Error: Unable to parse JSON response.")
        return {"error": "Invalid JSON response"}
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}



    
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