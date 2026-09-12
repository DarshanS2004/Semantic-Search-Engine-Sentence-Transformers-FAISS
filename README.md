# Semantic Search Engine

A lightweight and interactive **semantic search engine** built with **Streamlit, SentenceTransformers, and FAISS**.

The application allows users to upload a text-based document and perform semantic search over its contents using transformer-based text embeddings and fast vector similarity search.

---

## Overview

Traditional keyword search looks for exact or closely matching words.

This project takes a different approach by converting text into numerical **embeddings** and comparing the semantic similarity between the user's query and the content stored in the document.

The core workflow is:

```text
Upload Document
       │
       ▼
Parse Document
       │
       ▼
Generate Embeddings
       │
       ▼
Build FAISS Index
       │
       ▼
Enter Search Query
       │
       ▼
Generate Query Embedding
       │
       ▼
Semantic Vector Search
       │
       ▼
Relevant Results
```

---

## Key Features

- 🔎 Semantic rather than simple keyword-based search
- 🧠 SentenceTransformer-based text embeddings
- ⚡ FAISS-powered vector similarity search
- 🖥️ Interactive Streamlit user interface
- 📄 Single-document search
- 📤 Upload a text-based document through the UI
- 📝 Question-and-answer document format
- 🚀 Fast similarity-based retrieval
- 💻 Local execution without requiring an external AI API

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application development |
| **Streamlit** | Interactive web interface |
| **SentenceTransformers** | Generate semantic text embeddings |
| **FAISS** | Fast vector similarity search |
| **PowerShell** | Installation and application startup scripts |

The application uses SentenceTransformers for text embeddings and FAISS for vector search. :contentReference[oaicite:1]{index=1}

---

## How It Works

### 1. Upload a Document

The application accepts one text-based file through the Streamlit interface.

The semantic search index is built specifically for the uploaded document. :contentReference[oaicite:2]{index=2}

### 2. Parse the Document

The uploaded text file is expected to contain alternating non-empty lines:

```text
Question
Answer
Question
Answer
Question
Answer
```

For example:

```text
What is Python?
Python is a programming language.

What is FAISS?
FAISS is a library for efficient vector similarity search.
```

The documented parser expects the alternating Question/Answer structure. :contentReference[oaicite:3]{index=3}

### 3. Generate Embeddings

The text content is converted into numerical vector representations using **SentenceTransformers**.

These embeddings capture semantic relationships between pieces of text.

### 4. Build the FAISS Index

The generated vectors are stored in a **FAISS** index.

FAISS allows the application to efficiently search for vectors that are most similar to a user's query.

### 5. Search Semantically

When a user enters a query:

```text
How do I learn programming?
```

the query is converted into an embedding and compared against the vectors in the FAISS index.

The application can therefore find semantically relevant content even when the exact words in the query are not present in the stored text.

---

## Architecture

```text
                   ┌──────────────────────┐
                   │      Streamlit UI    │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Upload Text File   │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │   Document Parsing   │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ SentenceTransformers │
                   │      Embeddings      │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │    FAISS Vector      │
                   │        Index         │
                   └──────────┬───────────┘
                              │
                              │
                       User Search Query
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Query Embedding      │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Semantic Similarity  │
                   │       Search         │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Relevant Results     │
                   └──────────────────────┘
```

---

## Input Document Format

The application is designed for text files containing alternating questions and answers.

Required structure:

```text
Question
Answer
Question
Answer
Question
Answer
```

Each non-empty line is interpreted as part of the alternating Question/Answer structure. :contentReference[oaicite:4]{index=4}

### Example

```text
What is machine learning?
Machine learning is a field of artificial intelligence that enables systems to learn from data.

What is deep learning?
Deep learning is a machine learning approach based on neural networks with multiple layers.

What is semantic search?
Semantic search retrieves information based on meaning and context rather than only matching keywords.
```

Any uploaded text file following this format can be used by the application. :contentReference[oaicite:5]{index=5}

---

## Installation

### Recommended Python Version

For Windows, **Python 3.11** is recommended for the smoothest FAISS setup. :contentReference[oaicite:6]{index=6}

### Option 1 — Using the Installation Script

Run the provided PowerShell installation script:

```powershell
.\install_requirements.ps1
```

This is the documented installation method for the project. :contentReference[oaicite:7]{index=7}

---

## Manual Installation

If you prefer installing the dependencies manually:

```powershell
python -m pip install -r requirements.txt
```

For Windows, use the same Python 3.11 interpreter for both installation and execution.

Example:

```powershell
C:\Users\darsh\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt
```

The project documentation specifically recommends using the same Python 3.11 interpreter for installation and running the application. :contentReference[oaicite:8]{index=8}

---

## Running the Application

### Option 1 — Using the Run Script

Run:

```powershell
.\run_app.ps1
```

:contentReference[oaicite:9]{index=9}

### Option 2 — Run Streamlit Manually

```powershell
python -m streamlit run app.py
```

Or, using the documented Python 3.11 interpreter:

```powershell
C:\Users\darsh\AppData\Local\Programs\Python\Python311\python.exe -m streamlit run app.py
```

:contentReference[oaicite:10]{index=10}

---

## Usage

### Step 1 — Launch the Application

Start the Streamlit application:

```powershell
.\run_app.ps1
```

### Step 2 — Upload a Document

Upload one text-based document through the application interface.

### Step 3 — Build the Search Index

The application processes the uploaded document and creates the semantic search index.

### Step 4 — Enter a Query

Enter a question or search phrase related to the document.

### Step 5 — Review Results

The application performs vector similarity search and returns relevant content from the uploaded document.

---

## Semantic Search vs Keyword Search

A traditional keyword search might look for:

```text
"machine learning algorithms"
```

A semantic search engine can potentially identify related content such as:

```text
"methods used by computers to learn patterns from data"
```

even when the exact keywords are different.

This is possible because SentenceTransformers converts text into embeddings representing semantic information.

FAISS then performs efficient similarity search over those embeddings.

---

## Project Workflow

```text
                INPUT
                  │
                  ▼
          Upload Text File
                  │
                  ▼
          Parse Q&A Content
                  │
                  ▼
       Generate Text Embeddings
                  │
                  ▼
           Build FAISS Index
                  │
                  ▼
             User Query
                  │
                  ▼
        Generate Query Vector
                  │
                  ▼
       Compare Vector Similarity
                  │
                  ▼
        Retrieve Relevant Content
                  │
                  ▼
              RESULTS
```

---

## Project Structure

A typical project structure is:

```text
Semantic-Search-Engine/
│
├── app.py
├── requirements.txt
├── README.md
├── install_requirements.ps1
├── run_app.ps1
└── ...
```

The exact structure may vary depending on the current project implementation.

---

## Why SentenceTransformers?

SentenceTransformers provides a practical way to convert sentences and text into dense vector representations.

These representations can then be compared using vector similarity techniques.

In this project:

```text
Text
 ↓
SentenceTransformer
 ↓
Embedding Vector
```

The same process is applied to the user's search query before performing vector search.

---

## Why FAISS?

FAISS is designed for efficient similarity search over dense vectors.

In this application, FAISS acts as the vector search layer:

```text
Document Embeddings
        ↓
    FAISS Index
        ↓
   Similarity Search
        ↓
 Relevant Results
```

This combination makes SentenceTransformers + FAISS a useful foundation for semantic retrieval applications.

---

## Advantages

- Simple architecture
- Fast local vector search
- No external LLM API required for the core semantic search workflow
- Interactive Streamlit interface
- Easy to experiment with different embedding models
- Suitable for structured text-based datasets

---

## Limitations

- The application searches one uploaded document at a time. :contentReference[oaicite:11]{index=11}
- The input document must follow the expected Question/Answer format. :contentReference[oaicite:12]{index=12}
- Search quality depends on the selected embedding model and document quality.
- Very large documents may require additional memory and processing resources.
- The current project is focused on semantic retrieval rather than full conversational AI generation.

---

## Potential Use Cases

This architecture can be adapted for:

- 📚 FAQ search systems
- 🎓 Educational content retrieval
- 📖 Knowledge-base search
- 🏢 Internal document search
- 💬 FAQ assistants
- 🔎 Research content retrieval
- 🧑‍💻 Technical documentation search
- 📋 Structured question-answer datasets

---

## Future Improvements

Potential enhancements include:

- 📚 Multi-document semantic search
- 🗂️ Document collection management
- 💾 Persistent FAISS indexes
- 🔍 Advanced metadata filtering
- 📊 Similarity score visualization
- 🧠 Reranking of retrieved results
- 💬 LLM-powered answer generation
- 📑 Support for additional document formats
- 🔄 Automatic document indexing
- 🌐 Web-based knowledge integration
- 📈 Search analytics
- 🎯 Configurable retrieval parameters

---

## Learning Objectives

This project demonstrates practical concepts including:

- Semantic search
- Text embeddings
- SentenceTransformers
- Vector databases/indexes
- FAISS similarity search
- Document parsing
- Streamlit application development
- Information retrieval
- Vector-based ranking

---

## Security & Privacy

The project does not require an external AI API key for its core semantic-search workflow.

However, users should still review the handling of uploaded documents before deploying the application publicly.

For production deployments, consider implementing:

- Authentication
- Authorization
- Secure file handling
- File-size limits
- Input validation
- Access controls
- Data retention policies
- Encryption where appropriate

---

## Recommended Environment

For Windows:

```text
Python 3.11
```

Python 3.11 is recommended in the project documentation for a smoother FAISS setup. :contentReference[oaicite:13]{index=13}

---

## Project Highlights

### 🔎 Semantic Retrieval

Searches based on semantic similarity rather than relying exclusively on exact keyword matches.

### 🧠 Transformer Embeddings

Uses SentenceTransformers to generate meaningful vector representations of text.

### ⚡ Efficient Vector Search

Uses FAISS for fast similarity-based retrieval.

### 🖥️ Interactive Interface

Provides a Streamlit interface for document upload and semantic search.

### 💻 Local Architecture

The core search workflow can run locally without requiring an external LLM API.

---

## License

This project is available under the license included in this repository.

---

## Author

**Darshan S**

GitHub:

```text
https://github.com/DarshanS2004
```

---

## Conclusion

**Semantic Search Engine** demonstrates the fundamentals of modern vector-based information retrieval by combining **SentenceTransformers embeddings** with **FAISS similarity search** inside an interactive Streamlit application.

The project provides a simple foundation for building more advanced semantic search, knowledge retrieval, and document intelligence systems.