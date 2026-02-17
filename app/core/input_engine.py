import re
import base64
from dataclasses import dataclass, field
from typing import List

@dataclass
class InputInspectionResult:
    input_text: str
    flags: List[str] = field(default_factory=list)
    score: int = 0

KEYWORDS = {
    "ignore all": "instruction_override",
    "forget previous": "instruction_override",
    "system prompt": "system_extraction",
    "reveal internal": "system_extraction",
    "dan": "role_escalation",
    "do anything now": "role_escalation",
    "phishing": "policy_bypass",
    "malware": "policy_bypass",
    "nuclear": "high_criticality",
    "bomb": "high_criticality",
    "explosive": "high_criticality",
    "weapon": "high_criticality",
    "admin password": "role_escalation",
    "override security": "role_escalation"
}

LEET_MAP = {'4': 'a', '@': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's', '$': 's', '7': 't', '+': 't', '8': 'b'}

def normalize_text(text: str) -> str:
    """Cleans text of leetspeak and symbols for keyword matching."""
    text = text.lower()
    for char, replacement in LEET_MAP.items():
        text = text.replace(char, replacement)
    return re.sub(r'[^a-z\s]', '', text)

def inspect_input(text: str) -> InputInspectionResult:
    found_flags = set()

    clean_text = normalize_text(text)
    for word, flag in KEYWORDS.items():
        if word in clean_text:
            found_flags.add(flag)

    encoded_match = re.search(r'[A-Za-z0-9+/]{20,}', text)
    if encoded_match:
        try:
            decoded_text = normalize_text(base64.b64decode(encoded_match.group()).decode('utf-8'))
            for word, flag in KEYWORDS.items():
                if word in decoded_text:
                    found_flags.add("encoded_payload_malicious")
            if not found_flags:
                found_flags.add("encoded_payload")
        except:
            pass

    return InputInspectionResult(input_text=text, flags=list(found_flags))