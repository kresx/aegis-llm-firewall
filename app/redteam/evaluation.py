import requests
import json
import time
from typing import List, Dict

API_URL = "http://127.0.0.1:8000/chat"

def run_security_audit(test_file: str = "data/jailbreak_dataset.json"):
    with open(test_file, 'r') as f:
        attacks = json.load(f)

    results = []
    print(f"Starting Security Audit on {len(attacks)} attack vectors")

    for attack in attacks:
        payload = {"user_input": attack["prompt"]}
        start_time = time.perf_counter()
        
        try:
            response = requests.post(API_URL, json=payload)
            latency = (time.perf_counter() - start_time) * 1000
            if response.status_code == 403:
                data = response.json()["detail"]
                results.append({
                    "prompt": attack["prompt"],
                    "category": attack["category"],
                    "detected": True,
                    "risk_score": data["risk_score"],
                    "latency": latency
                })
            else:
                results.append({
                    "prompt": attack["prompt"],
                    "category": attack["category"],
                    "detected": False,
                    "risk_score": response.json().get("risk_score", 0),
                    "latency": latency
                })
        except Exception as e:
            print(f"Error testing prompt: {e}")

    generate_report(results)

def generate_report(results: List[Dict]):
    total = len(results)
    caught = sum(1 for r in results if r["detected"])
    leaked = total - caught
    accuracy = (caught / total) * 100

    print("\n" + "="*40)
    print("AEGIS-LAF SECURITY AUDIT REPORT")
    print("="*40)
    print(f"Total Attacks Tested: {total}")
    print(f"Successfully Blocked: {caught}")
    print(f"System Leaks (Failed): {leaked}")
    print(f"Overall Protection Rate: {accuracy:.2f}%")
    print(f"Avg Detection Latency: {sum(r['latency'] for r in results)/total:.2f}ms")
    print("="*40)

if __name__ == "__main__":
    run_security_audit()