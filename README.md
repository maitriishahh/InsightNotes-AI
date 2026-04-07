# 🎥 AI YouTube Video Summarizer 
### AI-Powered YouTube & Audio Knowledge Extraction System  

AI YouTube Video Summarizer is an end-to-end **GenAI + Retrieval-Augmented Generation (RAG)** application that converts long-form YouTube videos and audio files into structured notes and enables cross-video knowledge querying with grounded, hallucination-resistant answers.



## 🚀 Features

### 📥 Multi-Source Input
- YouTube URL processing *(Cloud deployments may restrict direct media downloads due to network policies.)*
- Local audio/video upload (`.mp3`, `.mp4`, `.wav`)  
- Automatic audio extraction for video files



### 🧠 AI-Powered Processing Pipeline
- Whisper-based transcription  
- LLM-based content classification (Lecture / Podcast / Meeting / General)  
- Chunked structured summarization  
- Rate-limited Groq API integration  



### 🔎 Retrieval-Augmented Generation (RAG)
- Local embeddings via SentenceTransformers  
- FAISS vector similarity search  
- Cross-video semantic querying  
- Relevance threshold filtering (reduces hallucination)  
- Strict grounded answering (no external knowledge used)  



### 📚 Knowledge Base
- Stores transcript + structured notes  
- Indexed per video  
- Supports cross-video comparison queries  
- Source references included in answers  



### 📄 Export
- One-click PDF export  
- Automatically downloaded  
- Saved under `storage/exports`  



### 🔗 YouTube Deep Linking
- Extracts `youtube_id`  
- Clickable YouTube link in saved notes  



## 🏗️ Architecture Overview
```
User Input (YouTube URL / File Upload)
            ↓
    Audio Extraction
            ↓
    Transcription (Whisper)
            ↓
    Classification (LLM)
            ↓
    Chunked Summarization
            ↓
    SQLite Storage
            ↓
    Embeddings Generation
            ↓
    FAISS Indexing
            ↓
    RAG Query Engine
```


## 🧩 Tech Stack

- **Frontend:** Streamlit  
- **LLM (Summarization + RAG):** Groq (llama-3.1-8b-instant)  
- **Transcription:** Faster-Whisper  
- **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)  
- **Vector Store:** FAISS  
- **Database:** SQLite  
- **PDF Export:** FPDF  
- **Rate Limiting:** Custom exponential backoff wrapper  


## 📁 Project Structure

```
AI YouTube Video Summarizer/
│
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── classifier.py
│   ├── input_handler.py
│   ├── audio_extractor.py
│   └── chunking.py
│
├── database/
│   ├── db.py
│   ├── crud.py
│   └── models.py
│
├── rag/
│   ├── embeddings.py
│   ├── vector_store.py
│   └── search.py
│
├── utils/
│   ├── rate_limiter.py
│   └── pdf_export.py
│
├── storage/
│   ├── audio/
│   └── exports/
│
├── app.py
└── requirements.txt
```



## ⚙️ Installation

### 1. Clone the repository

```bash
git https://github.com/maitriishahh/AI-YouTube-Video-Summarizer.git
cd AI YouTube Video Summarizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```


## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key_here
```



## 🎯 Key Highlights
- End-to-end GenAI system

- Local vector storage (privacy-friendly)

- Cross-video semantic intelligence

- Hallucination-resistant answering

- Modular and production-ready architecture

## 👩‍💻 Author
## Maitri Shah
