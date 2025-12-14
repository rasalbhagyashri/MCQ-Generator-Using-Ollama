# MCQ Generator using Ollama (Local LLM)

This project is a **local Multiple Choice Question (MCQ) Generator** that generates a **question paper and a separate answer sheet** from an uploaded PDF document using a **locally running Large Language Model (LLM) via Ollama**.

The application runs **entirely on a local machine**, does not require any cloud-based APIs, and ensures **data privacy, zero API cost, and offline capability after setup**.

---

## Features

- Upload PDF documents
- Generate a user-defined number of MCQs
- Uses **Ollama local LLM (phi3:mini)**
- Generates:
  - MCQ Question Paper (DOCX)
  - Answer Sheet (DOCX)
- FastAPI-based backend
- Simple and clean frontend using HTML and Tailwind CSS
- No internet or API key required after initial model download

---

## Project Architecture

Frontend (HTML + JavaScript)  
→ FastAPI Backend  
→ PDF Text Extraction  
→ Ollama Local LLM (phi3:mini)  
→ Structured MCQs (JSON)  
→ DOCX Generation  
→ Downloadable Question Paper & Answer Sheet  

---

## Folder Structure

```text
MCQ-Generator/
├── backend/
│   ├── main.py
│   ├── local_llm.py
│   ├── pdf_utils.py
│   ├── docx_utils.py
│   ├── models.py
│   └── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md
```


---

## Tech Stack

Backend:
- Python
- FastAPI
- Ollama
- pdfplumber
- python-docx
- Uvicorn

Frontend:
- HTML
- Tailwind CSS
- JavaScript

---

## Setup Instructions

### Step 1: Install Ollama

Download Ollama from https://ollama.com

```bash
ollama pull phi3:mini
ollama run phi3:mini
```

---

### Step 2: Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://127.0.0.1:8000

---

### Step 3: Frontend Setup

```bash
cd frontend
python -m http.server 3000
```

Open http://127.0.0.1:3000/index.html

---

## API Endpoints

POST /generate  
GET /download/{file_name}

Open-source for educational and personal use.
