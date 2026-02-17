from app.core.input_engine import InputInspectionResult
WEIGHTS = {
    "high_criticality": 100,  
    "encoded_payload_malicious": 90, 
    "system_extraction": 70,
    "instruction_override": 65,
    "role_escalation": 60,
    "policy_bypass": 55,
    "encoded_payload": 35 
}

def calculate_risk(inspection: InputInspectionResult, embedding_results: dict) -> int:

    pattern_score = max([WEIGHTS.get(f, 0) for f in inspection.flags]) if inspection.flags else 0

    raw_sim = embedding_results.get("similarity_score", 0.0)
    semantic_score = 100 if raw_sim > 0.7 else raw_sim * 110

    if pattern_score >= 100:
        final_risk = 100
    elif pattern_score > 0:
        final_risk = max(pattern_score, semantic_score + 20 if raw_sim > 0.4 else semantic_score)
    else:
        final_risk = semantic_score

    final_risk = int(min(100, max(0, final_risk)))
    inspection.score = final_risk
    return final_risk