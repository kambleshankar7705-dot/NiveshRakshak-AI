import os
import json
import httpx
from typing import Dict, Any
from app.services.rule_engine import analyze_text_rules

AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower().strip()

SYSTEM_PROMPT = """
You are NiveshRakshak AI, an investor protection and financial misinformation detection platform for Indian retail investors.
Your task is to analyze financial messages, claims, and social media posts to detect scams, deceptive claims, and manipulative language.

STRICT INSTRUCTIONS:
- You are NOT a trading advisor or stock picker.
- DO NOT recommend any stock, security, or investment.
- DO NOT provide buy/sell/hold advice.
- Return ONLY valid JSON matching this schema:
{
  "risk_score": 87,
  "risk_level": "VERY_HIGH",
  "content_type": "INVESTMENT_PROMOTION",
  "red_flags": [
    {
      "name": "Guaranteed Return",
      "severity": "HIGH",
      "evidence": "exact quote from text",
      "description": "explanation of risk",
      "score_impact": 20
    }
  ],
  "claim_analysis": [
    {
      "claim": "Claim text",
      "status": "UNVERIFIED",
      "reason": "Why unverified",
      "suggested_steps": ["step 1", "step 2"],
      "is_demo_data": true
    }
  ],
  "explanation": "Clear explanation in English",
  "explanation_hi": "Clear explanation in Hindi",
  "explanation_mr": "Clear explanation in Marathi",
  "recommended_actions": ["Action 1", "Action 2"],
  "pause_advised": true,
  "pause_reasons": ["Urgency detected"],
  "confidence": 0.95,
  "disclaimer": "NiveshRakshak AI provides educational and investor-protection information. It does not provide investment advice."
}
"""

async def analyze_with_ai_or_fallback(text: str, language: str = "en") -> Dict[str, Any]:
    # Check if AI key is provided
    api_key = os.getenv("AI_API_KEY", "").strip()

    if not api_key:
        result = analyze_text_rules(text, language)
        result["analysis_engine"] = "RULE_ENGINE_FALLBACK"
        result["engine_note"] = "Basic safety analysis used because advanced AI API key is not configured."
        return result

    try:
        if AI_PROVIDER == "openai":
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Analyze this financial message in {language}:\n\n{text}"}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.2
                    }
                )
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    parsed["analysis_engine"] = "AI_PRIMARY_OPENAI"
                    return parsed
        else: # Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{SYSTEM_PROMPT}\n\nAnalyze this financial message in {language}:\n\n{text}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.2
                }
            }
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_text)
                    parsed["analysis_engine"] = "AI_PRIMARY_GEMINI"
                    return parsed
    except Exception as e:
        # Graceful fallback on any API error or timeout
        pass

    result = analyze_text_rules(text, language)
    result["analysis_engine"] = "RULE_ENGINE_FALLBACK"
    result["engine_note"] = "Basic safety analysis used because advanced AI analysis is currently unavailable."
    return result
