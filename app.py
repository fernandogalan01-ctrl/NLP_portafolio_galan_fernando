import streamlit as st
from PyPDF2 import PdfReader
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
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
# Processing: Retrieval + Prompt Engineering + Local LLM Generation
def process_question(user_question, vector_store):
    # Retrieval
    docs = vector_store.similarity_search(user_question, k=3)
    context = "".join([doc.page_content for doc in docs])
    # Prompt Engineering 
    template = """
    Use the following pieces of context to answer the question at the end. 
    If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
    Context:
    {context}
    Question: {question}
    Helpful Answer:"""
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    # Local LLM Generation with Ollama
    llm = OllamaLLM(model="llama3.2")
    chain = prompt | llm
    # Invoke the chain with the retrieved context and user question
    response = chain.invoke({"context": context, "question": user_question})
    return response
# Streamlit UI
with st.sidebar:
    st.subheader("Your Documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing..."):
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            st.session_state.vector_store = get_vector_store(text_chunks)
            st.success("Processing Complete!")
user_question = st.text_input("Ask a question about your documents:")
if user_question and "vector_store" in st.session_state:
    with st.spinner("Thinking..."):
        answer = process_question(user_question, st.session_state.vector_store)
        st.write("**Answer:**")
        st.write(answer)
elif user_question:
    st.warning("Please upload and process a document first.")