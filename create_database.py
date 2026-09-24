import os
import uuid
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
    

    db_path = f"chroma_db_{uuid.uuid4().hex}"
    # db_path = "chroma_db_new"

    # if os.path.exists("chroma_db"):
    #     try:
    #         shutil.rmtree("chroma_db")
    #     except PermissionError:
    #         print("chroma_db is locked.Please restart the app")
    #         return None    
       


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
        persist_directory=db_path
    )

    # return vectorstore

    return db_path