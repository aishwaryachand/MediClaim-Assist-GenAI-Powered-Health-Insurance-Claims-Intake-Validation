from pypdf import PdfReader
from backend.rag import build_policy_vectorstore
from backend.assessments import assess_claim

vectorstore = build_policy_vectorstore()


def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def process_claim(file):
    claim_text = extract_text(file)

    policy_docs = vectorstore.similarity_search(claim_text, k=3)
    policy_context = "\n\n".join([doc.page_content for doc in policy_docs])


    assessment = assess_claim(policy_context)

    return {
        "assessment": assessment,
        "policy_snippet": policy_context[:700],
        "citations": ["Policy documents"],
    }
