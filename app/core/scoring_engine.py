from app.core.input_engine import InputInspectionResult

WEIGHTS = {
    "instruction_override": 55, 
    "system_extraction": 60,
    "role_escalation": 45,
    "tool_coercion": 35,
    "policy_bypass": 40,
    "encoded_payload": 30
}

def calculate_risk(inspection: InputInspectionResult, embedding_results: dict) -> int:
    """
    Tuned Hybrid Scoring to catch 'lead developer' and 'ignore rules' attacks.
    """
    pattern_score = sum(WEIGHTS.get(flag, 0) for flag in inspection.flags)

    raw_similarity = embedding_results.get("similarity_score", 0.0)
    if raw_similarity > 0.8:
        semantic_score = 100
    elif raw_similarity > 0.6:
        semantic_score = raw_similarity * 110
    else:
        semantic_score = raw_similarity * 100

    if len(inspection.flags) > 0:
        final_score = (pattern_score * 0.7) + (semantic_score * 0.3)
    else:
        final_score = semantic_score


    if len(inspection.flags) > 0 and raw_similarity > 0.5:
        final_score = max(final_score, 85)

    final_risk = int(min(100, max(0, final_score)))
    inspection.score = final_risk
    return final_risk