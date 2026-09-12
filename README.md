# Semantic Search Engine

A polished single-document semantic search app built with:

- Streamlit for the UI
- SentenceTransformers for text embeddings
- FAISS for fast vector search

## Input document

Upload one text-based file from the UI. The app builds semantic search only for that uploaded file.

## Recommended Python

Use Python 3.11 on Windows for the smoothest FAISS setup.

## Install

```powershell
.\install_requirements.ps1
```

## Run

```powershell
.\run_app.ps1
```

If you prefer manual commands, use the same Python 3.11 interpreter for both install and run:

```powershell
C:\Users\darsh\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt
C:\Users\darsh\AppData\Local\Programs\Python\Python311\python.exe -m streamlit run app.py
```

## Document format expected

The file is parsed as alternating non-empty lines:

1. Question
2. Answer
3. Question
4. Answer

Any uploaded text file that follows this format will work.
