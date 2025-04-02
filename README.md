This repository implements a PDF Question-Answering System using a Retrieval-Augmented Generation (RAG) approach. The system allows users to upload PDF documents, extract text from them, index the content, and then answer questions based on the document's content. It uses Hugging Face's transformers, FAISS for similarity search, and Streamlit for the front-end interface.

Tech Stack ⚙️
--
Frontend 🌐:

Streamlit: A fast way to create custom web applications for machine learning and data science.

Backend 🔧:

Flask: A lightweight Python web framework for building RESTful APIs.

PyPDF2: A Python library for PDF file handling and text extraction.

Transformers: Hugging Face’s library for Natural Language Processing tasks, such as Question Answering (QA).

Langchain: For managing text embedding and building vector databases.

FAISS: Facebook’s library for efficient similarity search and clustering of dense vectors.

HuggingFaceEmbeddings: To generate vector embeddings for the text in the documents.


Features
--
**PDF Upload**: Users can upload a PDF document to the system.

**Text Extraction**: The system extracts the text from the PDF.

**Text Indexing**: The extracted text is split into chunks and indexed using FAISS for fast similarity search.

**Question-Answering**: Users can ask questions based on the document, and the system will retrieve relevant chunks and generate an answer using a pre-trained language model.

How it Works
--

**Upload PDF**: The user uploads a PDF file through the front-end interface.

**Text Extraction & Indexing**: The PDF content is extracted and indexed using FAISS.

**Ask Questions**: Users can ask questions related to the document.

**Answer Retrieval**: The system retrieves relevant text chunks and uses the Hugging Face pipeline to answer the question.


How to Run the Application
--
Backend (Flask API)

Navigate to the folder where your backend.py file is located.

Run the backend Flask server - > python backend.py

Frontend (Streamlit app)

Navigate to the folder where your frontend.py file is located.
Run the streamlit app -> streamlit run frontend.py


