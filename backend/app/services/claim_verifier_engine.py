import re
from typing import Dict, Any, List

SEBI_REG_PATTERNS = {
    "RESEARCH_ANALYST": r"INH[0-9]{9}",
    "INVESTMENT_ADVISER": r"INA[0-9]{9}",
    "STOCK_BROKER": r"INZ[0-9]{9}",
    "PORTFOLIO_MANAGER": r"INP[0-9]{9}",
    "MERCHANT_BANKER": r"INM[0-9]{9}",
    "DEPOSITORY_PARTICIPANT": r"IN-DP-[0-9]{2,4}-[0-9]{4}",
    "MUTUAL_FUND": r"MF/[0-9]{3}/[0-9]{2}"
}

def verify_financial_claim(claim_text: str, language: str = "en") -> Dict[str, Any]:
    claim = claim_text.strip()
    c_lower = claim.lower()

    if not claim:
        return {
            "claim": "",
            "status": "INSUFFICIENT_EVIDENCE",
            "category": "EMPTY",
            "official_verification_status": "No claim provided to verify.",
            "reason": "Please provide a specific investment or regulatory claim to evaluate.",
            "reason_hi": "कृपया सत्यापन के लिए कोई विशिष्ट दावा दर्ज करें।",
            "reason_mr": "कृपया पडताळणीसाठी विशिष्ट दावा टाका.",
            "needed_evidence": "Valid official documentation or verifiable regulatory ID.",
            "needed_evidence_hi": "वैध आधिकारिक दस्तावेज या सेबी रजिस्ट्रेशन नंबर।",
            "needed_evidence_mr": "कायदेशीर अधिकृत कागदपत्रे किंवा सेबी नोंदणी क्रमांक.",
            "suggested_verification_steps": [],
            "suggested_verification_steps_hi": [],
            "suggested_verification_steps_mr": [],
            "evidence_checklist": [],
            "registry_url": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes",
            "scores_url": "https://scores.sebi.gov.in",
            "sachet_url": "https://sachet.rbi.org.in",
            "demo_badge": "Demo Verification Engine",
            "disclaimer": "NiveshRakshak AI provides investor-protection education only."
        }

    # 1. Check for Guaranteed Return Claims
    if re.search(r"(guarantee|100%\s*(return|profit)|double\s*your\s*money|fixed\s*return|zero\s*risk|नक्की\s*परतावा|पैसे\s*दुप्पट|गॅरंटीड|गारंटीड|खात्रीशीर|नक्की\s*नफा|फिक्स\s*रिटर्न|रोज\s*कमाई)", c_lower):
        return {
            "claim": claim,
            "status": "UNVERIFIED",
            "category": "GUARANTEED_RETURN",
            "official_verification_status": "PROHIBITED UNDER SEBI REGULATIONS",
            "reason": (
                "Under SEBI (Prohibition of Fraudulent and Unfair Trade Practices) Regulations, "
                "no registered intermediary is legally permitted to assure or guarantee fixed returns on market investments. "
                "Any claim of guaranteed market return is unlawful and represents a critical scam indicator."
            ),
            "reason_hi": (
                "सेबी (SEBI) के नियमों के तहत किसी भी पंजीकृत सलाहकार या संस्था को शेयर बाजार में गारंटीड या फिक्स रिटर्न का वादा करने की अनुमति नहीं है। "
                "गारंटीड मुनाफे का कोई भी दावा गैर-कानूनी और वित्तीय धोखाधड़ी का संकेत है।"
            ),
            "reason_mr": (
                "सेबीच्या (SEBI) नियमांनुसार बाजारातील कोणत्याही गुंतवणुकीवर निश्चित किंवा गॅरंटीड परतावा देण्याचे आश्वासन देणे बेकायदेशीर आहे. "
                "नक्की परताव्याचा कोणताही दावा आर्थिक फसवणुकीचे मुख्य लक्षण आहे."
            ),
            "needed_evidence": "No legitimate entity can legally provide evidence for guaranteed market returns because equity and derivatives fluctuate by law.",
            "needed_evidence_hi": "कोई भी वैध संस्था गारंटीड रिटर्न का कानूनी दस्तावेज नहीं दे सकती क्योंकि बाजार में उतार-चढ़ाव स्वाभाविक है।",
            "needed_evidence_mr": "कोणतीही कायदेशीर संस्था हमी परताव्याचा अधिकृत पुरावा देऊ शकत नाही, कारण बाजारात जोखीम अपरिहार्य असते.",
            "suggested_verification_steps": [
                "Recognize any guaranteed market return promise as an immediate red flag.",
                "Do not deposit funds into personal or private UPI handles.",
                "Report the unauthorized solicitation to SEBI SCORES (scores.sebi.gov.in) and National Cyber Crime Portal (cybercrime.gov.in)."
            ],
            "suggested_verification_steps_hi": [
                "गारंटीड रिटर्न के वादे को तुरंत धोखाधड़ी का गंभीर संकेत मानें।",
                "किसी भी निजी बैंक खाते या यूपीआई पर पैसे ट्रांसफर न करें।",
                "सेबी के स्कोर्स पोर्टल (scores.sebi.gov.in) और 1930 पर शिकायत दर्ज करें।"
            ],
            "suggested_verification_steps_mr": [
                "नक्की परताव्याचे आश्वासन दिसताच सावध व्हा आणि हा फसवणुकीचा प्रकार ओळखा.",
                "कोणत्याही खाजगी खात्यावर किंवा यूपीआयवर पैसे पाठवू नका.",
                "सेबीच्या स्कोर्स पोर्टलवर (scores.sebi.gov.in) आणि हेल्पलाइन १९३० वर तक्रार नोंदवा."
            ],
            "demo_badge": "Regulatory Compliance Check: PROHIBITED CLAIM",
            "disclaimer": "SEBI explicitly prohibits all market intermediaries from promising fixed or guaranteed returns."
        }

    # 2. Check for SEBI Registration Claims with explicit Registration Number
    found_sebi_num = None
    sebi_type = None
    for category, pattern in SEBI_REG_PATTERNS.items():
        match = re.search(pattern, claim, re.IGNORECASE)
        if match:
            found_sebi_num = match.group(0).upper()
            sebi_type = category.replace("_", " ").title()
            break

    if found_sebi_num:
        return {
            "claim": claim,
            "status": "PARTIALLY_VERIFIED",
            "category": "SEBI_REGISTRATION",
            "official_verification_status": f"SYNTACTICALLY VALID SEBI REGISTRATION PATTERN ({found_sebi_num})",
            "reason": (
                f"The provided registration code '{found_sebi_num}' matches the valid statutory format for a SEBI {sebi_type}. "
                "However, scammers often steal real registration numbers of genuine advisors to impersonate them."
            ),
            "reason_hi": (
                f"प्रदान किया गया रजिस्ट्रेशन नंबर '{found_sebi_num}' सेबी ({sebi_type}) के आधिकारिक प्रारूप से मेल खाता है। "
                "लेकिन धोखेबाज अक्सर असली सलाहकारों के नंबर चुराकर फर्जीवाड़ा करते हैं, इसलिए आधिकारिक पोर्टल पर नाम और पते की पुष्टि आवश्यक है।"
            ),
            "reason_mr": (
                f"दाखवलेला नोंदणी क्रमांक '{found_sebi_num}' सेबीच्या ({sebi_type}) अधिकृत रचनेशी जुळतो. "
                "तथापि, फसवणूक करणारे अनेकदा अधिकृत सल्लागारांचे क्रमांक चोरून वापरतात, म्हणून अधिकृत पोर्टलवर थेट खात्री करणे गरजेचे आहे."
            ),
            "needed_evidence": f"Official SEBI Certificate of Registration for '{found_sebi_num}' with registered corporate email, telephone, and registered office matching the person contacting you.",
            "needed_evidence_hi": f"सेबी का आधिकारिक सर्टिफिकेट, तथा अधिकृत ईमेल व फोन नंबर जो sebi.gov.in पर दर्ज पते से मेल खाता हो।",
            "needed_evidence_mr": f"सेबीचे अधिकृत नोंदणी प्रमाणपत्र आणि sebi.gov.in वर नोंदवलेला अधिकृत ई-मेल व फोन नंबर.",
            "suggested_verification_steps": [
                "Visit sebi.gov.in -> Recognised Intermediaries -> Search by Registration Number.",
                f"Search for '{found_sebi_num}' and confirm the legal company name and validity period.",
                "Cross-check that the contact telephone number and email domain match exactly.",
                "Ensure payments are deposited into the registered corporate bank account, NEVER an individual's personal savings account."
            ],
            "suggested_verification_steps_hi": [
                "sebi.gov.in पर जाएं -> Recognised Intermediaries -> रजिस्ट्रेशन नंबर से खोजें।",
                f"'{found_sebi_num}' खोजें और संस्था का कानूनी नाम व वैधता जांचें।",
                "सुनिश्चित करें कि फोन और ईमेल आईडी सेबी के रिकॉर्ड से बिल्कुल मेल खाती हो।",
                "भुगतान केवल अधिकृत कंपनी खाते में करें, किसी व्यक्ति के निजी खाते में कभी नहीं।"
            ],
            "suggested_verification_steps_mr": [
                "sebi.gov.in वर जा -> Recognised Intermediaries -> नोंदणी क्रमांकाने शोधा.",
                f"'{found_sebi_num}' शोधून अधिकृत नाव आणि मुदत तपासा.",
                "फोन नंबर आणि ई-मेल अधिकृत नोंदीशी जुळत असल्याची खात्री करा.",
                "पैसे केवळ अधिकृत कंपनीच्या खात्यात भरा, कोणाच्याही वैयक्तिक खात्यावर नाही."
            ],
            "demo_badge": "Format Validated: Final Verification on sebi.gov.in Required",
            "disclaimer": "Live SEBI Intermediary Registry API integration is in future scope. Verification computed via compliance heuristic database."
        }

    # 3. Check for SEBI / RBI / Govt Claims WITHOUT registration number
    if re.search(r"(sebi\s*(approved|certified|registered|मान्यता)|rbi\s*(approved|scheme|licensed)|government\s*(approved|scheme)|सरकारी\s*(योजना|स्कीम)|सेबी\s*मान्यता)", c_lower):
        return {
            "claim": claim,
            "status": "UNVERIFIED",
            "category": "REGULATOR_IMPERSONATION",
            "official_verification_status": "UNVERIFIED REGULATORY CLAIM (MISSING REGISTRATION NUMBER)",
            "reason": (
                "The claim asserts affiliation or approval by SEBI, RBI, or Government authorities, but does not provide "
                "the mandatory 12-digit statutory Registration Number. Unverified claims of official approval are a primary sign of financial impersonation."
            ),
            "reason_hi": (
                "इस दावे में सेबी (SEBI), आरबीआई (RBI) या सरकार से मान्यता का दावा किया गया है, लेकिन कोई 12 अंकों का रजिस्ट्रेशन नंबर नहीं दिया गया है। "
                "बिना नंबर के सेबी की मान्यता का दावा करना वित्तीय ठगी का सामान्य तरीका है।"
            ),
            "reason_mr": (
                "या संदेशात सेबी (SEBI) किंवा सरकारची मान्यता असल्याचा दावा आहे, परंतु १२-अंकी अधिकृत नोंदणी क्रमांक दिलेला नाही. "
                "क्रमांकाशिवाय सेबीच्या नावाचा वापर करणे ही तोतयागिरी व फसवणूक असू शकते."
            ),
            "needed_evidence": "12-digit statutory SEBI Registration Number (starting with INH, INA, INZ, or INP) and matching official certificate issued by SEBI.",
            "needed_evidence_hi": "12 अंकों का सेबी रजिस्ट्रेशन नंबर (INH, INA, INZ आदि से शुरू) और सेबी द्वारा जारी आधिकारिक प्रमाण पत्र।",
            "needed_evidence_mr": "१२-अंकी अधिकृत सेबी नोंदणी क्रमांक (INH, INA, INZ ने सुरू होणारा) आणि अधिकृत प्रमाणपत्र.",
            "suggested_verification_steps": [
                "Demand the 12-character alphanumeric SEBI registration number in writing.",
                "If they refuse, provide excuses, or send a cropped photo/PDF, CEASE communication immediately.",
                "Remember that RBI and SEBI NEVER run retail wealth schemes or give trading recommendations.",
                "Report the impersonation to the national cybercrime portal at 1930."
            ],
            "suggested_verification_steps_hi": [
                "लिखित रूप में 12 अंकों का सेबी रजिस्ट्रेशन नंबर मांगें।",
                "यदि वे कोई बहाना बनाएं या फोटो भेजें, तो तुरंत बातचीत बंद कर दें।",
                "याद रखें कि सेबी या आरबीआई कभी भी कोई निवेश स्कीम नहीं चलाते।",
                "राष्ट्रीय साइबर अपराध पोर्टल 1930 पर रिपोर्ट करें।"
            ],
            "suggested_verification_steps_mr": [
                "लेखी स्वरूपात १२-अंकी सेबी नोंदणी क्रमांक मागा.",
                "जर ते टाळाटाळ करत असतील किंवा मोबाईलवरील फोटो दाखवत असतील, तर त्वरित संवाद थांबवा.",
                "लक्षात ठेवा की सेबी किंवा आरबीआय कधीही स्वतः गुंतवणुकीच्या योजना चालवत नाही.",
                "सायबर हेल्पलाइन १९३० वर तक्रार नोंदवा."
            ],
            "demo_badge": "Missing Mandatory Registration Credentials",
            "disclaimer": "Genuine market advisors are legally required to state their registration number in all communications."
        }

    # 4. Check for Insider Tips / Secret Formula / 100% Accuracy
    if re.search(r"(insider\s*(tip|call|info)|secret\s*(formula|algorithm)|100%\s*accuracy|sure\s*shot|jackpot\s*call|10x\s*in|पक्का\s*कॉल|खात्रीशीर)", c_lower):
        return {
            "claim": claim,
            "status": "UNVERIFIED",
            "category": "MARKET_MANIPULATION",
            "official_verification_status": "HIGH-RISK MARKET MANIPULATION SIGNALS",
            "reason": (
                "Trading on material non-public 'insider information' is strictly illegal under SEBI (Prohibition of Insider Trading) Regulations. "
                "Furthermore, claims of 'secret algorithms' or 'sure shot 100% accuracy' are mathematically impossible in volatile capital markets."
            ),
            "reason_hi": (
                "इनसाइडर जानकारी के आधार पर ट्रेडिंग करना सेबी के इनसाइडर ट्रेडिंग नियमों के तहत गंभीर अपराध है। "
                "इसके अलावा '100% अचूक कॉल' या 'सीक्रेट फॉर्मूला' का दावा पूरी तरह भ्रामक है।"
            ),
            "reason_mr": (
                "इनसाइडर माहितीवर ट्रेडिंग करणे सेबीच्या नियमांनुसार बेकायदेशीर आहे. "
                "तसेच १००% अचूक कॉल किंवा गुप्त फॉर्म्युल्याचे दावे दिशाभूल करणारे असतात."
            ),
            "needed_evidence": "Verifiable audited performance track record certified by a qualified statutory auditor and published under SEBI guidelines.",
            "needed_evidence_hi": "मान्यताप्राप्त चार्टर्ड अकाउंटेंट (CA) द्वारा प्रमाणित ऑडिटेड ट्रैक रिकॉर्ड।",
            "needed_evidence_mr": "अधिकृत सीए (CA) द्वारे प्रमाणित केलेला ऑडिटेड नफा-तोटा अहवाल.",
            "suggested_verification_steps": [
                "Never trade based on social media group tips or pump-and-dump channels.",
                "Do not pay subscription fees for 'jackpot calls' or VIP channels.",
                "Consult only SEBI-registered Research Analysts (RA) or Investment Advisers (IA)."
            ],
            "suggested_verification_steps_hi": [
                "सोशल मीडिया या टेलीग्राम ग्रुप्स के टिप्स पर कभी पैसे न लगाएं।",
                "वीआईपी या जैकपॉट कॉल्स के लिए कोई सब्सक्रिप्शन फीस न दें।",
                "केवल सेबी-पंजीकृत रिसर्च एनालिस्ट या सलाहकारों से परामर्श लें।"
            ],
            "suggested_verification_steps_mr": [
                "सोशल मीडिया किंवा टेलिग्राम ग्रुप्समधील टिप्सवर कधीही व्यवहार करू नका.",
                "जॅकपॉट कॉल्ससाठी कोणतेही शुल्क देऊ नका.",
                "फक्त सेबी-नोंदणीकृत अधिकृत सल्लागारांचा सल्ला घ्या."
            ],
            "demo_badge": "High-Risk Unregulated Solicitation",
            "disclaimer": "Past returns do not guarantee future performance in volatile financial markets."
        }

    # 5. Default General Financial Claim
    return {
        "claim": claim,
        "status": "INSUFFICIENT_EVIDENCE",
        "category": "GENERAL_CLAIM",
        "official_verification_status": "INSUFFICIENT DOCUMENTARY EVIDENCE",
        "reason": (
            "The statement makes financial or commercial claims without attaching verifiable documentary proof, "
            "exchange filings (NSE/BSE), or audited statutory accounts."
        ),
        "reason_hi": (
            "इस दावे में वित्तीय या व्यावसायिक दावे किए गए हैं, लेकिन कोई आधिकारिक ऑडिटेड दस्तावेज या एक्सचेंज फाइलिंग संलग्न नहीं है।"
        ),
        "reason_mr": (
            "या संदेशामध्ये आर्थिक दावे केले आहेत, परंतु कोणताही अधिकृत पुरावा किंवा कंपनीचा ऑडिट रिपोर्ट दिलेला नाही."
        ),
        "needed_evidence": "Audited balance sheet, SEBI/MCA statutory filings, or corporate exchange announcements on nseindia.com or bseindia.com.",
        "needed_evidence_hi": "ऑडिट की गई बैलेंस शीट, सेबी/एमसीए फाइलिंग या एनएसई/बीएसई पर कंपनी की आधिकारिक घोषणा।",
        "needed_evidence_mr": "ऑडिट केलेला ताळेबंद, सेबी/एमसीए नोंदणी किंवा एनएसई/बीएसई वरील अधिकृत घोषणा.",
        "suggested_verification_steps": [
            "Request official corporate filings on the Ministry of Corporate Affairs portal (mca.gov.in).",
            "Verify all stock corporate actions directly on official exchange portals (nseindia.com / bseindia.com).",
            "Consult an independent financial professional before committing funds."
        ],
        "suggested_verification_steps_hi": [
            "कॉर्पोरेट मामलों के मंत्रालय (mca.gov.in) पर कंपनी के रिकॉर्ड की जांच करें।",
            "एक्सचेंज पोर्टल (nseindia.com / bseindia.com) पर आधिकारिक घोषणाओं की पुष्टि करें।",
            "पैसे लगाने से पहले स्वतंत्र वित्तीय पेशेवर से सलाह लें।"
        ],
        "suggested_verification_steps_mr": [
            "कंपनी व्यवहार मंत्रालय (mca.gov.in) वर कंपनीची नोंद तपासा.",
            "एक्सचेंज पोर्टल्सवर (nseindia.com / bseindia.com) अधिकृत माहितीची खात्री करा.",
            "गुंतवणुकीपूर्वी अधिकृत आर्थिक सल्लागाराशी चर्चा करा."
        ],
        "demo_badge": "Independent Document Verification Required",
        "disclaimer": "NiveshRakshak AI evaluates claims using deterministic compliance heuristics."
    }
