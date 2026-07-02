# 📚 AI-Powered Multi-PDF RAG Chatbot

An AI-powered chatbot that allows users to upload multiple PDF documents and ask questions in natural language using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📄 Upload Multiple PDFs
- 🤖 AI-powered Question Answering
- 🧠 Conversation Memory
- 💬 ChatGPT-style Chat Interface
- 🔍 MMR Retrieval
- 📚 Source Citation with Page Number
- ⚡ Fast Semantic Search using ChromaDB
- 🧩 Mistral Embeddings
- 🌐 Streamlit UI

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- ChromaDB
- Mistral AI
- PyPDF
- Python Dotenv

---

## 📂 Project Structure

```
multi-pdf-rag-chatbot/

│── app.py
│── create_database.py
│── main.py
│── requirements.txt
│── .gitignore
│── .env.example

│── document_loaders/
│── uploads/
│── chroma_db/
```

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-pdf-rag-chatbot.git
```

Move inside folder

```bash
cd multi-pdf-rag-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a .env file

```env
MISTRAL_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

## 💡 How It Works

1. Upload one or more PDF documents.

2. PDFs are split into chunks.

3. Embeddings are generated using Mistral AI.

4. Chunks are stored in ChromaDB.

5. User asks a question.

6. Relevant chunks are retrieved using MMR.

7. LLM generates the final answer.

8. Sources and page numbers are displayed.

---

## 🎯 Future Improvements

- Streaming Responses
- Voice Input
- Dark Mode
- Authentication
- Cloud Database
- Docker Deployment

---

## 👩‍💻 Author

**Disha Agrawal**

B.Tech Information Technology

Oriental Institute of Science & Technology
