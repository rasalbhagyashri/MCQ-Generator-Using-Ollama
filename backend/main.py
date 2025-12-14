from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pdf_utils import extract_text_from_pdf
from docx_utils import generate_question_paper, generate_answer_sheet
from local_llm import generate_mcqs_local

import uuid
import os

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GENERATE MCQs ----------------
@app.post("/generate")
async def generate_mcq(
    pdf: UploadFile,
    num_questions: int = Form(...)
):
    # 1. Validate file
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # 2. Extract text
    content = extract_text_from_pdf(pdf.file)
    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded PDF has no readable text")

    # 3. Generate MCQs using local LLM
    try:
        result = generate_mcqs_local(content, num_questions)
    except Exception as e:
        print("🔥 LLM ERROR:", e)
        raise HTTPException(status_code=500, detail="MCQ generation failed")

    # 4. Validate LLM output
    if "questions" not in result:
        raise HTTPException(status_code=500, detail="Invalid MCQ format generated")

    mcqs = result["questions"]

    # 5. Generate DOCX files
    uid = str(uuid.uuid4())
    q_file = f"questions_{uid}.docx"
    a_file = f"answers_{uid}.docx"

    generate_question_paper(mcqs, q_file)
    generate_answer_sheet(mcqs, a_file)

    return {
        "question_paper": q_file,
        "answer_sheet": a_file
    }

# ---------------- DOWNLOAD FILE ----------------
@app.get("/download/{file_name}")
def download(file_name: str):
    if not os.path.exists(file_name):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
