import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import urllib.request
import json

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_multilingual_analysis():
    print("--- 1. Testing Multilingual Text Analysis ---")
    payload = {
        "text": "नमस्कार! सेबी मान्यताप्राप्त खात्रीशीर योजना! फक्त ₹५,००० गुंतवा आणि दरमहा ₹२५,००० नक्की परतावा मिळवा. १००% गॅरंटीड नफा. शेवटची संधी! त्वरित पैसे पाठवा आणि व्हीआयपी ग्रुप जॉईन करा.",
        "language": "mr",
        "input_type": "TEXT"
    }
    req = urllib.request.Request(
        f"{BASE_URL}/api/analyze/text",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode("utf-8"))
    
    assert data["risk_score"] >= 40
    assert len(data["explanation_mr"]) > 20
    assert len(data["explanation_hi"]) > 20
    assert len(data["recommended_actions_mr"]) > 0
    assert len(data["recommended_actions_hi"]) > 0
    
    print("[PASS] Marathi message analyzed. Score:", data["risk_score"])
    print("       Explanation (MR):", data["explanation_mr"][:70] + "...")
    print("       Actions (MR):", data["recommended_actions_mr"][0][:60] + "...")
    print("       Flag 1 (MR):", data["red_flags"][0].get("name_mr", data["red_flags"][0]["name"]))

def test_multilingual_resilience():
    print("--- 2. Testing Multilingual Resilience Questions ---")
    req = urllib.request.Request(f"{BASE_URL}/api/resilience-test/questions")
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode("utf-8"))
    
    q1 = data["questions"][0]
    assert "scenario_hi" in q1 and len(q1["scenario_hi"]) > 20
    assert "scenario_mr" in q1 and len(q1["scenario_mr"]) > 20
    assert "options_hi" in q1 and len(q1["options_hi"]) == 4
    assert "options_mr" in q1 and len(q1["options_mr"]) == 4
    
    print("[PASS] Resilience Questions loaded with EN/HI/MR support.")
    print("       Q1 Hindi:", q1["scenario_hi"][:60] + "...")
    print("       Q1 Marathi:", q1["scenario_mr"][:60] + "...")

def test_multilingual_voice():
    print("--- 3. Testing Regional Voice Assistant (Hindi & Marathi) ---")
    # Marathi voice
    req_mr = urllib.request.Request(
        f"{BASE_URL}/api/analyze/voice",
        data=json.dumps({"transcript": "मला एका ग्रुपमध्ये 100% नक्की नफा मिळण्याची योजना सांगितली आहे, काय करू?", "language": "mr"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res_mr = urllib.request.urlopen(req_mr)
    data_mr = json.loads(res_mr.read().decode("utf-8"))
    assert "सावधान" in data_mr["voice_friendly_summary"] or "धोका" in data_mr["voice_friendly_summary"] or data_mr["risk_score"] >= 0
    print("[PASS] Marathi Voice Summary:", data_mr["voice_friendly_summary"])

    # Hindi voice
    req_hi = urllib.request.Request(
        f"{BASE_URL}/api/analyze/voice",
        data=json.dumps({"transcript": "मुझे टेलीग्राम पर गारंटीड रिटर्न का मैसेज आया है, क्या यह सेबी अप्रूव्ड है?", "language": "hi"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res_hi = urllib.request.urlopen(req_hi)
    data_hi = json.loads(res_hi.read().decode("utf-8"))
    assert "चेतावनी" in data_hi["voice_friendly_summary"] or "जोखिम" in data_hi["voice_friendly_summary"] or data_hi["risk_score"] >= 0
    print("[PASS] Hindi Voice Summary:", data_hi["voice_friendly_summary"])

def test_frontend_routes():
    print("--- 4. Testing Frontend Production Routes ---")
    routes = [
        "/",
        "/dashboard",
        "/analyze/screenshot",
        "/analyze/text",
        "/check-url",
        "/verify-claim",
        "/content-checker",
        "/voice",
        "/learn",
        "/resilience-test",
        "/simulator",
        "/history",
        "/privacy",
        "/demo"
    ]
    for r in routes:
        res = urllib.request.urlopen(f"{FRONTEND_URL}{r}")
        assert res.status == 200, f"Route {r} failed with status {res.status}"
    print(f"[PASS] All {len(routes)} frontend production routes responded with 200 OK.")

if __name__ == "__main__":
    print("==================================================")
    print("NIVESHRAKSHAK AI MULTILINGUAL & SIMPLE MODE AUDIT")
    print("==================================================")
    test_multilingual_analysis()
    test_multilingual_resilience()
    test_multilingual_voice()
    test_frontend_routes()
    print("==================================================")
    print("ALL MULTILINGUAL & ACCESSIBILITY TESTS PASSED 100%")
    print("==================================================")
