from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RedFlag(BaseModel):
    name: str
    name_hi: Optional[str] = None
    name_mr: Optional[str] = None
    severity: str  # HIGH, MEDIUM, LOW
    evidence: str
    description: str
    desc_hi: Optional[str] = None
    desc_mr: Optional[str] = None
    score_impact: int

class ClaimAnalysis(BaseModel):
    claim: str
    status: str  # VERIFIED, PARTIALLY_VERIFIED, UNVERIFIED, INSUFFICIENT_EVIDENCE
    reason: str
    suggested_steps: List[str]
    is_demo_data: bool = True

class AnalysisRequest(BaseModel):
    text: str
    language: str = "en"  # "en", "hi", "mr"
    input_type: str = "TEXT"  # "TEXT", "SCREENSHOT", "URL", "VOICE"

class AnalysisResult(BaseModel):
    id: Optional[str] = None
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str  # LOW, MEDIUM, HIGH, VERY_HIGH
    content_type: str  # INVESTMENT_PROMOTION, EDUCATIONAL, FRAUD_SUSPECT, INFORMATIONAL, UNCERTAIN
    red_flags: List[RedFlag] = []
    claim_analysis: List[ClaimAnalysis] = []
    explanation: str
    explanation_hi: Optional[str] = None
    explanation_mr: Optional[str] = None
    recommended_actions: List[str] = []
    recommended_actions_hi: Optional[List[str]] = None
    recommended_actions_mr: Optional[List[str]] = None
    pause_advised: bool = False
    pause_reasons: List[str] = []
    pause_reasons_hi: Optional[List[str]] = None
    pause_reasons_mr: Optional[List[str]] = None
    confidence: float = 0.90
    analysis_engine: str = "RULE_ENGINE_FALLBACK"  # "AI_PRIMARY" or "RULE_ENGINE_FALLBACK"
    disclaimer: str = (
        "NiveshRakshak AI provides educational and investor-protection information. "
        "It does not provide investment advice, stock recommendations, trading signals, or guaranteed outcomes."
    )
    created_at: Optional[str] = None

class UrlCheckRequest(BaseModel):
    url: str
    language: str = "en"

class UrlCheckResult(BaseModel):
    url: str
    risk_level: str  # LOW, MEDIUM, HIGH
    risk_score: int
    is_https: bool
    domain: str
    suspicious_indicators: List[str] = []
    explanation: str
    recommended_actions: List[str] = []
    disclaimer: str

class ClaimVerifyRequest(BaseModel):
    claim: str
    language: str = "en"

class ClaimVerifyResult(BaseModel):
    claim: str
    status: str  # VERIFIED, PARTIALLY_VERIFIED, UNVERIFIED, INSUFFICIENT_EVIDENCE
    official_verification_status: str
    reason: str
    needed_evidence: str
    suggested_verification_steps: List[str]
    demo_badge: str = "Demo Verification Data - Live Official Registry Integration in Future Scope"
    disclaimer: str

class ContentClassifyRequest(BaseModel):
    content: str
    platform: Optional[str] = "Social Media"  # YouTube, Telegram, WhatsApp, Instagram
    language: str = "en"

class ContentClassifyResult(BaseModel):
    classification: str  # EDUCATIONAL, PROMOTIONAL, MIXED, HIGH_RISK_PROMOTIONAL, UNCERTAIN
    confidence: float
    reasons: List[str]
    risk_indicators: List[str]
    evidence_quality: str  # HIGH, MODERATE, LOW, NONE
    explanation: str

class VoiceAnalyzeRequest(BaseModel):
    transcript: str
    language: str = "en"  # "en", "hi", "mr"

class VoiceAnalyzeResult(BaseModel):
    transcript: str
    detected_language: str
    voice_friendly_summary: str
    risk_level: str
    risk_score: int
    analysis: AnalysisResult

class ResilienceAnswerRequest(BaseModel):
    question_id: int
    selected_option: str

class ResilienceQuestion(BaseModel):
    id: int
    scenario: str
    question: str
    options: Dict[str, str]
    correct_option: str
    explanation: str
    concept_tested: str

class LearningTopicItem(BaseModel):
    id: str
    title: str
    title_hi: str
    title_mr: str
    category: str
    simple_explanation: str
    simple_explanation_hi: str
    simple_explanation_mr: str
    everyday_analogy: str
    everyday_analogy_hi: str
    everyday_analogy_mr: str
    example: str
    remember_this: str
    common_misconception: str
    quiz: Dict[str, Any]

class AnalyticsData(BaseModel):
    total_analyses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    common_red_flags: List[Dict[str, Any]]
    content_types: List[Dict[str, Any]]
    language_usage: Dict[str, int]
    input_channel_usage: Dict[str, int]
