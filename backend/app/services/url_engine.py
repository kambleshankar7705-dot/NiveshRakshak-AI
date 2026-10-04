from urllib.parse import urlparse
import re
from typing import Dict, Any, List

OFFICIAL_REGULATORS = {
    "sebi.gov.in",
    "rbi.org.in",
    "nseindia.com",
    "bseindia.com",
    "mca.gov.in",
    "incometax.gov.in",
    "cybercrime.gov.in",
    "scores.sebi.gov.in",
    "digilocker.gov.in"
}

POPULAR_BROKERS = [
    ("zerodha", "zerodha.com"),
    ("groww", "groww.in"),
    ("angelone", "angelone.in"),
    ("upstox", "upstox.com"),
    ("icicidirect", "icicidirect.com"),
    ("hdfcsec", "hdfcsec.com"),
    ("kotaksecurities", "kotaksecurities.com"),
    ("motilaloswal", "motilaloswal.com"),
    ("sharekhan", "sharekhan.com"),
    ("cdsl", "cdslindia.com"),
    ("nsdl", "nsdl.co.in")
]

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".click", ".vip", 
    ".work", ".buzz", ".monster", ".finance-vip", ".online", ".site",
    ".live", ".fit", ".rest", ".cam", ".sbs", ".cfd", ".shop", ".link"
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "is.gd", "t.me", "wa.me", "cutt.ly", 
    "rb.gy", "goo.gl", "rotf.lol", "ow.ly", "buff.ly"
}

SUSPICIOUS_KEYWORDS = [
    "guarantee", "profit", "wealth", "double", "invest-vip", "sebi-auth", 
    "rbi-bonus", "free-money", "fast-cash", "instant-return", "crypto-10x", 
    "jackpot", "sure-shot", "trading-bot", "deposit-double", "daily-return"
]

PHISHING_PATHS = [
    "deposit", "wallet", "claim-bonus", "login-otp", "upi-verify", 
    "transfer", "withdraw-bonus", "auth-token", "kyc-update", "free-grant"
]

def check_url_safety(url: str, language: str = "en") -> Dict[str, Any]:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not domain:
            domain = parsed.path.split("/")[0].lower()
        # Strip port if present in domain
        if ":" in domain:
            domain = domain.split(":")[0]
    except Exception:
        domain = "unknown"

    indicators: List[str] = []
    indicators_hi: List[str] = []
    indicators_mr: List[str] = []
    risk_score = 0

    # Whitelist check for official regulators
    is_official_regulator = any(domain == reg or domain.endswith("." + reg) for reg in OFFICIAL_REGULATORS)
    if is_official_regulator:
        return {
            "url": url,
            "domain": domain,
            "is_https": parsed.scheme == "https",
            "risk_level": "LOW",
            "risk_score": 0,
            "is_official_regulator": True,
            "suspicious_indicators": [],
            "suspicious_indicators_hi": [],
            "suspicious_indicators_mr": [],
            "checklist": [
                {
                    "item": "Official Government / Regulator Domain",
                    "item_hi": "आधिकारिक सरकारी / नियामक डोमेन",
                    "item_mr": "अधिकृत सरकारी / नियामक डोमेन",
                    "passed": True,
                    "note": "Verified legitimate official portal",
                    "note_hi": "सत्यापित आधिकारिक राष्ट्रीय पोर्टल",
                    "note_mr": "सत्यापित अधिकृत राष्ट्रीय पोर्टल"
                },
                {
                    "item": "HTTPS Encryption",
                    "item_hi": "एचटीटीपीएस (HTTPS) एन्क्रिप्शन",
                    "item_mr": "एचटीटीपीएस (HTTPS) सुरक्षितता",
                    "passed": parsed.scheme == "https",
                    "note": "Secure connection",
                    "note_hi": "सुरक्षित एन्क्रिप्टेड कनेक्शन",
                    "note_mr": "सुरक्षित एन्क्रिप्टेड कनेक्शन"
                },
                {
                    "item": "No URL Shortener Obfuscation",
                    "item_hi": "शॉर्ट यूआरएल द्वारा छुपाया नहीं गया",
                    "item_mr": "शॉर्ट लिंकद्वारे लपवले नाही",
                    "passed": True,
                    "note": "Direct destination domain",
                    "note_hi": "स्पष्ट प्रत्यक्ष गंतव्य",
                    "note_mr": "स्पष्ट थेट वेबसाईट"
                },
                {
                    "item": "No High-Risk TLD",
                    "item_hi": "विश्वसनीय डोमेन एक्सटेंशन",
                    "item_mr": "विश्वसनीय डोमेन एक्स्टेंशन",
                    "passed": True,
                    "note": "Recognized national .gov.in / corporate TLD",
                    "note_hi": "मान्यताप्राप्त .gov.in / .org.in डोमेन",
                    "note_mr": "मान्यताप्राप्त .gov.in / अधिकृत डोमेन"
                },
                {
                    "item": "No Phishing Path Markers",
                    "item_hi": "कोई फिशिंग पाथ नहीं",
                    "item_mr": "कोणताही फिशिंग मार्ग नाही",
                    "passed": True,
                    "note": "Clean path",
                    "note_hi": "सुरक्षित वेब पाथ",
                    "note_mr": "सुरक्षित वेब पाथ"
                }
            ],
            "explanation": f"The domain '{domain}' is an official, recognized Indian regulatory or government portal. It is safe for browsing.",
            "explanation_hi": f"डोमेन '{domain}' एक आधिकारिक व मान्यताप्राप्त भारतीय नियामक या सरकारी पोर्टल है। यह सुरक्षित है।",
            "explanation_mr": f"डोमेन '{domain}' हे एक अधिकृत आणि मान्यताप्राप्त भारतीय नियामक किंवा सरकारी पोर्टल आहे. हे सुरक्षित आहे.",
            "recommended_actions": [
                "Verify that the URL in your browser's address bar matches exactly.",
                "Ensure standard cyber hygiene and never share OTPs or passwords."
            ],
            "recommended_actions_hi": [
                "सुनिश्चित करें कि एड्रेस बार में यूआरएल बिल्कुल सही है।",
                "हमेशा सावधानी बरतें और कभी भी किसी के साथ पासवर्ड या ओटीपी साझा न करें।"
            ],
            "recommended_actions_mr": [
                "ब्राउझरच्या अ‍ॅड्रेस बारमधील लिंक तंतोतंत जुळत असल्याची खात्री करा.",
                "कधीही कोणाशीही पासवर्ड किंवा ओटीपी शेअर करू नका."
            ],
            "disclaimer": "Official regulatory domains are authenticated by Government of India authorities."
        }

    # 1. Check HTTPS
    is_https = parsed.scheme == "https"
    if not is_https:
        indicators.append("Missing HTTPS encryption: Connection is unencrypted, exposing data to interception.")
        indicators_hi.append("एचटीटीपीएस (HTTPS) एन्क्रिप्शन अनुपस्थित: डेटा चोरी होने का गंभीर खतरा है।")
        indicators_mr.append("एचटीटीपीएस (HTTPS) सुरक्षितता नाही: गोपनीय माहिती चोरीला जाण्याचा मोठा धोका आहे.")
        risk_score += 25

    # 2. Check for URL shorteners
    is_shortener = any(domain.endswith(s) or domain == s for s in SHORTENERS)
    if is_shortener:
        indicators.append(f"Shortened URL format ({domain}): Obscures the real final destination and server identity.")
        indicators_hi.append(f"शॉर्ट लिंक ({domain}): असली वेबसाइट का नाम छुपाने के लिए इस्तेमाल की गई है।")
        indicators_mr.append(f"शॉर्ट लिंक ({domain}): खरी वेबसाईट लपवण्यासाठी शॉर्ट लिंकचा वापर केला गेला आहे.")
        risk_score += 25

    # 3. Check for Suspicious TLDs
    matched_tld = [tld for tld in SUSPICIOUS_TLDS if domain.endswith(tld)]
    if matched_tld:
        indicators.append(f"High-risk top-level domain ({matched_tld[0]}): Often favored by disposable phishing domains.")
        indicators_hi.append(f"असुरक्षित डोमेन एक्सटेंशन ({matched_tld[0]}): फर्जी व अल्पकालिक ठगी साइटों द्वारा इस्तेमाल।")
        indicators_mr.append(f"धोकादायक डोमेन एक्स्टेंशन ({matched_tld[0]}): फसवेगिरी करणाऱ्या तात्पुरत्या साईट्स हे वापरतात.")
        risk_score += 30

    # 4. Check for IP address as host
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain):
        indicators.append("Direct IP address used instead of a registered domain name.")
        indicators_hi.append("रजिस्टर्ड डोमेन नाम के बजाय सीधे आईपी एड्रेस का उपयोग (अत्यधिक संदिग्ध)।")
        indicators_mr.append("नोंदणीकृत नावाऐवजी थेट आयपी अ‍ॅड्रेसचा वापर (अत्यंत संशयास्पद).")
        risk_score += 35

    # 5. Check for Punycode / IDN homograph attack
    if domain.startswith("xn--") or ".xn--" in domain:
        indicators.append("Internationalized Domain Name (Punycode): Often used in lookalike homograph attacks to impersonate real brands.")
        indicators_hi.append("प्यूनीकोड डोमेन (Punycode): असली ब्रांड जैसी दिखने वाली फर्जी वेबसाइट बनाने का तरीका।")
        indicators_mr.append("प्युनीकोड डोमेन (Punycode): नामांकित ब्रँडसारखी हुबेहूब बनावट वेबसाईट बनवण्याचा प्रकार.")
        risk_score += 35

    # 6. Check for deceptive financial keywords in URL
    url_lower = url.lower()
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in url_lower:
            indicators.append(f"Deceptive financial terminology in URL: '{kw}'.")
            indicators_hi.append(f"लिंक में भ्रामक वित्तीय लालच शब्द: '{kw}'।")
            indicators_mr.append(f"लिंकमध्ये संशयास्पद आमिष दाखवणारा शब्द: '{kw}'.")
            risk_score += 20
            break

    # 7. Check for impersonation of official regulators
    if "sebi" in domain and not domain.endswith("sebi.gov.in"):
        indicators.append("Impersonation Alert: Domain contains 'sebi' but is NOT the official sebi.gov.in portal.")
        indicators_hi.append("नियामक धोखाधड़ी: डोमेन में 'sebi' है लेकिन यह आधिकारिक sebi.gov.in नहीं है।")
        indicators_mr.append("नियामक तोतयागिरी: डोमेनमध्ये 'sebi' शब्द आहे परंतु हे अधिकृत sebi.gov.in नाही.")
        risk_score += 45

    if "rbi" in domain and not domain.endswith("rbi.org.in"):
        indicators.append("Impersonation Alert: Domain contains 'rbi' but is NOT the official rbi.org.in portal.")
        indicators_hi.append("नियामक धोखाधड़ी: डोमेन में 'rbi' है लेकिन यह आधिकारिक rbi.org.in नहीं है।")
        indicators_mr.append("नियामक तोतयागिरी: डोमेनमध्ये 'rbi' शब्द आहे परंतु हे अधिकृत rbi.org.in नाही.")
        risk_score += 45

    # 8. Check for popular broker lookalikes
    for broker_name, broker_official in POPULAR_BROKERS:
        if broker_name in domain and not (domain == broker_official or domain.endswith("." + broker_official)):
            indicators.append(f"Broker Impersonation: Domain contains '{broker_name}' but is NOT the official {broker_official} broker portal.")
            indicators_hi.append(f"ब्रोकर धोखाधड़ी: डोमेन में '{broker_name}' है लेकिन यह आधिकारिक {broker_official} नहीं है।")
            indicators_mr.append(f"ब्रोकर तोतयागिरी: डोमेनमध्ये '{broker_name}' आहे परंतु हे अधिकृत {broker_official} पोर्टल नाही.")
            risk_score += 40
            break

    # 9. Check for phishing path patterns
    path_lower = parsed.path.lower()
    for p in PHISHING_PATHS:
        if p in path_lower:
            indicators.append(f"Suspicious path keyword identified: '/{p}'. Often used in credential harvesting funnels.")
            indicators_hi.append(f"संदेहास्पद पाथ पहचान: '/{p}' (डेटा या पैसे चुराने का संभावित रास्ता)।")
            indicators_mr.append(f"संशयास्पद लिंक मार्ग: '/{p}' (माहिती किंवा पैसे लाटण्याचा प्रकार).")
            risk_score += 15
            break

    # Determine risk level
    risk_score = min(100, max(5, risk_score))
    if risk_score >= 60:
        risk_level = "HIGH"
        explanation = (
            f"The link '{domain}' displays high-risk characteristics ({indicators[0] if indicators else 'unverified target'}). "
            "Never enter Demat passwords, UPI PINs, bank details, or OTPs on this webpage."
        )
        explanation_hi = (
            f"लिंक '{domain}' में अत्यधिक गंभीर जोखिम के संकेत मिले हैं ({indicators_hi[0] if indicators_hi else 'संदिग्ध गंतव्य'})। "
            "इस वेबपेज पर कभी भी पासवर्ड, यूपीआई पिन या ओटीपी दर्ज न करें।"
        )
        explanation_mr = (
            f"लिंक '{domain}' मध्ये अत्यंत गंभीर धोक्याचे संकेत आढळले आहेत ({indicators_mr[0] if indicators_mr else 'संशयास्पद साईट'})। "
            "या पृष्ठावर कधीही पासवर्ड, डिमॅट माहिती किंवा यूपीआय पिन टाकू नका."
        )
        actions = [
            "Do not open or click this link. Do not download any APK files.",
            "Never enter personal, Demat, or banking credentials.",
            "Never authorize UPI payments or scan QR codes originating from this link.",
            "Report and block the sender on WhatsApp, Telegram, or SMS.",
            "File a phishing report at cybercrime.gov.in or call 1930."
        ]
        actions_hi = [
            "इस लिंक को न खोलें और न ही कोई एपीके (APK) फाइल डाउनलोड करें।",
            "कभी भी कोई व्यक्तिगत, डीमैट या बैंकिंग जानकारी दर्ज न करें।",
            "इस लिंक से जुड़े किसी भी क्यूआर कोड या यूपीआई पेमेंट को मंजूरी न दें।",
            "व्हाट्सएप या टेलीग्राम पर भेजने वाले को तुरंत ब्लॉक और रिपोर्ट करें।",
            "राष्ट्रीय साइबर अपराध पोर्टल (cybercrime.gov.in) या 1930 पर रिपोर्ट करें।"
        ]
        actions_mr = [
            "ही लिंक उघडू नका आणि कोणतीही एपीके (APK) फाईल डाऊनलोड करू नका.",
            "कोणतीही वैयक्तिक, डिमॅट किंवा बँक खात्याची माहिती देऊ नका.",
            "या लिंकशी संबंधित कोणताही क्यूआर कोड स्कॅन करू नका किंवा पेमेंट करू नका.",
            "व्हॉट्सअ‍ॅप किंवा टेलिग्रामवर पाठवणाऱ्या व्यक्तीला ब्लॉक व रिपोर्ट करा.",
            "राष्ट्रीय सायबर हेल्पलाइन १९३० वर किंवा cybercrime.gov.in वर तक्रार नोंदवा."
        ]
    elif risk_score >= 30:
        risk_level = "MEDIUM"
        explanation = (
            f"The link '{domain}' shows moderate risk factors such as {indicators[0] if indicators else 'unusual URL structure'}. "
            "Proceed with heightened caution and verify independently."
        )
        explanation_hi = (
            f"लिंक '{domain}' में मध्यम जोखिम पाया गया है ({indicators_hi[0] if indicators_hi else 'असामान्य यूआरएल संरचना'})। "
            "सतर्क रहें और आधिकारिक स्रोतों से पुष्टि करें।"
        )
        explanation_mr = (
            f"लिंक '{domain}' मध्ये मध्यम जोखीम आढळली आहे ({indicators_mr[0] if indicators_mr else 'संशयास्पद लिंक संरचना'})। "
            "सावधगिरी बाळगा आणि अधिकृत वेबसाईटवरून खात्री करा."
        )
        actions = [
            "Verify the official domain of the organization directly via a trusted search engine.",
            "Ensure the URL exactly matches the official domain name before providing information."
        ]
        actions_hi = [
            "संस्था की आधिकारिक वेबसाइट गूगल जैसे विश्वसनीय सर्च इंजन से स्वयं खोजें।",
            "कोई भी जानकारी देने से पहले सुनिश्चित करें कि डोमेन नाम बिल्कुल सही है।"
        ]
        actions_mr = [
            "संस्थेचे अधिकृत संकेतस्थळ स्वतः सर्च इंजिनवर शोधून खात्री करा.",
            "कोणतीही माहिती देण्यापूर्वी डोमेन नाव पूर्णपणे बरोबर असल्याची खात्री करा."
        ]
    else:
        risk_level = "LOW"
        explanation = f"The URL structure for '{domain}' appears standard. However, always exercise standard cyber vigilance."
        explanation_hi = f"डोमेन '{domain}' की संरचना सामान्य दिखाई देती है। फिर भी, हमेशा बुनियादी सुरक्षा सावधानियां बरतें।"
        explanation_mr = f"डोमेन '{domain}' ची रचना सामान्य दिसत आहे. तरीही नेहमी मूलभूत सायबर सुरक्षितता बाळगा."
        actions = [
            "Ensure the domain name exactly matches the service you intend to visit.",
            "Never share passwords, Demat credentials, or OTPs on any site."
        ]
        actions_hi = [
            "जांचें कि डोमेन नाम बिल्कुल उसी सेवा का है जिसका आप उपयोग करना चाहते हैं।",
            "किसी भी साइट पर कभी भी पासवर्ड, डीमैट विवरण या ओटीपी साझा न करें।"
        ]
        actions_mr = [
            "डोमेन नाव तुम्ही वापरू इच्छित असलेल्या सेवेचेच असल्याची खात्री करा.",
            "कोणत्याही संकेतस्थळावर कधीही पासवर्ड किंवा ओटीपी शेअर करू नका."
        ]

    # Detailed security checklist (Strictly 5 diagnostic items)
    checklist = [
        {
            "item": "HTTPS Encryption",
            "item_hi": "एचटीटीपीएस (HTTPS) एन्क्रिप्शन",
            "item_mr": "एचटीटीपीएस (HTTPS) सुरक्षितता",
            "passed": is_https,
            "note": "Secure encrypted communication" if is_https else "Insecure unencrypted HTTP",
            "note_hi": "सुरक्षित एन्क्रिप्टेड संचार" if is_https else "असुरक्षित अनएन्क्रिप्टेड कनेक्शन",
            "note_mr": "सुरक्षित एन्क्रिप्टेड संपर्क" if is_https else "असुरक्षित अनएन्क्रिप्टेड कनेक्शन"
        },
        {
            "item": "Regulator Impersonation Check",
            "item_hi": "नियामक तोतयागिरी तपासणी",
            "item_mr": "नियामक तोतयागिरी पडताळणी",
            "passed": "sebi" not in domain and "rbi" not in domain,
            "note": "Clean domain" if "sebi" not in domain and "rbi" not in domain else "Fake regulator keywords detected",
            "note_hi": "स्वच्छ डोमेन" if "sebi" not in domain and "rbi" not in domain else "फर्जी नियामक कीवर्ड मिले",
            "note_mr": "स्वच्छ डोमेन" if "sebi" not in domain and "rbi" not in domain else "बनावट नियामक शब्द आढळले"
        },
        {
            "item": "TLD Reputation",
            "item_hi": "डोमेन एक्सटेंशन प्रतिष्ठा",
            "item_mr": "डोमेन एक्स्टेंशन प्रतिष्ठा",
            "passed": not matched_tld,
            "note": "Standard top-level domain" if not matched_tld else f"High-risk disposable TLD ({matched_tld[0]})",
            "note_hi": "मानक सुरक्षित एक्सटेंशन" if not matched_tld else f"उच्च जोखिम वाला एक्सटेंशन ({matched_tld[0]})",
            "note_mr": "प्रमाणित सुरक्षित एक्स्टेंशन" if not matched_tld else f"धोकादायक तात्पुरते एक्स्टेंशन ({matched_tld[0]})"
        },
        {
            "item": "URL Shortener Check",
            "item_hi": "शॉर्ट यूआरएल जांच",
            "item_mr": "शॉर्ट लिंक तपासणी",
            "passed": not is_shortener,
            "note": "Direct destination" if not is_shortener else "Hidden destination via shortener",
            "note_hi": "प्रत्यक्ष गंतव्य" if not is_shortener else "शॉर्टनर द्वारा छुपाया गया गंतव्य",
            "note_mr": "थेट संकेतस्थळ" if not is_shortener else "शॉर्ट लिंकने लपवलेली साईट"
        },
        {
            "item": "Registered Domain Host",
            "item_hi": "रजिस्टर्ड होस्टनेम जांच",
            "item_mr": "नोंदणीकृत होस्ट तपासणी",
            "passed": not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain),
            "note": "Named host" if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain) else "Raw IP host",
            "note_hi": "मान्यताप्राप्त डोमेन होस्ट" if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain) else "सीधा संदिग्ध आईपी पता",
            "note_mr": "नोंदणीकृत डोमेन नाव" if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain) else "थेट संशयास्पद आयपी अ‍ॅड्रेस"
        }
    ]

    return {
        "url": url,
        "domain": domain,
        "is_https": is_https,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "is_official_regulator": False,
        "suspicious_indicators": indicators,
        "suspicious_indicators_hi": indicators_hi,
        "suspicious_indicators_mr": indicators_mr,
        "checklist": checklist,
        "explanation": explanation,
        "explanation_hi": explanation_hi,
        "explanation_mr": explanation_mr,
        "recommended_actions": actions,
        "recommended_actions_hi": actions_hi,
        "recommended_actions_mr": actions_mr,
        "disclaimer": (
            "URL safety assessments are informational heuristic checks and may not identify all malicious links. "
            "Always verify official domains directly."
        )
    }
