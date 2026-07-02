# import os
# import streamlit as st
# from dotenv import load_dotenv

# from langchain_community.vectorstores import Chroma
# from langchain_mistralai import ChatMistralAI
# from langchain_mistralai import MistralAIEmbeddings
# from langchain_core.prompts import ChatPromptTemplate

# from create_database import create_vector_database

# load_dotenv()

# st.set_page_config(
#     page_title="Multi PDF Chatbot",
#     page_icon="📚",
#     layout="wide"
# )

# st.title("📚 Multi PDF Chatbot")

# uploaded_files = st.file_uploader(
#     "Upload PDF(s)",
#     type="pdf",
#     accept_multiple_files=True
# )

# if uploaded_files:

#     os.makedirs("uploads", exist_ok=True)

#     pdf_paths = []

#     for uploaded_file in uploaded_files:

#         pdf_path = os.path.join(
#             "uploads",
#             uploaded_file.name
#         )

#         with open(pdf_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         pdf_paths.append(pdf_path)

#     st.write("### Uploaded PDFs")

#     for file in uploaded_files:
#         st.write("✅", file.name)

#     if st.button("Create Knowledge Base"):
#         print("Calling Function...")
#         print(pdf_paths)

#         with st.spinner("Creating Embeddings..."):

#             create_vector_database(pdf_paths)

#         st.success("Knowledge Base Created!")

#         st.session_state["db_ready"] = True


# if st.session_state.get("db_ready", False):

#     embedding_model = MistralAIEmbeddings(
#         model="mistral-embed"
#     )

#     vectorstore = Chroma(
#         persist_directory="chroma_db",
#         embedding_function=embedding_model
#     )

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k": 4,
#             "fetch_k": 10,
#             "lambda_mult": 0.5
#         }
#     )

#     llm = ChatMistralAI(
#         model="mistral-small-2506"
#     )

#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """
# You are a helpful AI assistant.

# Use ONLY the provided context.

# If the answer is not present in the context,
# say:
# 'I could not find the answer in the uploaded documents.'
# """
#         ),
#         (
#             "human",
#             """
# Context:
# {context}

# Question:
# {question}
# """
#         )
#     ])

#     question = st.text_input("Ask a Question")

#     if st.button("Ask"):

#         docs = retriever.invoke(question)

#         context = "\n\n".join(
#             [doc.page_content for doc in docs]
#         )

#         final_prompt = prompt.invoke({
#             "context": context,
#             "question": question
#         })

#         with st.spinner("Thinking..."):

#             response = llm.invoke(final_prompt)

#         st.subheader("Answer")

#         st.write(response.content)

#         with st.expander("Retrieved Chunks"):

#             for i, doc in enumerate(docs, start=1):

#                 st.markdown(f"### Chunk {i}")

#                 st.write("📄 Source :", doc.metadata.get("source"))

#                 st.write("📃 Page :", doc.metadata.get("page"))

#                 st.write(doc.page_content)

#                 st.divider()

import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

from create_database import create_vector_database

load_dotenv()
st.set_page_config(
    page_title="Multi PDF Chatbot",
    page_icon="📚",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("📚 Multi PDF Chatbot")

uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("uploads", exist_ok=True)

    pdf_paths = []

    for uploaded_file in uploaded_files:

        pdf_path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        pdf_paths.append(pdf_path)

    st.write("### Uploaded PDFs")

    for file in uploaded_files:
        st.write("✅", file.name)

    if st.button("Create Knowledge Base"):
        print("Calling Function...")
        print(pdf_paths)

        with st.spinner("Creating Embeddings..."):

            create_vector_database(pdf_paths)

        st.success("Knowledge Base Created!")

        st.session_state["db_ready"] = True


if st.session_state.get("db_ready", False):

    embedding_model = MistralAIEmbeddings(
        model="mistral-embed"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10,
            "lambda_mult": 0.5
        }
    )

    llm = ChatMistralAI(
        model="mistral-small-2506"
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a helpful AI assistant.

Use ONLY the provided context.

If the answer is not present in the context,
say:
'I could not find the answer in the uploaded documents.'
"""
        ),
        (
            "human",
            """

        Previous Conversation:
        {history}    
        Context:
        {context}

        Question:
        {question}
        """
        )
    ])

# Display previous chat

    for message in st.session_state.messages:

       with st.chat_message(message["role"]):
        st.markdown(message["content"])

    question = st.chat_input("Ask anything about your PDFs...")

    if question:

        st.session_state.messages.append(
           {
              "role": "user",
              "content": question
            }
        )

        with st.chat_message("user"):
          st.markdown(question)

        docs = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )
        conversation_history = ""

        for message in st.session_state.messages[-6:]:

            conversation_history += (
                f"{message['role'].capitalize()}: {message['content']}\n"
            )
        final_prompt = prompt.invoke({
            "history": conversation_history,
            "context": context,
            "question": question
        })

        with st.spinner("Thinking..."):

            response = llm.invoke(final_prompt)

        with st.chat_message("assistant"):

            st.markdown(response.content)

        st.session_state.messages.append(
                {
                  "role": "assistant",
                  "content": response.content
              }
            )


        with st.expander("Retrieved Chunks"):

            for i, doc in enumerate(docs, start=1):

             st.markdown(f"### 📄 Source {i}")

             col1, col2 = st.columns(2)

             with col1:
               st.info(f"📄 {doc.metadata.get('source')}")

             with col2:
                st.success(f"📃 Page {doc.metadata.get('page')}")

             st.write(doc.page_content)

             st.divider()