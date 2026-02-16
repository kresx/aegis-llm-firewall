import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class InputInspectionResult:
    input_text: str
    flags: List[str] = field(default_factory=list)
    score: int = 0

KEYWORDS = {
    "ignore all": "instruction_override",
    "disregard": "instruction_override",
    "reveal": "system_extraction",
    "system prompt": "system_extraction",

    "lead developer": "role_escalation",
    "administrator": "role_escalation",
    "commander": "role_escalation",
    "leader": "role_escalation",
    "boss": "role_escalation",
    
    "nuclear": "policy_bypass",
    "bomb": "policy_bypass",
    "explosive": "policy_bypass",
    "weapon": "policy_bypass",
    "malware": "policy_bypass",
    "crack": "tool_coercion"
}

def inspect_input(text: str) -> InputInspectionResult:
    text_lower = text.lower()
    found_flags = set()

    for word, flag in KEYWORDS.items():
        if word in text_lower:
            found_flags.add(flag)

    if re.search(r'[A-Za-z0-9+/]{20,}', text):
        found_flags.add("encoded_payload")

    return InputInspectionResult(input_text=text, flags=list(found_flags))