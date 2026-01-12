def assess_claim(policy_context: str):
    text = policy_context.lower()

    decision = "Needs Review"
    reasons = []
    explanation = ""
    missing_docs = []
    confidence = 0.5

    # Case 1: Policy / informational document instead of claim
    if any(x in text for x in ["right to examine", "policy overview", "terms and conditions"]):
        decision = "Needs Review"
        explanation = (
            "The uploaded document appears to be a policy or informational document "
            "rather than an itemized medical claim. Manual review is required to verify "
            "eligible expenses and supporting documentation."
        )
        reasons.append("Document is not a medical invoice or claim bill")
        missing_docs.append("Itemized medical bill")
        confidence = 0.6

    # Case 2: Explicit exclusion language
    elif any(x in text for x in ["not covered", "exclusion", "excluded"]):
        decision = "Likely Not Covered"
        explanation = (
            "The retrieved policy sections contain exclusion language indicating "
            "that the claimed services may not be eligible for reimbursement."
        )
        reasons.append("Policy exclusion identified")
        confidence = 0.75

    # Case 3: Coverage language found
    elif any(x in text for x in ["covered", "eligible", "reimbursable"]):
        decision = "Likely Covered"
        explanation = (
            "The retrieved policy sections indicate that the claimed services "
            "may be eligible for coverage, subject to verification of documentation."
        )
        reasons.append("Coverage language detected in policy")
        confidence = 0.8

    else:
        explanation = (
            "The policy context does not provide sufficient information to "
            "automatically determine coverage. Manual review is recommended."
        )

    return {
        "decision": decision,
        "reasons": reasons,
        "explanation": explanation,
        "missing_documents": missing_docs,
        "confidence": confidence
    }

