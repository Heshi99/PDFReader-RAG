import pdfplumber
import faiss
import pickle
from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
VECTOR_DB_PATH = 'faiss_index'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load better embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load better QA model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def process_and_store_pdf(pdf_path):
    """Process the PDF and store embeddings in FAISS"""
    text = extract_text_from_pdf(pdf_path)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = text_splitter.split_text(text)
    
    vector_store = FAISS.from_texts(texts, embeddings)
    faiss.write_index(vector_store.index, VECTOR_DB_PATH)
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vector_store, f)
    return "PDF processed successfully"

def load_vector_store():
    """Load the FAISS vector store"""
    if not os.path.exists("vectorstore.pkl"):
        return None
    with open("vectorstore.pkl", "rb") as f:
        return pickle.load(f)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    process_and_store_pdf(file_path)
    return jsonify({"message": "PDF uploaded and processed successfully"})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    
    vector_store = load_vector_store()
    if vector_store is None:
        return jsonify({"error": "No documents available. Upload a PDF first."})
    
    retrieved_docs = vector_store.similarity_search(question, k=3)
    
    # Debugging: Print retrieved text
    print("Retrieved Chunks:")
    for doc in retrieved_docs:
        print(doc.page_content)
    
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    
    qa_result = qa_pipeline({"question": question, "context": context})
    return jsonify({"answer": qa_result["answer"]})

if __name__ == '__main__':
    app.run(debug=True)
