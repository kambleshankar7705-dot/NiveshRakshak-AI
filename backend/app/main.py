import os
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.models.schemas import (
    AnalysisRequest, AnalysisResult,
    UrlCheckRequest, UrlCheckResult,
    ClaimVerifyRequest, ClaimVerifyResult,
    ContentClassifyRequest, ContentClassifyResult,
    VoiceAnalyzeRequest, VoiceAnalyzeResult,
    ResilienceAnswerRequest, ResilienceQuestion
)
from app.services.rule_engine import analyze_text_rules
from app.services.ai_engine import analyze_with_ai_or_fallback
from app.services.url_engine import check_url_safety
from app.services.classifier_engine import classify_financial_content
from app.services.claim_verifier_engine import verify_financial_claim
from app.services.ocr_engine import extract_text_from_image_bytes
from app.services.database import (
    init_db, save_analysis, get_history, delete_analysis, clear_all_history, get_analytics_summary
)
from app.data.seeds import DEMO_CASES, LEARNING_TOPICS, RESILIENCE_QUESTIONS

# Initialize FastAPI application
app = FastAPI(
    title="NiveshRakshak AI API",
    description="Investor Protection and Financial Misinformation Detection Platform for Indian Retail Investors",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NiveshRakshak AI",
        "version": "1.0.0",
        "ai_configured": bool(os.getenv("AI_API_KEY", "").strip()),
        "mode": "PRODUCTION_READY"
    }

# ----------------- MODULE A: TEXT ANALYZER -----------------
@app.post("/api/analyze/text", response_model=Dict[str, Any])
async def analyze_text(request: AnalysisRequest):
    result = await analyze_with_ai_or_fallback(request.text, request.language)
    analysis_id = save_analysis(result, input_type=request.input_type, language=request.language)
    result["id"] = analysis_id
    return result

# ----------------- MODULE B: SCREENSHOT ANALYZER -----------------
@app.post("/api/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    language: str = Form("en"),
    auto_analyze: bool = Form(True)
):
    try:
        contents = await file.read()
        ocr_result = extract_text_from_image_bytes(contents, filename=file.filename or "")
        
        extracted_text = ocr_result.get("extracted_text", "")
        
        analysis = None
        if auto_analyze and extracted_text:
            analysis = await analyze_with_ai_or_fallback(extracted_text, language)
            analysis_id = save_analysis(analysis, input_type="SCREENSHOT", language=language)
            analysis["id"] = analysis_id

        return {
            "success": ocr_result.get("success", False),
            "ocr_method": ocr_result.get("method", "OCR"),
            "extracted_text": extracted_text,
            "filename": file.filename,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")

# ----------------- MODULE C: URL SAFETY CHECKER -----------------
@app.post("/api/analyze/url", response_model=Dict[str, Any])
def analyze_url(req: UrlCheckRequest):
    result = check_url_safety(req.url, req.language)
    # Save URL check to history for tracking
    dummy_analysis = {
        "risk_score": result["risk_score"],
        "risk_level": result["risk_level"],
        "content_type": "URL_INSPECTION",
        "red_flags": [{"name": ind, "severity": "HIGH", "evidence": result["domain"], "description": ind, "score_impact": 15} for ind in result["suspicious_indicators"]],
        "claim_analysis": [],
        "explanation": result["explanation"],
        "explanation_hi": result["explanation"],
        "explanation_mr": result["explanation"],
        "recommended_actions": result["recommended_actions"]
    }
    save_analysis(dummy_analysis, input_type="URL", language=req.language)
    return result

# ----------------- MODULE D & E: CONTENT & PROMOTION CLASSIFIER -----------------
@app.post("/api/classify/content", response_model=Dict[str, Any])
def classify_content(req: ContentClassifyRequest):
    result = classify_financial_content(req.content, req.platform or "Social Media", req.language)
    if req.content and req.content.strip():
        promo_score = result.get("promotional_score", 0)
        risk_lvl = "HIGH" if promo_score >= 70 else ("MEDIUM" if promo_score >= 35 else "LOW")
        dummy_analysis = {
            "risk_score": promo_score,
            "risk_level": risk_lvl,
            "content_type": "CONTENT_CLASSIFIER",
            "red_flags": [{"name": ind, "severity": "HIGH", "evidence": req.platform or "Social Media", "description": ind, "score_impact": 15} for ind in result.get("risk_indicators", [])],
            "claim_analysis": [],
            "explanation": result["explanation"],
            "explanation_hi": result.get("explanation_hi", result["explanation"]),
            "explanation_mr": result.get("explanation_mr", result["explanation"]),
            "recommended_actions": [f"Scrutinize investment promotions on {req.platform or 'social media'}. Verify all advice."]
        }
        save_analysis(dummy_analysis, input_type="CONTENT", language=req.language)
    return result

# ----------------- MODULE F: VOICE ASSISTANT -----------------
@app.post("/api/analyze/voice")
async def analyze_voice(req: VoiceAnalyzeRequest):
    # Analyze spoken transcript
    analysis = await analyze_with_ai_or_fallback(req.transcript, req.language)
    analysis_id = save_analysis(analysis, input_type="VOICE", language=req.language)
    analysis["id"] = analysis_id

    # Generate very short, voice-friendly summary tailored to regional language
    risk_level = analysis.get("risk_level", "LOW")
    score = analysis.get("risk_score", 0)

    if req.language == "mr":
        if risk_level in ["HIGH", "VERY_HIGH"]:
            voice_summary = (
                f"सावधान! या संदेशामध्ये खूप जास्त धोका आढळला आहे, जोखीम स्कोर {score} आहे. "
                "कोणालाही पैसे पाठवू नका किंवा ओटीपी शेअर करू नका."
            )
        else:
            voice_summary = f"या मजकुरामध्ये मोठा धोका आढळला नाही. तरीही काळजीपूर्वक निर्णय घ्या."
    elif req.language == "hi":
        if risk_level in ["HIGH", "VERY_HIGH"]:
            voice_summary = (
                f"चेतावनी! इस संदेश में अत्यधिक जोखिम पाया गया है, रिस्क स्कोर {score} है। "
                "कृपया किसी को पैसे न भेजें और ओटीपी साझा न करें।"
            )
        else:
            voice_summary = f"इस संदेश में कोई गंभीर जोखिम नहीं दिखा। फिर भी सतर्क रहें।"
    else:
        if risk_level in ["HIGH", "VERY_HIGH"]:
            voice_summary = (
                f"Caution. High risk detected with a safety risk score of {score} out of 100. "
                "Do not transfer any money or share credentials."
            )
        else:
            voice_summary = f"Low risk detected. Content appears informational, but remember market investments carry risk."

    return {
        "transcript": req.transcript,
        "detected_language": req.language,
        "voice_friendly_summary": voice_summary,
        "risk_level": risk_level,
        "risk_score": score,
        "analysis": analysis
    }

# ----------------- MODULE G: CLAIM EVIDENCE VERIFICATION -----------------
@app.post("/api/verify/claim")
def verify_claim(req: ClaimVerifyRequest):
    result = verify_financial_claim(req.claim, req.language)
    if req.claim and req.claim.strip():
        claim_risk = 85 if result["status"] == "UNVERIFIED" else (40 if result["status"] == "PARTIALLY_VERIFIED" else 10)
        risk_lvl = "HIGH" if claim_risk >= 70 else ("MEDIUM" if claim_risk >= 30 else "LOW")
        dummy_analysis = {
            "risk_score": claim_risk,
            "risk_level": risk_lvl,
            "content_type": "CLAIM_VERIFICATION",
            "red_flags": [{"name": result.get("category", "CLAIM"), "severity": "HIGH", "evidence": req.claim, "description": result.get("official_verification_status", ""), "score_impact": 20}],
            "claim_analysis": [{"claim": req.claim, "is_verified": result["status"] == "VERIFIED", "category": result.get("category", ""), "verification_source": "SEBI Regulatory Heuristic"}],
            "explanation": result["reason"],
            "explanation_hi": result.get("reason_hi", result["reason"]),
            "explanation_mr": result.get("reason_mr", result["reason"]),
            "recommended_actions": result.get("suggested_verification_steps", [])
        }
        save_analysis(dummy_analysis, input_type="CLAIM", language=req.language)
    return result

# ----------------- MODULE H: LEARNING TOPICS -----------------
@app.get("/api/education")
def get_education_topics(language: str = Query("en")):
    return {
        "topics": LEARNING_TOPICS,
        "total": len(LEARNING_TOPICS)
    }

# ----------------- MODULE I: RESILIENCE TEST -----------------
@app.get("/api/resilience-test/questions")
def get_resilience_questions():
    return {
        "questions": RESILIENCE_QUESTIONS,
        "total": len(RESILIENCE_QUESTIONS)
    }

@app.post("/api/resilience-test/evaluate")
def evaluate_resilience_answers(submission: Dict[str, str]):
    # submission is {question_id: selected_option}
    score = 0
    feedback = []

    for q in RESILIENCE_QUESTIONS:
        qid_str = str(q["id"])
        selected = submission.get(qid_str, "").upper()
        is_correct = (selected == q["correct_option"])
        if is_correct:
            score += 1
        feedback.append({
            "question_id": q["id"],
            "scenario": q["scenario"],
            "scenario_hi": q.get("scenario_hi", q["scenario"]),
            "scenario_mr": q.get("scenario_mr", q["scenario"]),
            "user_choice": selected,
            "correct_choice": q["correct_option"],
            "is_correct": is_correct,
            "concept_tested": q["concept_tested"],
            "explanation": q["explanation"],
            "explanation_hi": q.get("explanation_hi", q["explanation"]),
            "explanation_mr": q.get("explanation_mr", q["explanation"])
        })

    percentage = int((score / len(RESILIENCE_QUESTIONS)) * 100) if RESILIENCE_QUESTIONS else 0
    if percentage >= 80:
        resilience_tier = "HIGH RESILIENCE"
        summary = "Outstanding! You possess strong scam detection instincts and understand key regulatory protections."
        summary_hi = "शानदार! आपकी समझ बहुत मजबूत है और आप वित्तीय धोखाधड़ी के संकेतों को अच्छी तरह पहचानते हैं।"
        summary_mr = "उत्कृष्ट! तुमची फसवणूक ओळखण्याची क्षमता उत्तम आहे आणि तुम्ही सेबीच्या नियमांची चांगली जाण राखता."
    elif percentage >= 50:
        resilience_tier = "MODERATE RESILIENCE"
        summary = "Good awareness. Review the explanations to identify subtle emotional pressure and fake regulatory claims."
        summary_hi = "अच्छी जागरूकता। भावनात्मक दबाव और फर्जी दावों को पहचानने के लिए स्पष्टीकरण ध्यान से पढ़ें।"
        summary_mr = "चांगली जागरूकता. भावनिक दबाव आणि बनावट दावे ओळखण्यासाठी स्पष्टीकरण लक्षपूर्वक वाचा."
    else:
        resilience_tier = "VULNERABLE TO SCAMS"
        summary = "Caution advised. Scammers frequently exploit urgency and guaranteed returns. Explore the Learn section to build your defenses."
        summary_hi = "सावधानी जरूरी है। धोखेबाज जल्दबाजी और गारंटीड रिटर्न का झांसा देते हैं। अपनी सुरक्षा बढ़ाने के लिए 'सीखें' सेक्शन देखें।"
        summary_mr = "सावधगिरी बाळगणे आवश्यक आहे. फसवणूक करणारे घाई आणि नक्की परताव्याचे आमिष दाखवतात. माहिती वाढवण्यासाठी 'माहिती व शिक्षण' विभाग पहा."

    return {
        "score": score,
        "total_questions": len(RESILIENCE_QUESTIONS),
        "percentage": percentage,
        "resilience_tier": resilience_tier,
        "summary": summary,
        "summary_hi": summary_hi,
        "summary_mr": summary_mr,
        "feedback": feedback,
        "disclaimer": "This score reflects educational scam awareness and is not a financial credit score or investment recommendation."
    }

# ----------------- MODULE J: ANALYSIS HISTORY -----------------
@app.get("/api/history")
def get_history_route(limit: int = 50):
    return {
        "history": get_history(limit),
        "privacy_notice": "No OTPs, passwords, bank accounts, or personal financial records are ever stored."
    }

@app.delete("/api/history/{analysis_id}")
def delete_history_item(analysis_id: str):
    success = delete_analysis(analysis_id)
    return {"success": success, "deleted_id": analysis_id}

@app.delete("/api/history")
def delete_all_history():
    count = clear_all_history()
    return {"success": True, "records_deleted": count}

# ----------------- MODULE K: DEMO CASES -----------------
@app.get("/api/demo")
def get_demo_cases():
    return {
        "cases": DEMO_CASES
    }

# ----------------- MODULE L: ADMIN & DEMO ANALYTICS -----------------
@app.get("/api/analytics")
def get_analytics():
    return get_analytics_summary()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
