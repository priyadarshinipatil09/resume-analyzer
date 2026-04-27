import fitz
import os
from docx import Document
from google.genai import Client
from dotenv import load_dotenv

#load the.env file
load_dotenv()

#get key from environment
api_key = os.getenv("GEMINI_API_KEY")

#configure gemini
client=Client(api_key=api_key)

def extract_resume_text(file_path):
  if file_path.lower().endswith(".pdf"):
    return extract_text_from_pdf(file_path)
  
  elif file_path.lower().endswith(".docx"):
    return extract_text_from_docx(file_path)
  
  else:
    print("Unsupported file format")
    return None
  
def extract_text_from_pdf(pdf_path):
  text = ""
  with fitz.open(pdf_path) as doc:
    for page in doc:
      text += page.get_text("text")
  return text

def extract_text_from_docx(doc_path):
  text=""
  doc = Document(doc_path)
  for paragraph in doc.paragraphs:
    text+= paragraph.text + "\n"
  return text


if __name__ == "__main__":
  file_path ="alex.docx"
  resume_text = extract_resume_text(file_path)
  
  if resume_text:
    print('Resume extracted successfully!')
    print('Sending to Gemini for analysis...')
    job_role = input("Enter the job role you are applying for: ")
    prompt=f"""You are a senior technical recruiter with 10+ years  of    experience hiring freshers for {job_role} roles.

              Analyze the following resume BRUTALLY and HONESTLY. Do not sugarcoat anything.
              Do not add any fake experience, skills, or achievements that are not in the resume.

              Provide feedback in exactly this structure:
              1. OVERALL IMPRESSION (2-3 lines)
              2. SECTION BY SECTION ANALYSIS:
                 - Objective/Summary: (strengths and what's weak)
                 - Education: (is it presented well)
                 - Technical Skills: (missing skills, irrelevant skills)
                 - Projects: (are they strong enough, what's missing)
                 - Certifications: (relevant or not)
              3. STRENGTHS (bullet points)
              4. WEAKNESSES (bullet points, be brutal)
              5. IMPROVEMENTS NEEDED (specific actionable steps)
              6. IMPROVED SECTIONS (rewrite weak sections based ONLY on what exists in resume)
              7. ATS SCORE ESTIMATE (out of 100, with reason)

              Resume:
              {resume_text}"""
    response =client.models.generate_content(
      model = "gemini-2.5-flash-lite",
      contents=prompt)
    print(response.text)
