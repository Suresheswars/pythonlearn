import streamlit as st
from dotenv import load_dotenv
import os

# ✅ LangChain imports (latest)
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

# ✅ Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 🎨 Streamlit App UI
st.set_page_config(page_title="Chat with your PDF — RAG + LangChain", page_icon="📄", layout="wide")

st.title("📄 Chat with your PDF using LangChain + OpenAI")
st.caption("Upload a PDF and start asking questions about it.")

# 📁 File Uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    # Save uploaded file temporarily
    pdf_path = "temp.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ PDF uploaded successfully!")

    # Load and split PDF
    with st.spinner("📖 Reading and splitting the document..."):
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = splitter.split_documents(pages)
        st.info(f"Document split into {len(docs)} chunks.")

    # Create embeddings + vector DB
    with st.spinner("🧠 Creating embeddings..."):
        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        db = FAISS.from_documents(docs, embeddings)
        st.success("✅ Vector database created successfully!")

    # Build the conversational chain
    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.3)
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User query input
    query = st.text_input("💬 Ask a question about your PDF:")

    # if query:
    #     with st.spinner("🤔 Thinking..."):
    #         result = qa_chain({"question": query, "chat_history": st.session_state.chat_history})
    #         st.session_state.chat_history.append((query, result["answer"]))
    #         st.markdown(f"**🤖 Answer:** {result['answer']}")
    if query:
        with st.spinner("🤔 Thinking..."):
        # 🧠 Updated for LangChain >= 0.1.0
            result = qa_chain.invoke({"question": query, "chat_history": st.session_state.chat_history})
            st.session_state.chat_history.append((query, result["answer"]))
            st.markdown(f"**🤖 Answer:** {result['answer']}")


    # Show chat history
    if st.session_state.chat_history:
        st.markdown("### 🧾 Chat History")
        for i, (q, a) in enumerate(st.session_state.chat_history):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**A{i+1}:** {a}")
