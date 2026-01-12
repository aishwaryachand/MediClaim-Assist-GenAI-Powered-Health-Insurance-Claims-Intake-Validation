import os
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

POLICY_FOLDER = "data/policies"


def load_policy_texts():
    texts = []

    for file in os.listdir(POLICY_FOLDER):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(POLICY_FOLDER, file))
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)

    return texts


def build_policy_vectorstore():
    policy_texts = load_policy_texts()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text("\n".join(policy_texts))

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore
