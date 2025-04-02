import streamlit as st
import requests
import os

st.title("PDF Question-Answering System")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file is not None:
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

    with st.spinner("Processing document..."):
        response = requests.post("http://127.0.0.1:5000/upload", files={"file": uploaded_file})
        if response.status_code == 200:
            st.success("Document processed and ready for questions!")
        else:
            st.error("Error processing the document.")

question = st.text_input("Ask a question about the document:")
if st.button("Get Answer"):
    if question:
        with st.spinner("Fetching answer..."):
            response = requests.post("http://127.0.0.1:5000/ask", json={"question": question})
            if response.status_code == 200:
                response_data = response.json()
                st.write("**Response Data:**", response_data)  # Print the entire response for debugging
                if "answer" in response_data:
                    st.write("**Answer:**", response_data["answer"])
                else:
                    st.error("No answer key in response.")
            else:
                st.error("Error fetching answer.")
