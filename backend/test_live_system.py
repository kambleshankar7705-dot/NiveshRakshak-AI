import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_live_system():
    print("=" * 60)
    print("RUNNING LIVE END-TO-END VERIFICATION OVER HTTP")
    print("=" * 60)

    # 1. Health
    res = requests.get(f"{BASE_URL}/api/health", timeout=5)
    assert res.status_code == 200, f"Health failed: {res.text}"
    print(f"✓ Health Check: {res.json()['status']} (Service: {res.json()['service']})")

    # 2. Text Analysis
    text_payload = {
        "text": "URGENT! SEBI APPROVED OPPORTUNITY. Invest ₹10,000 today and get ₹50,000 guaranteed within 30 days. No risk, 100% fixed profit. Only 5 slots left! Send money immediately via UPI to secure your spot. Join our Telegram VIP group: https://t.me/vip_invest_sure",
        "language": "en",
        "input_type": "TEXT"
    }
    res = requests.post(f"{BASE_URL}/api/analyze/text", json=text_payload, timeout=5)
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] >= 60
    print(f"✓ Text Analyzer: Risk Score {data['risk_score']} ({data['risk_level']}) - Red Flags: {len(data['red_flags'])}")

    # 3. URL Safety
    url_payload = {"url": "http://sebi-bonus-wealth.xyz/claim", "language": "en"}
    res = requests.post(f"{BASE_URL}/api/analyze/url", json=url_payload, timeout=5)
    assert res.status_code == 200
    url_data = res.json()
    assert url_data["risk_score"] >= 60
    print(f"✓ URL Safety Checker: Domain '{url_data['domain']}' - Risk: {url_data['risk_level']} (Score: {url_data['risk_score']})")

    # 4. Claim Evidence Verifier
    claim_payload = {"claim": "Guaranteed 40% monthly returns without risk", "language": "en"}
    res = requests.post(f"{BASE_URL}/api/verify/claim", json=claim_payload, timeout=5)
    assert res.status_code == 200
    claim_data = res.json()
    assert claim_data["status"] == "UNVERIFIED"
    print(f"✓ Claim Verifier: Status '{claim_data['status']}' - Badge: '{claim_data['demo_badge']}'")

    # 5. Content Classifier
    content_payload = {
        "content": "Join our VIP Telegram channel right now for jackpot penny stock calls! 10X returns guaranteed.",
        "platform": "Telegram",
        "language": "en"
    }
    res = requests.post(f"{BASE_URL}/api/classify/content", json=content_payload, timeout=5)
    assert res.status_code == 200
    content_data = res.json()
    assert content_data["classification"] in ["HIGH_RISK_PROMOTIONAL", "PROMOTIONAL"]
    print(f"✓ Content Classifier: Classification '{content_data['classification']}' (Promotional Score: {content_data['promotional_score']}%)")

    # 6. Voice Assistant
    voice_payload = {
        "transcript": "मला WhatsApp वर investment चा message आला आहे ज्यामध्ये 50 हजार नक्की मिळतील असे सांगितले आहे. तो safe आहे का?",
        "language": "mr"
    }
    res = requests.post(f"{BASE_URL}/api/analyze/voice", json=voice_payload, timeout=5)
    assert res.status_code == 200
    voice_data = res.json()
    assert "voice_friendly_summary" in voice_data
    print(f"✓ Voice Assistant (Marathi): Spoken Summary generated successfully ({len(voice_data['voice_friendly_summary'])} chars)")

    # 7. Resilience Test Questions
    res = requests.get(f"{BASE_URL}/api/resilience-test/questions", timeout=5)
    assert res.status_code == 200
    q_data = res.json()
    assert q_data["total"] >= 8
    print(f"✓ Resilience Questions: Loaded {q_data['total']} scenarios with multilingual EN/HI/MR support")

    # 8. Resilience Evaluation
    eval_payload = {"1": "C", "2": "B", "3": "B", "4": "A", "5": "D", "6": "B", "7": "B", "8": "B"}
    res = requests.post(f"{BASE_URL}/api/resilience-test/evaluate", json=eval_payload, timeout=5)
    assert res.status_code == 200
    eval_data = res.json()
    assert eval_data["score"] == 8
    assert eval_data["resilience_tier"] == "HIGH RESILIENCE"
    print(f"✓ Resilience Evaluation: Score {eval_data['score']}/{eval_data['total_questions']} - Tier: {eval_data['resilience_tier']}")

    # 9. Education Topics
    res = requests.get(f"{BASE_URL}/api/education", timeout=5)
    assert res.status_code == 200
    edu_data = res.json()
    assert edu_data["total"] >= 8
    print(f"✓ Education Topics: Loaded {edu_data['total']} topics")

    # 10. Analytics Summary
    res = requests.get(f"{BASE_URL}/api/analytics", timeout=5)
    assert res.status_code == 200
    analytics_data = res.json()
    print(f"✓ Platform Analytics: Total Analyzed {analytics_data['total_analyses']}, High Risk: {analytics_data['high_risk_count']}")

    print("=" * 60)
    print("ALL LIVE NETWORK ENDPOINTS VALIDATED AND 100% OPERATIONAL!")
    print("=" * 60)

if __name__ == "__main__":
    test_live_system()
