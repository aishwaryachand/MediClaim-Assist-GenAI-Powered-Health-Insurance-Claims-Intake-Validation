import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from backend.claim_processor import process_claim



st.set_page_config(
    page_title="MediClaim Assist",
    layout="centered"
)


st.title("MediClaim Assist")
st.caption("GenAI-Powered Health Insurance Claims Intake & Validation")

st.markdown(
    """
    Upload a health insurance claim document to receive a
    **policy-grounded, explainable assessment** that assists
    human reviewers in faster decision-making.
    """
)


uploaded_file = st.file_uploader(
    " Upload health insurance claim (PDF)",
    type=["pdf"]
)

# --- Processing ---
if uploaded_file:
    if st.button(" Process Claim"):
        with st.spinner("Analyzing claim and retrieving policy context..."):
            result = process_claim(uploaded_file)

        st.subheader(" AI Claim Assessment")

        assessment = result["assessment"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Decision", assessment["decision"])
        with col2:
            st.metric("Confidence", f"{assessment['confidence'] * 100:.0f}%")

        st.markdown("### 📝 Explanation")
        st.write(assessment["explanation"])

        if assessment["reasons"]:
            st.markdown("###  Key Signals")
            for r in assessment["reasons"]:
                st.write("•", r)

        if assessment["missing_documents"]:
            st.warning("### 📎 Missing Documents")
            for d in assessment["missing_documents"]:
                st.write("•", d)

        st.subheader(" Supporting Policy Evidence")
        st.text(result["policy_snippet"])

        # -------------------------------


        
        # Human Review 
  
        st.subheader(" Reviewer Action")
        st.radio(
            "Final Decision",
            ["Approve", "Escalate for Manual Review"]
        )
        st.text_area("Reviewer Notes", placeholder="Add optional review comments here...")
