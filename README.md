# AI Resume Analyzer

An AI-powered web application that analyzes resumes and provides 
structured feedback using Google Gemini API.

## Features
- Upload PDF or Word (.docx) resumes
- Enter target job role for role-specific analysis
- Get brutal honest feedback including strengths, weaknesses
- ATS score estimate out of 100
- Improved resume sections generated automatically

## Tech Stack
- Python, Flask
- Google Gemini API
- PyMuPDF, python-docx
- HTML, CSS

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Gemini API key in `.env` file as `GEMINI_API_KEY=your_key`
4. Run: `python app.py`
