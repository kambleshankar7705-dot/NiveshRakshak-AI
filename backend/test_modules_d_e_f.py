import urllib.request
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
_use_test_client = None
_test_client = None

def get_test_client():
    global _test_client
    if _test_client is None:
        from fastapi.testclient import TestClient
        from app.main import app
        _test_client = TestClient(app)
    return _test_client

def post(endpoint, data):
    global _use_test_client
    if _use_test_client is None:
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/api/health",
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                _use_test_client = False
        except Exception:
            _use_test_client = True

    if not _use_test_client:
        try:
            url = f"{BASE_URL}{endpoint}"
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            pass

    client = get_test_client()
    res = client.post(endpoint, json=data)
    return res.json()

def test_url_checker():
    print("--- 1. Testing URL Safety Checker ---")
    # Test high-risk phishing URL
    res = post("/api/analyze/url", {
        "url": "http://sebi-authorized-wealth-guaranteed.xyz/deposit?ref=telegram_vip",
        "language": "hi"
    })
    assert res["risk_level"] == "HIGH", f"Expected HIGH, got {res['risk_level']}"
    assert res["is_official_regulator"] is False
    assert len(res["checklist"]) == 5
    assert res["explanation_hi"], "Missing Hindi explanation"
    print("  ✓ Phishing URL test PASSED (Risk: HIGH, 5-point diagnostic checklist verified)")

    # Test official SEBI URL
    res_safe = post("/api/analyze/url", {
        "url": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes",
        "language": "mr"
    })
    assert res_safe["risk_level"] == "LOW", f"Expected LOW, got {res_safe['risk_level']}"
    assert res_safe["is_official_regulator"] is True
    assert res_safe["explanation_mr"], "Missing Marathi explanation"
    print("  ✓ Official SEBI URL test PASSED (Risk: LOW, Whitelisted as official regulator)")

def test_claim_verifier():
    print("\n--- 2. Testing Claim Evidence Verifier ---")
    # Test valid SEBI format
    res_valid_format = post("/api/verify/claim", {
        "claim": "ABC Capital is SEBI registered Research Analyst (INH000012345).",
        "language": "en"
    })
    assert res_valid_format["status"] == "PARTIALLY_VERIFIED"
    assert res_valid_format["category"] == "SEBI_REGISTRATION"
    assert "INH000012345" in res_valid_format["official_verification_status"]
    print("  ✓ Valid SEBI format test PASSED (PARTIALLY_VERIFIED, ID extracted)")

    # Test prohibited guaranteed return
    res_guaranteed = post("/api/verify/claim", {
        "claim": "100% Guaranteed profit on intraday options calls with zero risk.",
        "language": "hi"
    })
    assert res_guaranteed["status"] == "UNVERIFIED"
    assert res_guaranteed["category"] == "GUARANTEED_RETURN"
    assert res_guaranteed["reason_hi"], "Missing Hindi reason"
    print("  ✓ Guaranteed return claim test PASSED (UNVERIFIED, PROHIBITED claim detected)")

    # Test unverified regulatory impersonation
    res_unverified = post("/api/verify/claim", {
        "claim": "SEBI approved VIP intraday calls group.",
        "language": "mr"
    })
    assert res_unverified["status"] == "UNVERIFIED"
    assert res_unverified["category"] == "REGULATOR_IMPERSONATION"
    assert res_unverified["reason_mr"], "Missing Marathi reason"
    print("  ✓ Fake SEBI claim test PASSED (UNVERIFIED, Missing registration number identified)")

def test_content_classifier():
    print("\n--- 3. Testing Promotion vs Education Classifier ---")
    # High-Risk Promotional
    res_promo = post("/api/classify/content", {
        "content": "Tomorrow 9:15 AM! 100% SURE SHOT JACKPOT CALL! Penny stock will do 10X in 2 weeks! Join VIP Premium Group for ₹4,999.",
        "platform": "Telegram",
        "language": "en"
    })
    assert res_promo["classification"] == "HIGH_RISK_PROMOTIONAL"
    assert res_promo["promotional_score"] >= 80
    assert len(res_promo["risk_indicators"]) >= 2
    print(f"  ✓ High-Risk Promotional test PASSED (Promo Score: {res_promo['promotional_score']}%, Edu Score: {res_promo['educational_score']}%)")

    # Genuine Educational
    res_edu = post("/api/classify/content", {
        "content": "Understanding Diversification: Spreading your portfolio across equity, fixed income, and gold helps minimize concentration risk. All investments are subject to market volatility. Mutual fund NAV fluctuates daily.",
        "platform": "YouTube",
        "language": "hi"
    })
    assert res_edu["classification"] == "EDUCATIONAL"
    assert res_edu["educational_score"] >= 80
    assert len(res_edu["educational_signals"]) >= 2
    assert res_edu["explanation_hi"], "Missing Hindi explanation"
    print(f"  ✓ Educational content test PASSED (Promo Score: {res_edu['promotional_score']}%, Edu Score: {res_edu['educational_score']}%)")

    # Mixed Intent
    res_mixed = post("/api/classify/content", {
        "content": "What is compounding? Compounding is earning returns on your interest over time. If you want my daily stock picks to compound 20% every week, DM me for secret VIP group! Limited slots left!",
        "platform": "Instagram",
        "language": "mr"
    })
    assert res_mixed["classification"] == "MIXED"
    assert len(res_mixed["risk_indicators"]) >= 1
    assert len(res_mixed["educational_signals"]) >= 1
    assert res_mixed["explanation_mr"], "Missing Marathi explanation"
    print(f"  ✓ Mixed content test PASSED (Classification: {res_mixed['classification']})")

if __name__ == "__main__":
    try:
        test_url_checker()
        test_claim_verifier()
        test_content_classifier()
        print("\n========================================================")
        print("ALL URL CHECKER, CLAIM VERIFIER & CONTENT CLASSIFIER TESTS PASSED!")
        print("========================================================")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
