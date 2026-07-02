import os
import shutil

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def create_vector_database(pdf_paths):

    print("=" * 50)
    print("Function called")
    print("pdf_paths =", pdf_paths)
    print("=" * 50)

    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")

    

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=10
    )

    all_chunks = []

    # Process every uploaded PDF
    for pdf_path in pdf_paths:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        chunks = splitter.split_documents(docs)

        # Save PDF name
        for chunk in chunks:
            chunk.metadata["source"] = os.path.basename(pdf_path)

        all_chunks.extend(chunks)

    embedding_model = MistralAIEmbeddings(
        model="mistral-embed"
    )

    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    return vectorstore