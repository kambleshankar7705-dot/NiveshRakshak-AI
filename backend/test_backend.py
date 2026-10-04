import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import io
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "NiveshRakshak AI"
    print("[PASS] Health Check Passed")

def test_analyze_text_scam():
    text = (
        "URGENT! SEBI APPROVED OPPORTUNITY. Invest ₹10,000 today and get ₹50,000 guaranteed "
        "within 30 days. No risk, 100% fixed profit. Only 5 slots left! Send money immediately via UPI to secure your spot. Join our Telegram VIP group: https://t.me/vip_invest_sure"
    )
    response = client.post("/api/analyze/text", json={"text": text, "language": "en", "input_type": "TEXT"})
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] >= 60
    assert data["risk_level"] in ["HIGH", "VERY_HIGH"]
    assert len(data["red_flags"]) >= 3
    assert "explanation" in data
    assert "explanation_hi" in data
    assert "explanation_mr" in data
    assert data["pause_advised"] is True
    print(f"[PASS] Text Analyzer (Scam) Passed - Score: {data['risk_score']} ({data['risk_level']})")

def test_analyze_text_educational():
    text = (
        "Investor Awareness Notice: Asset allocation and diversification help manage portfolio risk over the long term. "
        "Market securities are subject to market volatility. Mutual fund NAV fluctuates daily. Always read scheme-related documents carefully."
    )
    response = client.post("/api/analyze/text", json={"text": text, "language": "en", "input_type": "TEXT"})
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] <= 30
    assert data["risk_level"] == "LOW"
    assert data["content_type"] == "EDUCATIONAL"
    print(f"[PASS] Text Analyzer (Educational) Passed - Score: {data['risk_score']} ({data['risk_level']})")

def test_analyze_text_regional_languages():
    # Marathi scam
    mr_text = "नमस्कार! सेबी मान्यताप्राप्त खात्रीशीर योजना! फक्त ₹५,००० गुंतवा आणि दरमहा ₹२५,००० नक्की परतावा मिळवा. शेवटची संधी!"
    res_mr = client.post("/api/analyze/text", json={"text": mr_text, "language": "mr", "input_type": "TEXT"})
    assert res_mr.status_code == 200
    data_mr = res_mr.json()
    assert data_mr["risk_score"] >= 40
    assert "explanation_mr" in data_mr
    print(f"[PASS] Text Analyzer (Marathi) Passed - Score: {data_mr['risk_score']}")

    # Hindi scam
    hi_text = "अंतिम अवसर! सेबी अप्रूव्ड स्कीम। ₹10,000 निवेश करें और 30 दिनों में ₹1,00,000 पाएं। 100% गारंटीड रिटर्न। तुरंत पेमेंट करें।"
    res_hi = client.post("/api/analyze/text", json={"text": hi_text, "language": "hi", "input_type": "TEXT"})
    assert res_hi.status_code == 200
    data_hi = res_hi.json()
    assert data_hi["risk_score"] >= 40
    assert "explanation_hi" in data_hi
    print(f"[PASS] Text Analyzer (Hindi) Passed - Score: {data_hi['risk_score']}")

def test_analyze_image():
    # Generate a dummy test image
    img = Image.new("RGB", (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "SEBI Guaranteed return 100% profit WhatsApp Scam", fill=(0, 0, 0))
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    files = {"file": ("test_whatsapp_scam.png", img_bytes, "image/png")}
    data = {"language": "en", "auto_analyze": "true"}

    response = client.post("/api/analyze/image", files=files, data=data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert "extracted_text" in res_data
    assert "analysis" in res_data
    assert res_data["analysis"]["risk_score"] >= 50
    print(f"[PASS] Screenshot Analyzer Passed - Extracted: {res_data['extracted_text'][:40]}...")

def test_analyze_url():
    # Suspicious link
    suspicious_url = "http://sebi-authorized-wealth-guaranteed.xyz/deposit?ref=telegram_vip"
    res = client.post("/api/analyze/url", json={"url": suspicious_url, "language": "en"})
    assert res.status_code == 200
    data = res.json()
    assert data["risk_score"] >= 50
    assert data["risk_level"] in ["HIGH", "MEDIUM"]
    assert data["is_https"] is False
    print(f"[PASS] URL Safety Checker (Suspicious) Passed - Score: {data['risk_score']} ({data['risk_level']})")

    # Safe link
    safe_url = "https://www.sebi.gov.in"
    res_safe = client.post("/api/analyze/url", json={"url": safe_url, "language": "en"})
    assert res_safe.status_code == 200
    safe_data = res_safe.json()
    assert safe_data["is_https"] is True
    assert safe_data["risk_level"] == "LOW"
    print(f"[PASS] URL Safety Checker (Safe) Passed - Score: {safe_data['risk_score']}")

def test_classify_content():
    # Promotional post
    promo = "Guaranteed 10X return! Join our VIP Telegram channel right now for exclusive daily jackpot calls."
    res_promo = client.post("/api/classify/content", json={"content": promo, "platform": "Telegram", "language": "en"})
    assert res_promo.status_code == 200
    data_promo = res_promo.json()
    assert data_promo["classification"] in ["HIGH_RISK_PROMOTIONAL", "PROMOTIONAL"]
    print(f"[PASS] Content Classifier (Promotional) Passed: {data_promo['classification']}")

    # Educational post
    edu = "Diversification and asset allocation reduce concentration risk. Learn how mutual fund NAV works."
    res_edu = client.post("/api/classify/content", json={"content": edu, "platform": "YouTube", "language": "en"})
    assert res_edu.status_code == 200
    data_edu = res_edu.json()
    assert data_edu["classification"] == "EDUCATIONAL"
    print(f"[PASS] Content Classifier (Educational) Passed: {data_edu['classification']}")

def test_voice_assistant():
    transcript = "मला WhatsApp वर एक मेसेज आला आहे ज्यामध्ये 50 हजार नक्की मिळतील असे सांगितले आहे. हे खरे आहे का?"
    res = client.post("/api/analyze/voice", json={"transcript": transcript, "language": "mr"})
    assert res.status_code == 200
    data = res.json()
    assert "voice_friendly_summary" in data
    assert "analysis" in data
    assert data["detected_language"] == "mr"
    print(f"[PASS] Voice Assistant Passed - Summary: {data['voice_friendly_summary']}")

def test_verify_claim():
    claim = "ABC Securities is registered with SEBI as an official Research Analyst"
    res = client.post("/api/verify/claim", json={"claim": claim, "language": "en"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["UNVERIFIED", "INSUFFICIENT_EVIDENCE"]
    assert "needed_evidence" in data
    assert len(data["suggested_verification_steps"]) >= 2
    assert "demo_badge" in data
    print("[PASS] Claim Evidence Verification Passed")

def test_education_topics():
    res = client.get("/api/education")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 8
    first_topic = data["topics"][0]
    assert "title" in first_topic
    assert "title_hi" in first_topic
    assert "title_mr" in first_topic
    assert "everyday_analogy" in first_topic
    assert "quiz" in first_topic
    print(f"[PASS] Education Topics Passed - Loaded {data['total']} topics with EN/HI/MR support")

def test_resilience_test():
    # Fetch questions
    res_q = client.get("/api/resilience-test/questions")
    assert res_q.status_code == 200
    data_q = res_q.json()
    assert data_q["total"] >= 5
    print(f"[PASS] Resilience Questions Passed - Loaded {data_q['total']} questions")

    # Evaluate answers
    submission = {"1": "C", "2": "B", "3": "B", "4": "A"}
    res_eval = client.post("/api/resilience-test/evaluate", json=submission)
    assert res_eval.status_code == 200
    data_eval = res_eval.json()
    assert "score" in data_eval
    assert "resilience_tier" in data_eval
    assert "feedback" in data_eval
    print(f"[PASS] Resilience Evaluation Passed - Tier: {data_eval['resilience_tier']}")

def test_history_and_privacy():
    # Get history
    res_hist = client.get("/api/history")
    assert res_hist.status_code == 200
    data_hist = res_hist.json()
    assert "history" in data_hist
    assert "privacy_notice" in data_hist
    print(f"[PASS] History Retrieval Passed - Found {len(data_hist['history'])} records")

    # If there are records, test single delete
    if len(data_hist["history"]) > 0:
        first_id = data_hist["history"][0]["id"]
        res_del = client.delete(f"/api/history/{first_id}")
        assert res_del.status_code == 200
        print(f"[PASS] Single Record Deletion Passed for ID: {first_id}")

    # Test clear all history (Privacy Center guarantee)
    res_clear = client.delete("/api/history")
    assert res_clear.status_code == 200
    assert res_clear.json()["success"] is True
    print("[PASS] Clear All History (Privacy Center Action) Passed")

def test_demo_cases():
    res = client.get("/api/demo")
    assert res.status_code == 200
    data = res.json()
    assert len(data["cases"]) == 5
    assert data["cases"][0]["id"] == "demo-1"
    print(f"[PASS] Demo Cases Passed - Loaded {len(data['cases'])} scenarios")

def test_analytics():
    res = client.get("/api/analytics")
    assert res.status_code == 200
    data = res.json()
    assert "total_analyses" in data
    assert "high_risk_count" in data
    assert "common_red_flags" in data
    assert "language_usage" in data
    assert "input_channel_usage" in data
    print(f"[PASS] Analytics Passed - Total Aggregated Analyses: {data['total_analyses']}")

def test_edge_cases():
    # 1. Empty text
    res_empty = client.post("/api/analyze/text", json={"text": "", "language": "en", "input_type": "TEXT"})
    assert res_empty.status_code == 200
    assert res_empty.json()["risk_score"] == 0

    # 2. Very long text (50,000 characters)
    long_text = "Learn about investing in mutual funds. " * 1200
    res_long = client.post("/api/analyze/text", json={"text": long_text, "language": "en", "input_type": "TEXT"})
    assert res_long.status_code == 200

    # 3. Malformed / weird URL
    res_url = client.post("/api/analyze/url", json={"url": "not-a-valid-domain", "language": "en"})
    assert res_url.status_code == 200
    assert "risk_score" in res_url.json()

    # 4. Empty claim
    res_claim = client.post("/api/verify/claim", json={"claim": "", "language": "en"})
    assert res_claim.status_code == 200
    assert res_claim.json()["status"] == "INSUFFICIENT_EVIDENCE"

    print("[PASS] Edge Cases (Empty, Long, Malformed Input) Passed")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING COMPLETE NIVESHRAKSHAK AI BACKEND API TEST SUITE")
    print("=" * 60)
    test_health()
    test_edge_cases()
    test_analyze_text_scam()
    test_analyze_text_educational()
    test_analyze_text_regional_languages()
    test_analyze_image()
    test_analyze_url()
    test_classify_content()
    test_voice_assistant()
    test_verify_claim()
    test_education_topics()
    test_resilience_test()
    test_demo_cases()
    test_analytics()
    test_history_and_privacy()
    print("=" * 60)
    print("ALL BACKEND ENDPOINTS AND DATABASE OPERATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)
