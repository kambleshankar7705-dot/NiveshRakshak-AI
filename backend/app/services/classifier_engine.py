import re
from typing import Dict, Any, List

PROMOTIONAL_PATTERNS = [
    (
        r"(guarantee|100%\s*(safe|profit|sure|win|success)|double\s*(your)?\s*money|fixed\s*(return|profit)|zero\s*risk|10x|100x|multibagger|पैसे\s*दुप्पट|नक्की\s*नफा|गारंटीड|गॅरंटीड|खात्रीशीर)",
        "Promises guaranteed, high-multiple or fixed market returns, which is prohibited under SEBI regulations.",
        "बाजार में निश्चित, मल्टीबैगर या गारंटीड रिटर्न का वादा, जो सेबी नियमों के तहत अवैध है।",
        "बाजारात हमी किंवा अनेक पट परताव्याचे आश्वासन, जे सेबीच्या नियमांनुसार बेकायदेशीर आहे."
    ),
    (
        r"((join|entry|link|dm)\s*(in|to|for|me)?\s*(our|my|the|secret|exclusive|vip)?\s*(vip|telegram|whatsapp|premium|private)\s*(group|channel|community)?|vip\s*(group|channel|community|premium)|dm\s*(me|us)?\s*(for|to)?\s*(calls|stock|group|tips|profit|secret)|jackpot\s*call|sure\s*shot|stock\s*picks?|व्हॉट्सअ‍ॅप|टेलिग्राम)",
        "Directs audience to private unregulated messaging channels (Telegram/WhatsApp/VIP) for trading calls or secret tips.",
        "ट्रेडिंग कॉल्स या सीक्रेट टिप्स के लिए दर्शकों को निजी टेलीग्राम या व्हाट्सएप ग्रुप में भेजने का प्रयास।",
        "ट्रेडिंग टिप्स किंवा खाजगी ग्रुपसाठी प्रेक्षकांना टेलिग्राम किंवा व्हॉट्सअ‍ॅपवर नेण्याचा प्रयत्न."
    ),
    (
        r"(hurry|limited\s*(seats|slots|offer|time|spaces?|left)|last\s*chance|act\s*now|urgent|only\s*\d+\s*(slots|seats|left)|closing\s*soon|expires\s*(soon|today|midnight)|शेवटची\s*संधी|जल्दी\s*करें|त्वरा\s*करा)",
        "Manufactures artificial urgency, scarcity, or countdown pressure to force an impulsive decision.",
        "जल्दबाजी, सीमित समय और सीटों का दबाव ताकि सोचने व स्वतंत्र जांच का समय न मिले।",
        "घाईगडबड आणि वेळेचा दबाव निर्माण करून अविचाराने निर्णय घेण्यास भाग पाडणे."
    ),
    (
        r"(buy\s*(my|our)?\s*course|paid\s*(group|channel|calls|service)|subscription\s*fees?|[₹$]\s*[0-9,]+|rs\.?\s*[0-9,]+|coupon\s*code|discount\s*code|use\s*code|fees\s*only|admission\s*open|कोर्स\s*जॉईन\s*करा)",
        "Commercial upselling: Sells expensive unaccredited trading courses, membership packages, or fee-based tips.",
        "व्यावसायिक प्रचार: महंगे ट्रेडिंग कोर्स या सब्सक्रिप्शन पैकेज बेचने का प्रयास।",
        "व्यावसायिक विक्री: महागडे कोर्सेस किंवा पॅकेजेस विकण्याचा प्रयत्न."
    ),
    (
        r"(multibagger\s*call|sure\s*shot\s*(call|target)?|penny\s*stock|insider\s*(info|buying|operator)|target\s*[₹$]?\s*\d+|stop\s*loss\s*hit|rocket\s*stock|जैकपॉट\s*शेअर|१०\s*पट)",
        "Specific speculative price targets, penny stock pump, or hype designed to create retail buy pressure.",
        "विशिष्ट शेयरों में भारी मुनाफे का दावा कर खुदरा निवेशकों को आकर्षित करने की कोशिश।",
        "विशिष्ट शेअर्सचे अवास्तव टार्गेट देऊन सामान्य गुंतवणूकदारांना भुलवण्याचा प्रयत्न."
    )
]

EDUCATIONAL_PATTERNS = [
    (
        r"(diversification|asset\s*allocation|nav|mutual\s*fund|portfolio|risk\s*tolerance|compounding|rupee\s*cost\s*averaging|index\s*fund|etf|pe\s*ratio|fundamental\s*analysis|विविधीकरण|गुंतवणूक\s*विविधता|म्युच्युअल\s*फंड|एसआयपी|चक्रवाढ)",
        "Explains fundamental concepts such as asset allocation, diversification, rupee-cost averaging, and risk tolerance.",
        "एसेट एलोकेशन, विविधीकरण और बाजार के मूलभूत सिद्धांतों की समझाइश।",
        "गुंतवणुकीचे मूलभूत नियम, जोखीम व्यवस्थापन आणि विविधता यावर मार्गदर्शन."
    ),
    (
        r"(disclaimer|subject\s*to\s*market\s*(risks?|volatility)|market\s*volatility|not\s*financial\s*advice|do\s*your\s*own\s*research|dyor|past\s*performance\s*is\s*not|capital\s*at\s*risk|consult\s*(a|your)?\s*financial\s*advisor|बाजार\s*जोखिम|जोखीम\s*सूचना)",
        "Includes standard regulatory risk disclosures, volatility warnings, and investor caution.",
        "वैधानिक जोखिम चेतावनी और निवेशकों को स्वयं जांच करने की सलाह।",
        "कायदेशीर जोखीम इशारा आणि स्वतः खात्री करण्याचा योग्य सल्ला."
    ),
    (
        r"(long\s*term\s*(horizon|investing|wealth|goals?)|patient\s*investing|avoid\s*(greed|fomo|impulsive)|financial\s*(planning|discipline)|emergency\s*fund|asset\s*rebalancing|दीर्घकालीन|आर्थिक\s*नियोजन|संयम|धैर्य)",
        "Focuses on long-term wealth creation, personal financial discipline, and patience.",
        "दीर्घकालिक वित्तीय योजना, अनुशासन और लालच से बचने की सीख।",
        "दीर्घकालीन संपत्ती निर्मिती, आर्थिक शिस्त आणि संयमाचे महत्त्व."
    ),
    (
        r"(sebi\s*(registered|guidelines?|awareness)|scores\s*portal|regulatory\s*compliance|investor\s*education|investor\s*awareness|फायनान्शियल\s*लिटरसी|वित्तीय\s*साक्षरता)",
        "Emphasizes regulatory compliance, official verification, and investor protection rights.",
        "नियामक अनुपालन, आधिकारिक सत्यापन और निवेशक सुरक्षा अधिकारों पर जोर।",
        "नियामक नियम, अधिकृत पडताळणी आणि गुंतवणूकदार संरक्षण हक्क यावर भर."
    )
]

def classify_financial_content(content: str, platform: str = "Social Media", language: str = "en") -> Dict[str, Any]:
    if not content or not content.strip():
        return {
            "classification": "UNCERTAIN",
            "confidence": 0.5,
            "platform": platform,
            "promotional_score": 0,
            "educational_score": 0,
            "reasons": ["Content is empty or insufficient to evaluate."],
            "reasons_hi": ["सामग्री खाली है या मूल्यांकन के लिए अपर्याप्त है।"],
            "reasons_mr": ["मजकूर रिक्त आहे किंवा मूल्यमापनासाठी अपुरा आहे."],
            "risk_indicators": [],
            "risk_indicators_hi": [],
            "risk_indicators_mr": [],
            "educational_signals": [],
            "educational_signals_hi": [],
            "educational_signals_mr": [],
            "evidence_quality": "NONE",
            "explanation": "Please provide social media post text, video transcript, or caption to classify.",
            "explanation_hi": "कृपया जांच के लिए कोई सोशल मीडिया पोस्ट या संदेश दर्ज करें।",
            "explanation_mr": "कृपया तपासणीसाठी कोणताही सोशल मीडिया संदेश किंवा मजकूर टाका."
        }

    c_lower = content.lower()
    reasons = []
    reasons_hi = []
    reasons_mr = []
    risk_indicators = []
    risk_indicators_hi = []
    risk_indicators_mr = []
    edu_indicators = []
    edu_indicators_hi = []
    edu_indicators_mr = []

    # Check promotional patterns
    for pat, desc, desc_hi, desc_mr in PROMOTIONAL_PATTERNS:
        if re.search(pat, c_lower):
            risk_indicators.append(desc)
            risk_indicators_hi.append(desc_hi)
            risk_indicators_mr.append(desc_mr)

    # Check educational patterns
    for pat, desc, desc_hi, desc_mr in EDUCATIONAL_PATTERNS:
        if re.search(pat, c_lower):
            edu_indicators.append(desc)
            edu_indicators_hi.append(desc_hi)
            edu_indicators_mr.append(desc_mr)

    promo_count = len(risk_indicators)
    edu_count = len(edu_indicators)

    # Decision Matrix
    if promo_count >= 1 and edu_count >= 1:
        classification = "MIXED"
        confidence = 0.88
        evidence_quality = "MODERATE"
        reasons.extend(risk_indicators)
        reasons.extend(edu_indicators)
        reasons_hi.extend(risk_indicators_hi)
        reasons_hi.extend(edu_indicators_hi)
        reasons_mr.extend(risk_indicators_mr)
        reasons_mr.extend(edu_indicators_mr)
        explanation = (
            f"This {platform} content is MIXED. It uses genuine educational concepts as a wrapper to market an underlying "
            "trading channel, paid course, or private tip service. Separate the conceptual knowledge from the commercial call to action."
        )
        explanation_hi = (
            f"यह {platform} सामग्री 'मिश्रित' (Mixed) है। यह शैक्षणिक अवधारणाओं की आड़ में किसी कोर्स या पेड ग्रुप का प्रचार कर रही है। "
            "सीखने की बात अलग रखें और किसी भी पेड ग्रुप या टिप्स से बचें।"
        )
        explanation_mr = (
            f"हा {platform} मजकूर 'मिश्रित' (Mixed) स्वरूपाचा आहे. माहितीपूर्ण भाषेचा वापर करून शेवटी सशुल्क कोर्सेस किंवा टेलिग्राम चॅनेलचा प्रचार केला जात आहे. "
            "माहिती वेगळी ठेवा आणि आर्थिक आमिषांना बळी पडू नका."
        )
    elif promo_count >= 2 or (promo_count >= 1 and any(k in c_lower for k in ["guaranteed", "telegram", "jackpot", "sure shot", "vip", "10x", "नक्की", "गॅरंटी", "गारंटी"])):
        classification = "HIGH_RISK_PROMOTIONAL"
        confidence = 0.95
        evidence_quality = "NONE"
        reasons.extend(risk_indicators)
        reasons_hi.extend(risk_indicators_hi)
        reasons_mr.extend(risk_indicators_mr)
        explanation = (
            f"This {platform} content is classified as HIGH-RISK PROMOTIONAL. "
            "It exhibits multiple predatory marketing signals including guaranteed profits, private messaging funnels, or artificial urgency without substantiated proof."
        )
        explanation_hi = (
            f"यह {platform} सामग्री 'अत्यधिक जोखिम वाली प्रचारक' श्रेणी में आती है। "
            "इसमें गारंटीड रिटर्न, गुप्त टेलीग्राम ग्रुप्स और जल्दबाजी जैसे भ्रामक हथकंडे पाए गए हैं।"
        )
        explanation_mr = (
            f"हा {platform} मजकूर 'अत्यंत धोकादायक प्रचारक' म्हणून वर्गीकृत केला गेला आहे. "
            "यात हमी परतावा, खाजगी टेलिग्राम ग्रुप्स आणि घाईगडबडीचे आमिष स्पष्ट दिसत आहे."
        )
    elif promo_count >= 1:
        classification = "PROMOTIONAL"
        confidence = 0.88
        evidence_quality = "LOW"
        reasons.extend(risk_indicators)
        reasons_hi.extend(risk_indicators_hi)
        reasons_mr.extend(risk_indicators_mr)
        explanation = (
            f"This {platform} content is PROMOTIONAL. The primary intent is marketing a product, stock advisory, or course rather than objective public education."
        )
        explanation_hi = (
            f"यह {platform} सामग्री 'प्रचारक' (Promotional) है। इसका मुख्य उद्देश्य किसी वित्तीय उत्पाद या सेवा का विज्ञापन करना है।"
        )
        explanation_mr = (
            f"हा {platform} मजकूर 'प्रचारक' (Promotional) आहे. याचा मुख्य उद्देश उत्पादन किंवा सेवेची जाहिरात करणे हा आहे."
        )
    elif edu_count >= 1:
        classification = "EDUCATIONAL"
        confidence = 0.92
        evidence_quality = "HIGH"
        reasons.extend(edu_indicators)
        reasons_hi.extend(edu_indicators_hi)
        reasons_mr.extend(edu_indicators_mr)
        explanation = (
            f"This {platform} content is EDUCATIONAL. It explains fundamental financial principles, includes risk warnings, and refrains from pushing individual stock tips or paid funnels."
        )
        explanation_hi = (
            f"यह {platform} सामग्री 'सच्ची शैक्षणिक' (Educational) है। यह वित्तीय सिद्धांतों और जोखिम की समझ देती है और कोई टिप या निजी ग्रुप नहीं बेचती।"
        )
        explanation_mr = (
            f"हा {platform} मजकूर 'शैक्षणिक व मार्गदर्शक' आहे. यात वित्तीय तत्त्वे व जोखीम समजावून सांगितली आहे आणि कोणताही संशयास्पद प्रचार नाही."
        )
    else:
        classification = "UNCERTAIN"
        confidence = 0.65
        evidence_quality = "LOW"
        reasons.append("Content lacks prominent promotional hype or in-depth educational depth.")
        reasons_hi.append("सामग्री में न तो स्पष्ट प्रचार है और न ही गहन शैक्षणिक तत्व।")
        reasons_mr.append("मजकुरात कोणताही उघड प्रचार किंवा सखोल शैक्षणिक माहिती आढळली नाही.")
        explanation = "Content appears informal or neutral. Maintain healthy skepticism and verify specific financial claims independently."
        explanation_hi = "सामग्री सामान्य या अनौपचारिक है। हमेशा स्वतंत्र रूप से दावों की पुष्टि करें।"
        explanation_mr = "मजकूर सामान्य स्वरूपाचा आहे. कोणत्याही आर्थिक दाव्याची स्वतः खात्री करा."

    # Compute promotional percentage
    total_signals = promo_count + edu_count
    if classification == "MIXED":
        promotional_score = max(50, min(80, int((promo_count / total_signals) * 100)))
        educational_score = 100 - promotional_score
    elif total_signals > 0:
        promotional_score = int((promo_count / total_signals) * 100)
        educational_score = 100 - promotional_score
    else:
        promotional_score = 20
        educational_score = 80

    return {
        "classification": classification,
        "confidence": confidence,
        "platform": platform,
        "promotional_score": promotional_score,
        "educational_score": educational_score,
        "reasons": reasons,
        "reasons_hi": reasons_hi,
        "reasons_mr": reasons_mr,
        "risk_indicators": risk_indicators,
        "risk_indicators_hi": risk_indicators_hi,
        "risk_indicators_mr": risk_indicators_mr,
        "educational_signals": edu_indicators,
        "educational_signals_hi": edu_indicators_hi,
        "educational_signals_mr": edu_indicators_mr,
        "evidence_quality": evidence_quality,
        "explanation": explanation,
        "explanation_hi": explanation_hi,
        "explanation_mr": explanation_mr
    }
