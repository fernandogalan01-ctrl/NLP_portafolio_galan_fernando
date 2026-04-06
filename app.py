import streamlit as st
from PyPDF2 import PdfReader
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
st.set_page_config(page_title="Local DocQ&A")
st.title("Local Document Q&A Assistant")
st.write("Upload a PDF document and ask questions based on its context. Powered entirely by local LLMs via Ollama.")
# Preprocessing: PDF to Text 
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
# Preprocessing: Text Chunking
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_text(text)
# 
def get_vector_store(text_chunks):
    # Using Nomic embeddings via Ollama for local processing
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store
