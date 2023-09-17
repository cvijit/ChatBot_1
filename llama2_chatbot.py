import streamlit as st
import replicate
import os
import io
from PyPDF2 import PdfFileReader

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate Credentials
# ... (Your existing code for credentials)

# ...

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfFileReader(uploaded_file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page_num).extractText()
    return text

# ...

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Check if the uploaded file is a PDF
if 'file' in st.session_state and st.session_state.file.type == 'application/pdf':
    with st.spinner("Extracting text from the PDF..."):
        pdf_text = extract_text_from_pdf(st.session_state.file)
        st.session_state.messages.append({"role": "user", "content": "I uploaded a PDF file."})
        st.session_state.messages.append({"role": "assistant", "content": "Analyzing the PDF..."})
        st.session_state.messages.append({"role": "user", "content": pdf_text})
        st.session_state.file = None  # Clear the uploaded file to avoid reprocessing

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(pdf_text)  # Use the extracted PDF text as input
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
