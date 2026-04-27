import os
import markdown
from google.genai import Client
from dotenv import load_dotenv
from analyzer import extract_resume_text
from flask import Flask, render_template, request

load_dotenv()
api_key =  os.getenv("GEMINI API KEY")
client = Client(api_key = api_key)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
   job_role = request.files.get("jobrole")
   resume_file = request.files.get("filename")

   file_path = os.path.join("uploads", resume_file.filename)
   os.makedirs("uploads", exist_ok = True)
   resume_file.save(file_path)

   resume_text =extract_resume_text(file_path)

   prompt = f"""You are a senior technical recruiter with 10+ years  of    experience hiring freshers for {job_role} roles.

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
   response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=prompt
   )

   result = markdown.markdown(response.text)

   return render_template("result.html", result=result)

if __name__ == "__main__":
  app.run(debug=True)
