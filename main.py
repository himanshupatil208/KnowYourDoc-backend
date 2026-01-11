import os
import requests
import json
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI, File, UploadFile, HTTPException
from PyPDF2 import PdfReader
from io import BytesIO
import uvicorn
import re


# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for production, use specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Function to extract text from PDF document
def extract_text_from_pdf(pdf_bytes):
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        text = "".join([page.extract_text() or "" for page in reader.pages])
        return text if text.strip() else "No text found in PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

# Function to send request to Gemini API
def generate_text(prompt):
    
    if not API_KEY:
        return "Error: GEMINI_API_KEY not found in .env file."

    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

# API endpoint to upload PDF and get summary
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        extracted_text = extract_text_from_pdf(pdf_bytes)

        if "Error" in extracted_text:
            raise HTTPException(status_code=400, detail=extracted_text)

        gemini_prompt = f"""
        Read this text given in backticks properly go through everything in detail\n
        ```{extracted_text}``` \n
        Follow these steps:
        1. Write Comprehensive summary of the text.\n"
        2. Assign a score from 1 to 10 where 10 is the most complex a document can get for the average person.\n"
        3. Identify any potential risky clauses\n"
        4. Extract any necessary financial amounts/deadlines/necessary figures\n"
        5. Flag vague or ambiguous terms\n."
        Return a valid JSON object with the following keys: summary, complexity_rating, red_flag_detection, figures_extraction, and loopholes.\n
        summary and complexity rating have single values
        red_flag_detection, figures_extraction and loopholes have array as associated value 

        """
        response = generate_text(gemini_prompt)
        try:
            # Attempt to find the innermost JSON object
            json_match = re.search(r'\{.*\}', response, re.DOTALL) #re.DOTALL to match newlines.
            if json_match:
                json_string = json_match.group(0)
                json_response = json.loads(json_string)
                return json_response
            else:
                raise ValueError("No valid JSON found in response.")

        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON Parsing Error: {e}")
            print(f"Failed to parse: {response}")
            raise HTTPException(status_code=500, detail=f"Gemini API returned invalid JSON: {e}")
       

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main function to run FastAPI server
def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# Run the app only if this script is executed directly
if __name__ == "__main__":
    main()
