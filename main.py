
from fastapi import FastAPI, File, UploadFile,Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from function import pdf_to_text, get_groq_response,get_groq_response1,Basic_details,strength_weakness,ats_scoring
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import urllib.parse
from fastapi.responses import RedirectResponse

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve static files from the uploads directory
app.mount("/resume", StaticFiles(directory=UPLOAD_DIR), name="resume")


# Set up Jinja2 templates directory
app.mount("/templates", StaticFiles(directory=Path(__file__).resolve().parent / "templates"), name="templates")


# Serve an HTML form for uploading resumes
@app.get("/")
def get():
    file_path = Path(__file__).resolve().parent / "templates" / "front_page.html"
    if not file_path.exists():
        return HTMLResponse("File not found", status_code=404)
    return HTMLResponse(file_path.read_text())


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    file_ext = file.filename.split('.')[-1].lower()
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if file_ext == 'docx' or file_ext == 'pdf':
        return {"filename": file.filename, "message": "Resume uploaded successfully!"}

    return {"error": "Unsupported file format"}


# Endpoint 1: Input resume text and get a response
@app.post("/process_resume/")
async def process_resume(file: UploadFile = File(...)):
    text = pdf_to_text(file.file)
    result = get_groq_response(text, Basic_details)

    return {"details": result}# Endpoint 2: Input resume text and job description, strength,weakness
@app.post("/process_resume_and_job/")
async def process_resume_and_job(file: UploadFile = File(...),job_description: str = Form(None)):
    text = pdf_to_text(file.file)
    result = get_groq_response1(text + " " + job_description, strength_weakness)
    return JSONResponse(content={"filename": file.filename, "result": result})
    #return result

#score
@app.post("/process_resume_and_job/score")
async def process_resume_and_job(file: UploadFile = File(...),job_description: str = Form(None)):
    text = pdf_to_text(file.file)
    result = get_groq_response1(text + " " + job_description, ats_scoring)
    return JSONResponse(content={"filename": file.filename, "result": result})