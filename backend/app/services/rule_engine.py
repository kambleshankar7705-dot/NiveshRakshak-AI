import re
from typing import Dict, Any, List, Tuple
from app.models.schemas import RedFlag, ClaimAnalysis, AnalysisResult

# Keyword dictionaries supporting English, transliterated Hindi/Marathi, and Devanagari script
PATTERNS = {
    "GUARANTEED_RETURN": {
        "weight": 20,
        "name": "Guaranteed Return Claim",
        "name_hi": "गारंटीड रिटर्न का दावा",
        "name_mr": "नक्की परताव्याचा दावा",
        "severity": "HIGH",
        "desc": "Legitimate market investments never guarantee high fixed returns. Every investment carries market risk.",
        "desc_hi": "शेयर बाजार में कोई भी वैध निवेश निश्चित या गारंटीड रिटर्न का वादा नहीं करता। सभी निवेशों में जोखिम होता है।",
        "desc_mr": "बाजारातील कोणतीही कायदेशीर गुंतवणूक कधीही हमी परतावा देत नाही. प्रत्येक गुंतवणुकीत जोखीम असते.",
        "regex": r"(guaranteed return|100%\s*(guarantee|return|safe|fixed)|no\s*loss|risk\s*free|zero\s*risk|fixed\s*profit|नक्की\s*परतावा|गॅरंटीड|गॅरंटी|हमीभाव|नक्की\s*नफा|गारंटीड|गारंटी|पक्का\s*मुनाफा|फिक्स\s*प्रॉफिट|नुकसान\s*नाही|बिना\s*जोखिम)"
    },
    "UNREALISTIC_PROFIT": {
        "weight": 15,
        "name": "Unrealistic Profit Promise",
        "name_hi": "अवास्तविक लाभ का वादा",
        "name_mr": "अवास्तव नफ्याचे आमिष",
        "severity": "HIGH",
        "desc": "Claims of doubling money or multiplying wealth in short periods are characteristic of fraudulent schemes.",
        "desc_hi": "कम समय में पैसे दोगुना करने या अत्यधिक मुनाफा देने का दावा पोंजी या धोखाधड़ी योजनाओं का मुख्य लक्षण है।",
        "desc_mr": "कमी दिवसांत पैसे दुप्पट करण्याचे किंवा मोठा नफा देण्याचे आमिष फसव्या योजनांचे लक्षण आहे.",
        "regex": r"(double\s*your\s*money|10x|5x|3x|2x\s*in\s*\d+|₹?\s*\d+[\d,]*\s*(to|into|बनाएं|करा|पाएं|मिळवा|कमवा)\s*₹?\s*\d+[\d,]*|dampat\s*return|लखपती|करोडपती|पैसे\s*दुप्पट|दोगुना|100%\s*profit|daily\s*profit|20%\s*daily|50%\s*weekly)"
    },
    "URGENCY_PRESSURE": {
        "weight": 10,
        "name": "Urgency & Time Pressure",
        "name_hi": "जल्दबाजी और समय का दबाव",
        "name_mr": "घाईगडबड आणि वेळेचा दबाव",
        "severity": "MEDIUM",
        "desc": "Scammers create artificial FOMO (Fear of Missing Out) and rush victims so they do not have time to verify facts.",
        "desc_hi": "धोखेबाज कृत्रिम जल्दबाजी पैदा करते हैं ताकि पीड़ित को सोचने या सत्यापन करने का समय न मिले।",
        "desc_mr": "फसवणूक करणारे वेळेची कृत्रिम घाई निर्माण करतात जेणेकरून विचार करायला वेळ मिळू नये.",
        "regex": r"(act\s*now|hurry\s*up|today\s*only|last\s*chance|limited\s*slots|limited\s*seats|offer\s*expires|invest\s*immediately|urgent|फास्ट\s*करा|लवकर\s*करा|शेवटची\s*संधी|आजच\s*करा|तुरंत\s*(करें|पेमेंट|भुगतान)|तुरंत|अंतिम\s*अवसर|आखिरी\s*मौका|जल्दी\s*करें)"
    },
    "FEAR_PRESSURE": {
        "weight": 10,
        "name": "Fear or Coercive Pressure",
        "name_hi": "डर या नुकसान का भय दिखाना",
        "name_mr": "भीती किंवा नुकसानीचा दबाव",
        "severity": "HIGH",
        "desc": "Language designed to induce panic, missed opportunity fear, or legal penalties.",
        "desc_hi": "मौका हाथ से निकल जाने या पछतावे का डर दिखाकर जल्दबाजी में निर्णय कराने का प्रयास।",
        "desc_mr": "संधी हुकल्यास मोठे नुकसान होईल अशी भीती दाखवून निर्णय घेण्यास भाग पाडणे.",
        "regex": r"(don\'t\s*miss\s*out|regret\s*later|loss\s*of\s*lifetime|account\s*blocked|penalty\s*if\s*not|legal\s*action|पछताओगे|हाथ\s*से\s*निकल\s*जाएगा|संधी\s*हुकवू\s*नका|नुकसान\s*होगा)"
    },
    "AUTHORITY_IMPERSONATION": {
        "weight": 15,
        "name": "Fake Authority / Regulatory Claim",
        "name_hi": "फर्जी सेबी/सरकारी योजना दावा",
        "name_mr": "बनावट सेबी/सरकारी मान्यता दावा",
        "severity": "HIGH",
        "desc": "Claiming affiliation with SEBI, RBI, or Government bodies to fabricate false legitimacy without registration proof.",
        "desc_hi": "बिना वैध रजिस्ट्रेशन नंबर के सेबी (SEBI) या आरबीआई (RBI) के नाम का दुरुपयोग कर विश्वास जीतना।",
        "desc_mr": "नोंदणी क्रमांकाशिवाय सेबी किंवा आरबीआयच्या नावाचा वापर करून खोटी खात्री देणे.",
        "regex": r"(sebi\s*(approved|registered|certified|authorized|मान्यता)|rbi\s*(approved|licensed|scheme)|government\s*(approved|scheme|backed)|official\s*scheme|सरकारी\s*(योजना|स्कीम)|सेबी\s*(मान्यता|अप्रूव्ड|रजिस्टर्ड)|आरबीआय|आरबीआई|भारत\s*सरकार)"
    },
    "PAYMENT_PRESSURE": {
        "weight": 10,
        "name": "Unusual Payment / Transfer Request",
        "name_hi": "व्यक्तिगत खाते में भुगतान की मांग",
        "name_mr": "खाजगी खात्यावर पैसे पाठवण्याची मागणी",
        "severity": "MEDIUM",
        "desc": "Requests to transfer funds directly via personal UPI or personal bank accounts rather than regulated broker clearing accounts.",
        "desc_hi": "आधिकारिक ब्रोकर खाते के बजाय किसी निजी व्यक्ति के यूपीआई या बैंक खाते में पैसे मांगने की कोशिश।",
        "desc_mr": "अधिकृत खात्याऐवजी वैयक्तिक यूपीआय किंवा बँक खात्यावर पैसे जमा करण्यास सांगणे.",
        "regex": r"(send\s*money|upi\s*now|pay\s*registration\s*fee|transfer\s*to\s*personal\s*account|gpay\s*to|phonepe\s*to|paytm\s*number|पैसे\s*(पाठवा|भेजें)|रजिस्ट्रेशन\s*फी|खात्यावर\s*पाठवा|पेमेंट\s*करें|भुगतान\s*करें|upi\s*पर)"
    },
    "CREDENTIAL_REQUEST": {
        "weight": 20,
        "name": "Credential / OTP Request",
        "name_hi": "ओटीपी या पासवर्ड मांगने का प्रयास",
        "name_mr": "ओटीपी किंवा पासवर्ड मागण्याचा प्रकार",
        "severity": "HIGH",
        "desc": "Asking for confidential security information such as OTP, banking PIN, or Demat credentials. Legitimate entities never ask for these.",
        "desc_hi": "ओटीपी, पिन या पासवर्ड जैसी गोपनीय जानकारी मांगना। कोई भी अधिकृत संस्था इसे कभी नहीं मांगती।",
        "desc_mr": "ओटीपी, पिन किंवा पासवर्ड यासारखी गुप्त माहिती विचारणे. कोणतीही खरी संस्था हे कधीही मागत नाही.",
        "regex": r"(otp|one\s*time\s*password|password|pin|mpin|login\s*details|share\s*code|ओटीपी|पासवर्ड|पिन)"
    },
    "SOCIAL_SOLICITATION": {
        "weight": 8,
        "name": "Social Media Solicitation (Telegram/VIP)",
        "name_hi": "सोशल मीडिया व वीआईपी ग्रुप आमंत्रण",
        "name_mr": "सोशल मीडिया व व्हीआयपी ग्रुप आमंत्रण",
        "severity": "LOW",
        "desc": "Directing individuals to private messaging groups (Telegram, WhatsApp) where unregulated tips and market manipulations circulate.",
        "desc_hi": "टेलीग्राम या व्हाट्सएप के गुप्त ग्रुप्स में जोड़ना जहां गैर-कानूनी टिप्स और जोड़-तोड़ चलती है।",
        "desc_mr": "टेलिग्राम किंवा व्हॉट्सअ‍ॅप ग्रुपमध्ये बोलावून बेकायदेशीर टिप्स देण्याचा प्रयत्न.",
        "regex": r"(join\s*telegram|vip\s*group|telegram\s*channel|whatsapp\s*group|premium\s*tips|dm\s*for\s*tips|inbox\s*me|link\s*in\s*bio|टेलिग्राम|टेलीग्राम|व्हॉट्सअ‍ॅप|व्हाट्सएप|व्हीआयपी\s*ग्रुप|वीआईपी\s*ग्रुप|ग्रुप\s*से\s*जुड़ें)"
    },
    "LIMITED_TIME": {
        "weight": 8,
        "name": "Limited Slot Exploitation",
        "name_hi": "सीमित सीटों का झांसा",
        "name_mr": "मर्यादित जागांचे आमिष",
        "severity": "LOW",
        "desc": "Claiming only 5 or 10 slots remain to force an unconsidered financial decision.",
        "desc_hi": "केवल कुछ सीटें बची हैं कहकर तुरंत पैसे ट्रांसफर कराने की चाल।",
        "desc_mr": "फक्त काहीच जागा शिल्लक आहेत असे सांगून घाईघाईत पैसे उकळण्याची क्लृप्ती.",
        "regex": r"(only\s*\d+\s*(slots|seats|spots)\s*left|first\s*\d+\s*members|कमी\s*जागा|फक्त\s*\d+\s*लोकांसाठी|सिर्फ\s*\d+\s*(सीटें|स्लॉट))"
    },
    "UNVERIFIED_CLAIM": {
        "weight": 10,
        "name": "Unsupported Financial Claim",
        "name_hi": "अपुष्ट व अविश्वसनीय वित्तीय दावा",
        "name_mr": "अपुरा व संशयास्पद आर्थिक दावा",
        "severity": "MEDIUM",
        "desc": "Bold claims of insider knowledge, secret algorithms, or guaranteed winning algorithms with no audited track record.",
        "desc_hi": "गुप्त सूत्रों, जादुई फॉर्मूला या 100% सही कॉल का खोखला दावा।",
        "desc_mr": "गुप्त माहिती किंवा १००% अचूक फॉर्म्युला असल्याचा खोटा दावा.",
        "regex": r"(100%\s*accuracy|insider\s*tip|secret\s*formula|sure\s*shot|jackpot\s*call|100%\s*कॉल|नक्की\s*नफा|खात्रीशीर\s*टिप|जैकपॉट\s*कॉल)"
    }
}


EDUCATIONAL_PATTERNS = [
    r"(diversification|asset\s*allocation|nav|mutual\s*fund|portfolio|risk\s*management|volatility|compounding|sebi\s*guidelines|investor\s*education|समतोल|विविधता|जोखिम|म्युच्युअल\s*फंड|दीर्घकालीन|एसआयपी|sip\s*calculator)"
]

def analyze_text_rules(text: str, language: str = "en") -> Dict[str, Any]:
    if not text or not text.strip():
        return {
            "risk_score": 0,
            "risk_level": "LOW",
            "content_type": "INFORMATIONAL",
            "red_flags": [],
            "claim_analysis": [],
            "explanation": "No text content provided for risk inspection.",
            "explanation_hi": "जोखिम निरीक्षण के लिए कोई पाठ्य सामग्री प्रदान नहीं की गई।",
            "explanation_mr": "तपासणीसाठी कोणताही मजकूर उपलब्ध नाही.",
            "recommended_actions": ["Please provide a message or upload an image to analyze."],
            "recommended_actions_hi": ["कृपया विश्लेषण के लिए कोई संदेश दर्ज करें या फोटो अपलोड करें।"],
            "recommended_actions_mr": ["कृपया विश्लेषणासाठी मजकूर टाका किंवा फोटो अपलोड करा."],
            "pause_advised": False,
            "pause_reasons": [],
            "pause_reasons_hi": [],
            "pause_reasons_mr": [],
            "confidence": 0.5,
            "analysis_engine": "RULE_ENGINE_FALLBACK"
        }

    detected_flags: List[RedFlag] = []
    total_score = 0
    pause_reasons = []
    pause_reasons_hi = []
    pause_reasons_mr = []

    text_lower = text.lower()

    for key, rule in PATTERNS.items():
        matches = re.findall(rule["regex"], text, re.IGNORECASE)
        if matches:
            # Extract distinct matched text snippet
            sample_match = matches[0]
            if isinstance(sample_match, tuple):
                sample_match = next((m for m in sample_match if m), sample_match[0])
            
            flag = RedFlag(
                name=rule["name"],
                name_hi=rule.get("name_hi"),
                name_mr=rule.get("name_mr"),
                severity=rule["severity"],
                evidence=f"Matched phrasing: '{sample_match}'",
                description=rule["desc"],
                desc_hi=rule.get("desc_hi"),
                desc_mr=rule.get("desc_mr"),
                score_impact=rule["weight"]
            )
            detected_flags.append(flag)
            total_score += rule["weight"]

            if key in ["URGENCY_PRESSURE", "FEAR_PRESSURE", "LIMITED_TIME"]:
                pause_reasons.append("High urgency detected: Scammers use time pressure to prevent independent verification.")
                pause_reasons_hi.append("अत्यधिक जल्दबाजी: धोखेबाज तथ्यों की जांच रोकने के लिए तुरंत निर्णय का दबाव बनाते हैं।")
                pause_reasons_mr.append("वेळेचा दबाव: सत्यता पडताळणी टाळण्यासाठी फसवणूक करणारे त्वरित पैसे पाठवण्याची घाई करतात.")
            if key == "CREDENTIAL_REQUEST":
                pause_reasons.append("Security Alert: Credential/OTP request identified. Never share security codes.")
                pause_reasons_hi.append("सुरक्षा चेतावनी: ओटीपी या पासवर्ड मांगने का प्रयास। गोपनीय कोड कभी साझा न करें।")
                pause_reasons_mr.append("सुरक्षा इशारा: ओटीपी किंवा पासवर्ड मागण्याचा प्रकार. कोणालाही कोड शेअर करू नका.")
            if key == "PAYMENT_PRESSURE":
                pause_reasons.append("Financial Alert: Direct payment or deposit request found. Do not transfer funds.")
                pause_reasons_hi.append("वित्तीय चेतावनी: सीधे पैसे भेजने का अनुरोध। सत्यापन के बिना पैसे न भेजें।")
                pause_reasons_mr.append("आर्थिक इशारा: थेट खात्यावर पैसे पाठवण्याची मागणी. खात्री केल्याशिवाय व्यवहार करू नका.")

    # Educational check
    is_educational = False
    for pat in EDUCATIONAL_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            is_educational = True
            break

    # If it's strongly educational and has zero high-severity red flags, reduce score
    if is_educational and len(detected_flags) == 0:
        total_score = max(0, total_score - 15)

    # Score cap
    final_score = min(100, max(0, total_score))

    # Risk level classification
    if final_score >= 80:
        risk_level = "VERY_HIGH"
    elif final_score >= 60:
        risk_level = "HIGH"
    elif final_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Content type determination
    if final_score >= 60:
        content_type = "FRAUD_SUSPECT"
    elif detected_flags:
        content_type = "INVESTMENT_PROMOTION"
    elif is_educational:
        content_type = "EDUCATIONAL"
    else:
        content_type = "INFORMATIONAL"

    # Analyze specific claims
    claims: List[ClaimAnalysis] = []
    if re.search(r"sebi\s*(approved|registered|authorized)", text, re.IGNORECASE):
        claims.append(ClaimAnalysis(
            claim="Claim of SEBI Registration or Approval",
            status="UNVERIFIED",
            reason="Message claims SEBI approval, but no valid SEBI Registration Number (e.g., INH... or INZ...) was found or verified against the official SEBI intermediary database.",
            suggested_steps=[
                "Ask for the 12-digit SEBI Registration Number.",
                "Visit sebi.gov.in -> Recognized Intermediaries and verify registration status.",
                "Ensure the bank account belongs to the registered entity, not an individual."
            ],
            is_demo_data=True
        ))

    if re.search(r"guaranteed|100%\s*return|double", text, re.IGNORECASE):
        claims.append(ClaimAnalysis(
            claim="Guaranteed or Risk-Free High Returns",
            status="UNVERIFIED",
            reason="Under SEBI regulations, registered entities and legitimate advisors are strictly prohibited from promising fixed or guaranteed returns on market securities.",
            suggested_steps=[
                "Remember that equity markets fluctuate and cannot guarantee returns.",
                "Recognize guaranteed return promises as a standard indicator of high-risk schemes."
            ],
            is_demo_data=True
        ))

    if not claims and detected_flags:
        claims.append(ClaimAnalysis(
            claim="Investment return or solicitation claims",
            status="INSUFFICIENT_EVIDENCE",
            reason="The message lacks verifiable documentation, audit reports, or regulatory disclosures.",
            suggested_steps=[
                "Do not rely solely on unsolicited messages or group posts.",
                "Verify information through registered financial advisors and official exchange portals (NSE/BSE)."
            ],
            is_demo_data=True
        ))

    # Formulate safe actions
    actions = []
    actions_hi = []
    actions_mr = []
    if risk_level in ["HIGH", "VERY_HIGH"]:
        actions.extend([
            "Do not transfer money or make UPI payments to unknown or personal accounts.",
            "Do not share OTP, passwords, UPI PINs, or financial credentials with anyone.",
            "Do not click on links provided in unverified WhatsApp or Telegram groups.",
            "Independently verify whether the entity is registered on the official SEBI website (sebi.gov.in).",
            "Report fraudulent messages on the National Cyber Crime Reporting Portal (cybercrime.gov.in) or call 1930."
        ])
        actions_hi.extend([
            "तुरंत किसी अनजान या निजी खाते में पैसे या यूपीआई पेमेंट न करें।",
            "कभी भी किसी के साथ ओटीपी, पासवर्ड, यूपीआई पिन या गोपनीय जानकारी साझा न करें।",
            "व्हाट्सएप या टेलीग्राम ग्रुप्स में दिए गए संदेहास्पद लिंक्स पर क्लिक न करें।",
            "सेबी की आधिकारिक वेबसाइट (sebi.gov.in) पर संस्था की 12-अंकों के रजिस्ट्रेशन की पुष्टि करें।",
            "साइबर धोखाधड़ी की शिकायत राष्ट्रीय हेल्पलाइन 1930 या cybercrime.gov.in पर दर्ज करें।"
        ])
        actions_mr.extend([
            "त्वरित कोणाच्याही अनोळखी किंवा खाजगी खात्यावर पैसे किंवा यूपीआय ट्रान्सफर करू नका.",
            "कधीही कोणालाही ओटीपी, पासवर्ड, यूपीआय पिन किंवा डिमॅटची माहिती देऊ नका.",
            "व्हॉट्सअ‍ॅप किंवा टेलिग्राम ग्रुप्समधील संशयास्पद लिंक्सवर क्लिक करू नका.",
            "सेबीच्या अधिकृत वेबसाईटवर (sebi.gov.in) संस्थेच्या १२-अंकी नोंदणीची खात्री करा.",
            "सायबर फसवणुकीची तक्रार राष्ट्रीय हेल्पलाइन १९३० किंवा cybercrime.gov.in वर नोंदवा."
        ])
    elif risk_level == "MEDIUM":
        actions.extend([
            "Ask for official registration details and verifiable credentials before taking action.",
            "Check for official disclosures and independent financial statements.",
            "Discuss with a SEBI-registered Investment Advisor before committing funds."
        ])
        actions_hi.extend([
            "कोई भी कदम उठाने से पहले आधिकारिक रजिस्ट्रेशन विवरण और कानूनी दस्तावेज मांगें।",
            "आधिकारिक डिस्क्लोजर और स्वतंत्र ऑडिट रिपोर्ट की जांच करें।",
            "पैसे लगाने से पहले किसी सेबी-रजिस्टर्ड निवेश सलाहकार से परामर्श लें।"
        ])
        actions_mr.extend([
            "कोणताही निर्णय घेण्यापूर्वी अधिकृत नोंदणी तपशील आणि कायदेशीर कागदपत्रे मागा.",
            "अधिकृत माहिती आणि ऑडिट अहवालांची स्वतंत्र पडताळणी करा.",
            "गुंतवणुकीपूर्वी सेबी-नोंदणीकृत गुंतवणूक सल्लागाराशी चर्चा करा."
        ])
    else:
        actions.extend([
            "Continue practicing healthy financial caution.",
            "Ensure you understand market risks, fees, and asset allocation before investing.",
            "Verify all sources through regulated exchange portals (NSE, BSE, SEBI)."
        ])
        actions_hi.extend([
            "निवेश करते समय हमेशा बुनियादी वित्तीय सावधानी बरतें।",
            "निवेश से पहले बाजार जोखिम, फीस और एसेट एलोकेशन को समझें।",
            "सभी स्रोतों की पुष्टि आधिकारिक एक्सचेंज पोर्टलों (NSE, BSE, SEBI) से करें।"
        ])
        actions_mr.extend([
            "गुंतवणूक करताना नेहमी मूलभूत आर्थिक दक्षता बाळगा.",
            "गुंतवणुकीपूर्वी बाजारातील जोखीम, आकारले जाणारे शुल्क समजून घ्या.",
            "सर्व स्रोतांची अधिकृत एक्सचेंज पोर्टल्सवरून (NSE, BSE, SEBI) खात्री करा."
        ])

    # Formulate multilingual explanations
    explanation_en = generate_explanation(risk_level, detected_flags, "en")
    explanation_hi = generate_explanation(risk_level, detected_flags, "hi")
    explanation_mr = generate_explanation(risk_level, detected_flags, "mr")

    pause_advised = len(pause_reasons) > 0 or risk_level in ["HIGH", "VERY_HIGH"]

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "content_type": content_type,
        "red_flags": [f.dict() for f in detected_flags],
        "claim_analysis": [c.dict() for c in claims],
        "explanation": explanation_en,
        "explanation_hi": explanation_hi,
        "explanation_mr": explanation_mr,
        "recommended_actions": actions,
        "recommended_actions_hi": actions_hi,
        "recommended_actions_mr": actions_mr,
        "pause_advised": pause_advised,
        "pause_reasons": pause_reasons,
        "pause_reasons_hi": pause_reasons_hi,
        "pause_reasons_mr": pause_reasons_mr,
        "confidence": 0.92,
        "analysis_engine": "RULE_ENGINE_FALLBACK",
        "disclaimer": (
            "NiveshRakshak AI provides educational and investor-protection information. "
            "It does not provide investment advice, stock recommendations, trading signals, or guaranteed outcomes."
        )
    }

def generate_explanation(risk_level: str, flags: List[RedFlag], lang: str) -> str:
    flag_names = [f.name for f in flags]

    if lang == "hi":
        if risk_level in ["HIGH", "VERY_HIGH"]:
            msg = (
                f"इस संदेश में उच्च जोखिम वाले संकेत पाए गए हैं (पहचाने गए संकेत: {', '.join(flag_names) if flag_names else 'संदेहास्पद दावे'})। "
                "सेबी (SEBI) के नियमों के अनुसार किसी भी शेयर बाजार निवेश में निश्चित या गारंटीड रिटर्न का वादा नहीं किया जा सकता। "
                "जल्दबाजी करने का दबाव और निजी खातों में पैसे भेजने की मांग धोखाधड़ी की ओर इशारा करती है। कृपया बिना आधिकारिक सत्यापन के कोई भुगतान न करें।"
            )
        elif risk_level == "MEDIUM":
            msg = "इस संदेश में कुछ संदिग्ध वित्तीय दावे या प्रचारक भाषा शामिल है। निवेश करने से पहले आधिकारिक स्रोतों से पुष्टि करें।"
        else:
            msg = "इस संदेश में कोई स्पष्ट धोखाधड़ी या अत्यधिक जोखिम के संकेत नहीं मिले हैं। फिर भी, हमेशा समझदारी और सावधानी से निर्णय लें।"
        return msg

    elif lang == "mr":
        if risk_level in ["HIGH", "VERY_HIGH"]:
            msg = (
                f"या संदेशामध्ये अत्यंत धोक्याचे संकेत आढळले आहेत (आढळलेले धोके: {', '.join(flag_names) if flag_names else 'संशयास्पद दावे'})। "
                "सेबीच्या (SEBI) नियमांनुसार बाजारातील कोणत्याही गुंतवणुकीवर निश्चित किंवा गॅरंटीड परतावा देण्याचे आश्वासन देणे बेकायदेशीर आहे. "
                "घाईगडबड करणे आणि टेलिग्राम किंवा खाजगी खात्यावर पैसे पाठवण्यास सांगणे हे आर्थिक फसवणुकीचे मुख्य लक्षण आहे. कोणालाही पैसे पाठवू नका."
            )
        elif risk_level == "MEDIUM":
            msg = "या संदेशामध्ये काही संशयास्पद दावे आढळले आहेत. कोणत्याही निर्णयापूर्वी अधिकृत नोंदणीची खात्री करा."
        else:
            msg = "या मजकुरामध्ये फसवणुकीचे कोणतेही उघड संकेत आढळले नाहीत. तरीही गुंतवणुकीपूर्वी बाजारातील जोखीम समजून घ्या."
        return msg

    else: # English
        if risk_level in ["HIGH", "VERY_HIGH"]:
            msg = (
                f"High-risk indicators were detected in this content (Identified factors: {', '.join(flag_names) if flag_names else 'Suspicious claims'}). "
                "Regulated financial markets carry inherent volatility, and promising guaranteed profits is prohibited under SEBI regulations. "
                "The presence of artificial urgency and solicitations via unofficial channels are classic hallmarks of investment scams. Do not transfer funds or share credentials."
            )
        elif risk_level == "MEDIUM":
            msg = (
                "Moderate risk indicators detected. The content uses promotional framing or unverified claims. "
                "Exercise caution and independently verify any claims before committing funds."
            )
        else:
            msg = (
                "No direct high-risk scam indicators were identified. The content appears educational or informational. "
                "Remember that all genuine market investments still carry market risks."
            )
        return msg
