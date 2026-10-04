# Comprehensive Seed Data for NiveshRakshak AI
# Covers Demo Cases, Financial Concepts in EN/HI/MR, and Resilience Quiz Questions

DEMO_CASES = [
    {
        "id": "demo-1",
        "title": "Guaranteed-Return WhatsApp Scam",
        "title_hi": "गारंटीड रिटर्न व्हाट्सएप स्कैम",
        "title_mr": "नक्की परतावा देणारा व्हॉट्सअ‍ॅप घोटाळा",
        "input_type": "TEXT",
        "description": "Unsolicited WhatsApp message promising ₹50,000 on a ₹10,000 investment in 30 days with VIP Telegram invite.",
        "content": "URGENT! SEBI APPROVED OPPORTUNITY. Invest ₹10,000 today and get ₹50,000 guaranteed within 30 days. No risk, 100% fixed profit. Only 5 slots left! Send money immediately via UPI to secure your spot. Join our Telegram VIP group: https://t.me/vip_invest_sure",
        "expected_risk_level": "VERY_HIGH",
        "expected_score": 87,
        "key_red_flags": ["Guaranteed return claim", "Unrealistic profit promise", "Urgency / Time pressure", "Fake authority claim", "Social media solicitation"]
    },
    {
        "id": "demo-2",
        "title": "Fake Regulatory / Government Authority Scheme",
        "title_hi": "फर्जी सरकारी व सेबी योजना",
        "title_mr": "बनावट सेबी व सरकारी योजना",
        "input_type": "TEXT",
        "description": "Message impersonating RBI & SEBI officers asking for an upfront registration fee and Aadhaar/OTP.",
        "content": "Official Notification: RBI & SEBI Joint National Wealth Multiplier Scheme 2025. Pay mandatory registration fee ₹2,500 to authorized executive personal account. Send your OTP and Aadhaar card photo to claim guaranteed ₹1,00,000 grant.",
        "expected_risk_level": "VERY_HIGH",
        "expected_score": 90,
        "key_red_flags": ["Fake Authority / Regulatory Claim", "Credential / OTP Request", "Payment / Transfer Pressure", "Unsupported Financial Claim"]
    },
    {
        "id": "demo-3",
        "title": "Telegram Stock Tip & Pump Scheme",
        "title_hi": "टेलीग्राम स्टॉक टिप व पंप स्कीम",
        "title_mr": "टेलिग्राम शेअर मार्केट टिप घोटाळा",
        "input_type": "TEXT",
        "description": "Private Telegram operator claiming 100% insider jackpot tips for tomorrow's market open.",
        "content": "Tomorrow 9:15 AM! 100% SURE SHOT JACKPOT CALL! Penny stock will do 10X in 2 weeks! Insider operator buying confirmed. Join VIP Premium Group for ₹4,999. Hurry, offer expires at midnight! Don't miss out on life-changing profit!",
        "expected_risk_level": "HIGH",
        "expected_score": 75,
        "key_red_flags": ["Unrealistic Profit Promise", "Social Media Solicitation", "Urgency / FOMO Pressure", "Unsupported Financial Claim"]
    },
    {
        "id": "demo-4",
        "title": "Legitimate Educational Financial Content",
        "title_hi": "सच्ची शैक्षणिक वित्तीय सामग्री",
        "title_mr": "योग्य आणि मार्गदर्शक शैक्षणिक माहिती",
        "input_type": "TEXT",
        "description": "Standard investor education post explaining asset allocation, diversification, and mutual fund risk factors.",
        "content": "Investor Education: Diversification across different asset classes (equity, debt, gold) helps reduce portfolio concentration risk over long horizons. Market investments are subject to market volatility. Mutual fund NAV fluctuates based on underlying market values. Always assess your financial goals and risk tolerance before investing.",
        "expected_risk_level": "LOW",
        "expected_score": 10,
        "key_red_flags": []
    },
    {
        "id": "demo-5",
        "title": "Suspicious Phishing Investment URL",
        "title_hi": "संदिग्ध फिशिंग निवेश लिंक",
        "title_mr": "संशयास्पद फिशिंग गुंतवणूक लिंक",
        "input_type": "URL",
        "description": "Unencrypted HTTP link on a disposable .xyz domain impersonating SEBI approval.",
        "content": "http://sebi-authorized-wealth-guaranteed.xyz/deposit?ref=telegram_vip",
        "expected_risk_level": "HIGH",
        "expected_score": 85,
        "key_red_flags": ["Missing HTTPS encryption", "High-risk .xyz TLD", "Deceptive regulatory keywords", "Shortened / Referral funnel"]
    }
]

LEARNING_TOPICS = [
    {
        "id": "topic-1",
        "title": "What is Risk?",
        "title_hi": "जोखिम (Risk) क्या है?",
        "title_mr": "जोखीम (Risk) म्हणजे काय?",
        "category": "Fundamentals",
        "simple_explanation": "Risk is the chance that your actual investment outcome will differ from what you expect, including the possibility of losing some or all of your invested money.",
        "simple_explanation_hi": "जोखिम वह संभावना है कि आपको उम्मीद से कम फायदा हो या आपका लगाया हुआ पैसा कम या खत्म हो जाए।",
        "simple_explanation_mr": "गुंतवलेल्या पैशांवर अपेक्षेपेक्षा कमी परतावा मिळणे किंवा मुद्दल कमी होण्याची शक्यता म्हणजे जोखीम.",
        "everyday_analogy": "Like carrying an umbrella: There is a chance of rain, so you prepare rather than pretending rain does not exist.",
        "everyday_analogy_hi": "जैसे बारिश के मौसम में छाता लेकर निकलना। बारिश होगी या नहीं यह निश्चित नहीं है, लेकिन तैयारी जरूरी है।",
        "everyday_analogy_mr": "पावसाळ्यात बाहेर पडताना छत्री सोबत ठेवण्यासारखे आहे. पाऊस पडू शकतो, म्हणून खबरदारी घ्यावी लागते.",
        "example": "If you buy shares of a company, the price can go up if the company prospers, or fall if it faces losses.",
        "remember_this": "Higher potential returns always come with higher potential risks. No risk = low returns.",
        "common_misconception": "Misconception: 'Government approved means zero risk'. Reality: Regulators set rules, but market investments always carry market risk.",
        "quiz": {
            "question": "If someone promises high returns with zero risk, what is the reality?",
            "options": ["It is a miracle investment", "Every high return carries risk; guaranteed zero risk is a major red flag", "All banks offer this", "Risk does not apply to stocks"],
            "correct": 1
        }
    },
    {
        "id": "topic-2",
        "title": "What is Volatility?",
        "title_hi": "उतार-चढ़ाव (Volatility) क्या है?",
        "title_mr": "बाजारातील चढ-उतार (Volatility) म्हणजे काय?",
        "category": "Fundamentals",
        "simple_explanation": "Volatility measures how quickly and sharply prices of an asset go up and down over a period of time.",
        "simple_explanation_hi": "किसी शेयर या संपत्ति की कीमत कितनी तेजी से ऊपर या नीचे जाती है, उसे वोलैटिलिटी कहते हैं।",
        "simple_explanation_mr": "एखाद्या शेअरचे किंवा मालमत्तेचे भाव किती वेगाने वर-खाली होतात, त्याला चढ-उतार (Volatility) म्हणतात.",
        "everyday_analogy": "Like ocean waves: Some days the water is calm; on windy days the waves fluctuate wildly.",
        "everyday_analogy_hi": "जैसे समुद्र की लहरें। कभी शांत तो कभी बहुत तेज हिचकोले खाती हैं।",
        "everyday_analogy_mr": "समुद्राच्या लाटांसारखे. कधी पाणी शांत असते, तर वादळात लाटा खूप उंच उसळतात.",
        "example": "A stock priced at ₹100 swinging between ₹85 and ₹115 in a week is more volatile than a bond varying by ₹1.",
        "remember_this": "Volatility is normal in financial markets; it is not the same as permanent loss if you hold quality assets long-term.",
        "common_misconception": "Misconception: 'A drop in price today means you lost money forever.' Reality: Daily price changes are normal fluctuations.",
        "quiz": {
            "question": "What should a long-term investor do during normal market volatility?",
            "options": ["Panic and sell everything immediately", "Stick to their planned financial goals and avoid rash emotional decisions", "Borrow money to gamble", "Stop monitoring their finances"],
            "correct": 1
        }
    },
    {
        "id": "topic-3",
        "title": "What is Diversification?",
        "title_hi": "विविधीकरण (Diversification) क्या है?",
        "title_mr": "विविधता (Diversification) म्हणजे काय?",
        "category": "Strategy",
        "simple_explanation": "Diversification means spreading your investments across different assets (like equities, fixed income, gold) so that a loss in one does not ruin your entire savings.",
        "simple_explanation_hi": "अपने सारे पैसे एक ही जगह न लगाकर अलग-अलग जगहों (जैसे शेयर, बैंक एफडी, सोना) में बांटना।",
        "simple_explanation_mr": "आपले सर्व पैसे एकाच ठिकाणी न गुंतवता विविध पर्यायांमध्ये (उदा. शेअर्स, बँक ठेवी, सोने) विभागणे.",
        "everyday_analogy": "Don't put all your eggs in one basket: If the basket drops, all eggs break.",
        "everyday_analogy_hi": "सारे अंडे एक ही टोकरी में न रखें। टोकरी गिरी तो सारे अंडे फूट जाएंगे।",
        "everyday_analogy_mr": "सर्व अंडी एकाच टोपलीत ठेवू नका; टोपली पडली तर सर्व अंडी फुटतील.",
        "example": "If you hold shares in 10 different industries, a temporary downturn in automobile does not wipe out your savings.",
        "remember_this": "Diversification reduces concentration risk and smooths out the journey.",
        "common_misconception": "Misconception: 'Putting all money into one hot tip makes me rich fast.' Reality: It drastically increases your probability of catastrophic loss.",
        "quiz": {
            "question": "Why is diversification recommended?",
            "options": ["To guarantee you never pay taxes", "To reduce the risk of a single bad investment wiping out your wealth", "Because regulators force it", "To double your money in 24 hours"],
            "correct": 1
        }
    },
    {
        "id": "topic-4",
        "title": "What is Compounding?",
        "title_hi": "चक्रवृद्धि (Compounding) क्या है?",
        "title_mr": "चक्रवाढ (Compounding) म्हणजे काय?",
        "category": "Fundamentals",
        "simple_explanation": "Compounding is earning returns on your original investment plus on the returns that have accumulated over previous periods.",
        "simple_explanation_hi": "मूलधन के साथ-साथ कमाए हुए ब्याज पर भी ब्याज मिलना। समय के साथ यह बहुत तेजी से बढ़ता है।",
        "simple_explanation_mr": "मुद्दलावर मिळालेल्या व्याजावर किंवा परताव्यावर पुन्हा परतावा मिळणे म्हणजे चक्रवाढ.",
        "everyday_analogy": "Like a small snowball rolling down a snow-covered hill: It picks up more snow and grows exponentially larger with time.",
        "everyday_analogy_hi": "जैसे बर्फ का एक छोटा गोला ढलान पर लुढ़कते-लुढ़कते बहुत बड़ा बन जाता है।",
        "everyday_analogy_mr": "बर्फाचा छोटा गोळा डोंगरावरून खाली येताना मोठा होत जाण्यासारखे आहे.",
        "example": "₹10,000 invested at 10% annual return grows not in equal steps, but accelerates over 10, 20, and 30 years.",
        "remember_this": "Time in the market is the greatest fuel for compounding, not timing the market.",
        "common_misconception": "Misconception: 'Compounding works overnight.' Reality: Real compounding requires patience and years.",
        "quiz": {
            "question": "What is the key ingredient needed for compounding to create substantial wealth?",
            "options": ["Day trading tips", "Time and consistent discipline", "Borrowing heavy debt", "Switching brokers weekly"],
            "correct": 1
        }
    },
    {
        "id": "topic-5",
        "title": "What is Net Asset Value (NAV)?",
        "title_hi": "एनएवी (NAV) क्या होता है?",
        "title_mr": "एनएव्ही (NAV) म्हणजे काय?",
        "category": "Mutual Funds",
        "simple_explanation": "NAV represents the market value of one unit of a mutual fund scheme, calculated by subtracting liabilities from total assets and dividing by total units.",
        "simple_explanation_hi": "म्यूचुअल फंड की एक यूनिट की वास्तविक बाजार कीमत को NAV कहा जाता है।",
        "simple_explanation_mr": "म्युच्युअल फंडाच्या एका युनिटचे बाजारमूल्य म्हणजे एनएव्ही (NAV).",
        "everyday_analogy": "Like slicing a whole pizza into equal slices: NAV is the value of a single slice.",
        "everyday_analogy_hi": "जैसे एक बड़े पिज़्ज़ा को बराबर टुकड़ों में काटना। एक टुकड़े की कीमत उसका NAV है।",
        "everyday_analogy_mr": "मोठ्या पिझ्झाचे समान तुकडे करण्यासारखे; एका तुकड्याचे मूल्य म्हणजे एनएव्ही.",
        "example": "A fund with ₹100 crore in assets and 1 crore units has an NAV of ₹100 per unit.",
        "remember_this": "A fund with ₹10 NAV is not 'cheaper' or better than a fund with ₹100 NAV; it simply represents a different unit split.",
        "common_misconception": "Misconception: 'Low NAV means the mutual fund is a bargain.' Reality: Percentage returns depend on portfolio growth, not the nominal NAV.",
        "quiz": {
            "question": "Does a lower NAV make a mutual fund inherently cheaper or more profitable?",
            "options": ["Yes, always", "No, NAV is just the per-unit value and doesn't dictate future percentage returns", "Only in equity funds", "Only when markets are crashing"],
            "correct": 1
        }
    },
    {
        "id": "topic-6",
        "title": "What is FOMO in Investing?",
        "title_hi": "निवेश में FOMO क्या है?",
        "title_mr": "गुंतवणुकीतील FOMO म्हणजे काय?",
        "category": "Psychology",
        "simple_explanation": "FOMO stands for Fear Of Missing Out. It is the emotional panic that others are getting rich quickly while you are left behind.",
        "simple_explanation_hi": "FOMO मतलब 'मौका छूट जाने का डर'। जब लोग दूसरों को देख कर हड़बड़ी में बिना सोचे-समझे पैसे लगा देते हैं।",
        "simple_explanation_mr": "FOMO म्हणजे 'संधी गमावण्याची भीती'. दुसऱ्यांना भरपूर नफा होताना पाहून घाईघाईत चुकीचा निर्णय घेणे.",
        "everyday_analogy": "Rushing into a crowded shop just because a crowd gathered, only to find overpriced goods.",
        "everyday_analogy_hi": "भीड़ देखकर बिना जरूरत के किसी दुकान में घुस जाना और नुकसान उठाना।",
        "everyday_analogy_mr": "गर्दी पाहून नक्की काय आहे हे न पाहता दुकानात धाव घेण्यासारखे.",
        "example": "Scammers post fake screenshots of huge profits shouting 'Last 5 slots! Join now!' to trigger your FOMO.",
        "remember_this": "Whenever you feel a sudden emotional urge to invest immediately, PAUSE. Urgency is the scammer's best tool.",
        "common_misconception": "Misconception: 'If I don't invest today, my chance of wealth is gone forever.' Reality: Good investment opportunities exist every single month.",
        "quiz": {
            "question": "How do financial fraudsters exploit FOMO?",
            "options": ["By publishing audited financial accounts", "By manufacturing artificial urgency like 'today only' or 'limited slots'", "By offering low interest savings accounts", "By asking you to speak with your family"],
            "correct": 1
        }
    },
    {
        "id": "topic-7",
        "title": "How to Identify Guaranteed Return Scams",
        "title_hi": "गारंटीड रिटर्न स्कैम की पहचान कैसे करें?",
        "title_mr": "नक्की परतावा देणारे घोटाळे कसे ओळखावे?",
        "category": "Scam Prevention",
        "simple_explanation": "In genuine financial markets, risk and return are inseparable. Anyone promising guaranteed 20%, 50%, or 100% returns in days is operating an illegal scam.",
        "simple_explanation_hi": "शेयर बाजार में कभी कोई निश्चित रिटर्न नहीं हो सकता। 10 दिन या महीने में पैसे डबल या फिक्स रिटर्न का वादा 100% फर्जीवाड़ा है।",
        "simple_explanation_mr": "बाजारात परताव्याची कोणतीही खात्री देता येत नाही. 'पैसे दुप्पट' किंवा 'नक्की परतावा' सांगणारे सर्व संदेश फसवे असतात.",
        "everyday_analogy": "A vendor claiming they will give you pure 24-carat gold at the price of iron.",
        "everyday_analogy_hi": "कोई कहे कि वह लोहे के दाम पर असली सोना बेच रहा है।",
        "everyday_analogy_mr": "लोखंडाच्या भावात अस्सल २४ कॅरेट सोने देतो म्हणण्यासारखे हे अशक्य आहे.",
        "example": "WhatsApp message: 'Deposit ₹5,000, receive ₹25,000 in your bank account in 24 hours guaranteed.'",
        "remember_this": "SEBI strictly bars any market intermediary from offering guaranteed or assured returns.",
        "common_misconception": "Misconception: 'They showed a SEBI certificate photo, so it must be real.' Reality: Certificates sent on WhatsApp are easily forged with graphic apps.",
        "quiz": {
            "question": "Under SEBI regulations, can a registered entity promise guaranteed market returns?",
            "options": ["Yes, for VIP clients", "Strictly No, promising guaranteed market returns is prohibited by SEBI", "Yes, if on Telegram", "Yes, on festive days"],
            "correct": 1
        }
    },
    {
        "id": "topic-8",
        "title": "How Regulators are Impersonated",
        "title_hi": "नियामकों (SEBI / RBI) का फर्जीवाड़ा",
        "title_mr": "सेबी किंवा आरबीआयच्या नावाचा गैरवापर कसा होतो?",
        "category": "Scam Prevention",
        "simple_explanation": "Scammers steal official logos of SEBI, RBI, or Government of India to manufacture fake letters and trick citizens into trusting them.",
        "simple_explanation_hi": "धोखेबाज सेबी या आरबीआई के लोगो और नकली लेटरहेड का इस्तेमाल कर लोगों को विश्वास में लेते हैं।",
        "simple_explanation_mr": "गुन्हेगार सेबी आणि रिझर्व्ह बँकेचे खोटे शिक्के व लोगो वापरून लोकांची फसवणूक करतात.",
        "everyday_analogy": "Someone wearing a toy police badge and demanding money on the road.",
        "everyday_analogy_hi": "जैसे कोई नकली पुलिस की वर्दी पहनकर पैसे वसूली करने की कोशिश करे।",
        "everyday_analogy_mr": "एखाद्याने नकली पोलिसाचा गणवेश घालून तोतयागिरी करण्यासारखे आहे.",
        "example": "A PDF titled 'SEBI Wealth Growth Certificate 2025' asking for a ₹3,000 processing fee.",
        "remember_this": "SEBI and RBI NEVER collect money from retail investors, endorse trading tips, or operate investment schemes.",
        "common_misconception": "Misconception: 'The letterhead has the official emblem, so it must be official.' Reality: Anyone can copy and paste an emblem into a Word document.",
        "quiz": {
            "question": "Does SEBI ever run direct investment schemes or collect deposits from citizens?",
            "options": ["Yes, annually", "Never. SEBI is a regulator, not an investment fund or deposit taker", "Only for pensioners", "Yes, through WhatsApp"],
            "correct": 1
        }
    }
]

RESILIENCE_QUESTIONS = [
    {
        "id": 1,
        "scenario": "You receive a WhatsApp message from an unknown number: 'SEBI Approved scheme! Invest ₹10,000 and get ₹40,000 guaranteed in 15 days. Only 4 slots left today!'",
        "scenario_hi": "आपको किसी अनजान नंबर से व्हाट्सएप संदेश मिलता है: 'सेबी अप्रूव्ड स्कीम! ₹10,000 निवेश करें और 15 दिनों में ₹40,000 गारंटीड पाएं। आज केवल 4 सीटें बची हैं!'",
        "scenario_mr": "तुम्हाला अनोळखी नंबरवरून व्हॉट्सअ‍ॅप संदेश येतो: 'सेबी मान्यताप्राप्त योजना! ₹१०,००० गुंतवा आणि १५ दिवसांत ₹४०,००० नक्की मिळवा. आज फक्त ४ जागा शिल्लक!'",
        "question": "What is the safest and most appropriate action?",
        "question_hi": "सबसे सुरक्षित और उचित कदम क्या है?",
        "question_mr": "सर्वात सुरक्षित आणि योग्य कृती कोणती?",
        "options": {
            "A": "Transfer ₹10,000 immediately before the 4 slots expire.",
            "B": "Forward the message to your family and friends so they can benefit.",
            "C": "Recognize the red flags (guaranteed return, urgency, unverified SEBI claim) and do not send money.",
            "D": "Send a small trial amount of ₹1,000 to test if they return profits."
        },
        "options_hi": {
            "A": "सीटें खत्म होने से पहले तुरंत ₹10,000 भेज दें।",
            "B": "अपने परिवार और दोस्तों को यह मैसेज भेजें ताकि उन्हें भी फायदा हो।",
            "C": "धोखाधड़ी के संकेत (गारंटीड रिटर्न, जल्दबाजी, फर्जी सेबी दावा) पहचानें और पैसे न भेजें।",
            "D": "जांचने के लिए छोटा ट्रायल अमाउंट ₹1,000 भेजें।"
        },
        "options_mr": {
            "A": "जागा संपण्यापूर्वी त्वरित ₹१०,००० पाठवा.",
            "B": "कुटुंबीय आणि मित्रांना फायदा व्हावा म्हणून मेसेज फॉरवर्ड करा.",
            "C": "धोक्याचे संकेत (नक्की परतावा, घाईगडबड, खोटा सेबी दावा) ओळखा आणि पैसे पाठवू नका.",
            "D": "तपासण्यासाठी लहान रक्कम ₹१,००० पाठवून पहा."
        },
        "correct_option": "C",
        "concept_tested": "Guaranteed Return & Urgency Trap",
        "explanation": "Guaranteed returns and artificial slot urgency are classic indicators of financial fraud. Sending even a 'trial amount' is a known trap where scammers fake initial returns to lure larger sums.",
        "explanation_hi": "गारंटीड रिटर्न और सीमित सीटों की जल्दबाजी वित्तीय धोखाधड़ी के प्रमुख संकेत हैं। छोटा ट्रायल अमाउंट भेजना भी जालसाजी का हिस्सा होता है।",
        "explanation_mr": "नक्की परतावा आणि वेळेचा दबाव ही आर्थिक फसवणुकीची मुख्य लक्षणे आहेत. ट्रायल म्हणून लहान रक्कम पाठवणे हाही फसवेगिरीचाच सापळा असतो."
    },
    {
        "id": 2,
        "scenario": "A member in a Telegram stock tips group claims to have 'insider information' about a penny stock that will surge 500% tomorrow at 9:15 AM.",
        "scenario_hi": "टेलीग्राम स्टॉक टिप्स ग्रुप का एक सदस्य दावा करता है कि उसके पास एक पेनी स्टॉक की 'गुप्त इनसाइडर जानकारी' है जो कल सुबह 9:15 बजे 500% उछलेगा।",
        "scenario_mr": "टेलिग्राम ग्रुपमधील एक व्यक्ती दावा करते की तिच्याकडे पेनी स्टॉकची 'गुप्त इनसाइडर माहिती' आहे जो उद्या सकाळी ९:१५ वाजता ५००% वाढेल.",
        "question": "What is the primary risk here?",
        "question_hi": "यहाँ मुख्य जोखिम क्या है?",
        "question_mr": "यामध्ये मुख्य धोका कोणता आहे?",
        "options": {
            "A": "You might become a millionaire too quickly.",
            "B": "It is likely an illegal 'Pump and Dump' scheme where operators inflate prices and dump shares on retail investors.",
            "C": "The stock exchange will reward you for following tips.",
            "D": "There is zero risk if you exit within 5 minutes."
        },
        "options_hi": {
            "A": "आप बहुत जल्दी करोड़पति बन सकते हैं।",
            "B": "यह अवैध 'पंप एंड डंप' हो सकता है जहां ऑपरेटर भाव बढ़ाकर छोटे निवेशकों को फंसा देते हैं।",
            "C": "स्टॉक एक्सचेंज आपको टिप मानने के लिए इनाम देगा।",
            "D": "अगर आप 5 मिनट में निकल जाते हैं तो कोई जोखिम नहीं है।"
        },
        "options_mr": {
            "A": "तुम्ही खूप लवकर करोडपती होऊ शकता.",
            "B": "ही बेकायदेशीर 'पंप आणि डंप' क्लृप्ती असू शकते, ज्यात भाव फुगवून सामान्य गुंतवणूकदारांना अडकवले जाते.",
            "C": "स्टॉक एक्सचेंज तुम्हाला टिप पाळल्याबद्दल बक्षीस देईल.",
            "D": "५ मिनिटांत बाहेर पडल्यास कोणताही धोका नाही."
        },
        "correct_option": "B",
        "concept_tested": "Market Manipulation & Social Media Tips",
        "explanation": "Unregulated social media groups frequently conduct 'Pump and Dump' manipulations. Retail investors buy at inflated prices and are left with illiquid, worthless shares when organizers exit.",
        "explanation_hi": "असुरक्षित सोशल मीडिया ग्रुप्स अक्सर 'पंप एंड डंप' हेरफेर करते हैं। छोटे निवेशक महंगे भाव पर खरीद लेते हैं और बाद में घाटा उठाते हैं।",
        "explanation_mr": "असुरक्षित ग्रुप्स 'पंप आणि डंप' हेराफेरी करतात. सामान्य गुंतवणूकदार चढ्या भावात खरेदी करतात आणि नंतर अडकून पडतात."
    },
    {
        "id": 3,
        "scenario": "A caller claiming to be from your broker's technical support desk says your Demat account will be frozen within 1 hour unless you share the OTP sent to your phone.",
        "scenario_hi": "एक कॉलर ब्रोकर का प्रतिनिधि बनकर कहता है कि आपका डीमैट खाता 1 घंटे में फ्रीज हो जाएगा यदि आपने मोबाइल पर आया ओटीपी साझा नहीं किया।",
        "scenario_mr": "तुमच्या ब्रोकरकडून बोलत असल्याचे भासवून एक व्यक्ती सांगते की १ तासात डिमॅट खाते बंद होईल, जर तुम्ही ओटीपी शेअर केला नाही.",
        "question": "How should you respond?",
        "question_hi": "आपको क्या प्रतिक्रिया देनी चाहिए?",
        "question_mr": "तुम्ही कशी प्रतिक्रिया द्यावी?",
        "options": {
            "A": "Share the OTP immediately so your Demat account remains active.",
            "B": "Never share your OTP with anyone. Hang up and contact your broker through their verified official app or website.",
            "C": "Tell them half of the OTP digits first.",
            "D": "Share your UPI PIN instead of the OTP."
        },
        "options_hi": {
            "A": "तुरंत ओटीपी साझा करें ताकि खाता सक्रिय रहे।",
            "B": "कभी भी किसी को ओटीपी न बताएं। फोन काटें और आधिकारिक ऐप या वेबसाइट से ब्रोकर से संपर्क करें।",
            "C": "पहले ओटीपी के आधे अंक बताएं।",
            "D": "ओटीपी के बजाय यूपीआई पिन साझा करें।"
        },
        "options_mr": {
            "A": "खाते सुरू राहण्यासाठी त्वरित ओटीपी द्या.",
            "B": "कधीही कोणालाही ओटीपी सांगू नका. फोन कट करा आणि ब्रोकरच्या अधिकृत अ‍ॅपवरून खात्री करा.",
            "C": "सुरुवातीला ओटीपीचे अर्धे आकडे सांगा.",
            "D": "ओटीपीऐवजी यूपीआय पिन द्या."
        },
        "correct_option": "B",
        "concept_tested": "Credential Protection & Impersonation",
        "explanation": "Legitimate brokers, banks, and regulators never ask for your OTP, password, or PIN. Creating panic about account closure is a standard social engineering tactic.",
        "explanation_hi": "वैध ब्रोकर या बैंक कभी भी ओटीपी, पासवर्ड या पिन नहीं मांगते। खाते बंद होने का डर दिखाकर कोड मांगना ठगी का तरीका है।",
        "explanation_mr": "अधिकृत बँका किंवा ब्रोकर्स कधीही ओटीपी, पासवर्ड किंवा पिन मागत नाहीत. भीती दाखवून फसवण्याचा हा नेहमीचा प्रकार आहे."
    },
    {
        "id": 4,
        "scenario": "You see a link on social media: 'http://rbi-subsidy-wealth.click/apply'. It asks you to enter your bank account number and UPI PIN to claim a government bonus.",
        "scenario_hi": "आप सोशल मीडिया पर एक लिंक देखते हैं: 'http://rbi-subsidy-wealth.click/apply'। यह सरकारी बोनस के लिए बैंक खाता और यूपीआई पिन दर्ज करने को कहता है।",
        "scenario_mr": "सोशल मीडियावर लिंक दिसते: 'http://rbi-subsidy-wealth.click/apply'. सरकारी अनुदान मिळवण्यासाठी बँक खाते आणि यूपीआय पिन मागितला जातो.",
        "question": "What indicates this link is hazardous?",
        "question_hi": "इस लिंक में क्या खतरनाक है?",
        "question_mr": "या लिंकमध्ये कोणता धोका स्पष्ट दिसतो?",
        "options": {
            "A": "It lacks HTTPS, uses a suspicious .click domain, and asks for a UPI PIN (which is ONLY used to send money, never receive it).",
            "B": "It has the letters RBI in it, so it is 100% genuine.",
            "C": "All government websites use .click domain names.",
            "D": "Entering a UPI PIN is required to receive money."
        },
        "options_hi": {
            "A": "इसमें HTTPS नहीं है, संदिग्ध .click डोमेन है, और यूपीआई पिन मांगा जा रहा है (पिन सिर्फ पैसे भेजने के लिए होता है, पाने के लिए नहीं)।",
            "B": "इसमें RBI लिखा है, इसलिए यह 100% असली है।",
            "C": "सभी सरकारी वेबसाइट्स .click का इस्तेमाल करती हैं।",
            "D": "पैसे पाने के लिए यूपीआई पिन डालना अनिवार्य है।"
        },
        "options_mr": {
            "A": "यात HTTPS नाही, संशयास्पद .click डोमेन आहे आणि यूपीआय पिन मागितला आहे (पिन फक्त पैसे पाठवण्यासाठी असतो, स्वीकारण्यासाठी नाही).",
            "B": "यात RBI शब्द आहे, म्हणून हे १००% खरे आहे.",
            "C": "सर्व सरकारी संकेतस्थळे .click डोमेन वापरतात.",
            "D": "पैसे मिळवण्यासाठी यूपीआय पिन टाकणे आवश्यक असते."
        },
        "correct_option": "A",
        "concept_tested": "URL Safety & UPI Mechanics",
        "explanation": "A UPI PIN is used strictly to authorize outgoing payments, never to receive money. Official RBI websites use rbi.org.in, not obscure third-party domains.",
        "explanation_hi": "यूपीआई पिन का उपयोग केवल पैसे भेजने के लिए होता है, प्राप्त करने के लिए कभी नहीं। आरबीआई की आधिकारिक वेबसाइट rbi.org.in है।",
        "explanation_mr": "यूपीआय पिन फक्त पैसे पाठवण्यासाठी वापरला जातो, पैसे खात्यात येण्यासाठी पिनची गरज नसते. आरबीआयचे खरे संकेतस्थळ rbi.org.in आहे."
    },
    {
        "id": 5,
        "scenario": "An influencer on Instagram displays luxury cars and claims their proprietary algorithm makes 5% profit daily without any loss.",
        "scenario_hi": "इंस्टाग्राम पर एक इन्फ्लुएंसर लग्जरी कारों का प्रदर्शन करता है और दावा करता है कि उसका सीक्रेट एल्गोरिदम बिना नुकसान के रोज 5% मुनाफा देता है।",
        "scenario_mr": "इन्स्टाग्रामवरील एक व्यक्ती महागड्या गाड्या दाखवून दावा करते की तिचा खास फॉर्म्युला दररोज ५% खात्रीशीर नफा देतो.",
        "question": "What should an investor keep in mind?",
        "question_hi": "निवेशक को क्या ध्यान में रखना चाहिए?",
        "question_mr": "गुंतवणूकदाराने कोणती गोष्ट लक्षात ठेवली पाहिजे?",
        "options": {
            "A": "Rented luxury items and lifestyle displays are common marketing tactics used to sell unverified courses or tips.",
            "B": "5% daily return compounded over a year is mathematically impossible in real financial markets.",
            "C": "Past performance screenshots can be easily faked with demo accounts or inspect-element tools.",
            "D": "All of the above."
        },
        "options_hi": {
            "A": "किराए की लग्जरी कारें और दिखावा अक्सर अप्रमाणित कोर्स या टिप्स बेचने का हथकंडा होता है।",
            "B": "रोज 5% मुनाफा वास्तविक वित्तीय बाजार में गणितीय रूप से असंभव है।",
            "C": "मुनाफे के स्क्रीनशॉट डेमो अकाउंट या एडिटिंग से आसानी से नकली बनाए जा सकते हैं।",
            "D": "उपरोक्त सभी।"
        },
        "options_mr": {
            "A": "भाड्याने घेतलेल्या अलिशान वस्तू दाखवून अपूर्ण माहिती असलेले कोर्सेस किंवा टिप्स विकल्या जातात.",
            "B": "दररोज ५% नफा मिळणे हे बाजारात गणिताच्या दृष्टीने अशक्य आहे.",
            "C": "नफ्याचे स्क्रीनशॉट सहजपणे बनावट तयार केले जाऊ शकतात.",
            "D": "वरील सर्व बाबी."
        },
        "correct_option": "D",
        "concept_tested": "Finfluencer Scrutiny & Return Realism",
        "explanation": "A 5% daily return would turn ₹10,000 into hundreds of crores in a single year, which is mathematically absurd. Lifestyle displays and screenshots are frequently manufactured to create false credibility.",
        "explanation_hi": "रोज 5% रिटर्न से ₹10,000 एक साल में सैकड़ों करोड़ बन जाएंगे, जो पूरी तरह असंभव है। स्क्रीनशॉट अक्सर नकली होते हैं।",
        "explanation_mr": "दररोज ५% परतावा म्हणजे वर्षात १० हजार रुपयांचे शेकडो कोटी रुपये होतील, जे अशक्य आहे. असे स्क्रीनशॉट बनावट असतात."
    },
    {
        "id": 6,
        "scenario": "Someone asks you to transfer investment funds into a personal savings account in an individual's name rather than a SEBI-registered broker's clearing account.",
        "scenario_hi": "कोई व्यक्ति सेबी-रजिस्टर्ड ब्रोकर के आधिकारिक खाते के बजाय किसी निजी व्यक्ति के बचत खाते में निवेश राशि ट्रांसफर करने को कहता है।",
        "scenario_mr": "एखादी व्यक्ती सेबी-नोंदणीकृत ब्रोकरच्या खात्याऐवजी स्वतःच्या वैयक्तिक बचत खात्यात गुंतवणुकीचे पैसे पाठवण्यास सांगते.",
        "question": "What does this signify?",
        "question_hi": "यह क्या दर्शाता है?",
        "question_mr": "याचा नक्की काय अर्थ होतो?",
        "options": {
            "A": "It is a standard convenience feature in modern banking.",
            "B": "Major warning sign: Legitimate investments never route client money into personal individual bank accounts.",
            "C": "It helps you avoid broker commissions.",
            "D": "It means the government will directly insure your capital."
        },
        "options_hi": {
            "A": "यह आधुनिक बैंकिंग की एक सामान्य सुविधा है।",
            "B": "गंभीर चेतावनी: वैध निवेश कभी भी किसी निजी व्यक्ति के व्यक्तिगत बैंक खाते में नहीं मंगाए जाते।",
            "C": "इससे ब्रोकरेज कमीशन की बचत होती है।",
            "D": "इसका मतलब है कि सरकार आपके पैसे का बीमा करेगी।"
        },
        "options_mr": {
            "A": "ही आधुनिक बँकिंगची सोपी पद्धत आहे.",
            "B": "मोठा धोक्याचा इशारा: कायदेशीर गुंतवणुकीचे पैसे कधीही कोणाच्याही खाजगी खात्यात मागितले जात नाहीत.",
            "C": "यामुळे ब्रोकरेज वाचते.",
            "D": "याचा अर्थ सरकार पैशांची हमी घेते."
        },
        "correct_option": "B",
        "concept_tested": "Segregation of Client Funds",
        "explanation": "SEBI rules strictly mandate that investment funds must only be deposited into designated client bank accounts of registered intermediaries, never personal savings accounts.",
        "explanation_hi": "सेबी नियमों के अनुसार निवेश का पैसा केवल पंजीकृत संस्था के आधिकारिक बैंक खाते में ही जमा होना चाहिए, किसी व्यक्ति के निजी खाते में नहीं।",
        "explanation_mr": "सेबीच्या नियमांनुसार गुंतवणुकीचे पैसे फक्त नोंदणीकृत संस्थेच्या अधिकृत खात्यातच जमा केले पाहिजेत, वैयक्तिक खात्यात नाही."
    },
    {
        "id": 7,
        "scenario": "You receive a message about a friend investing in a scheme that doubled their money in one week, and they urge you to put your retirement savings into it.",
        "scenario_hi": "आपको खबर मिलती है कि एक दोस्त ने एक हफ्ते में पैसे डबल कर लिए हैं, और वह आपको अपनी रिटायरमेंट की बचत उस स्कीम में लगाने की सलाह देता है।",
        "scenario_mr": "तुमच्या मित्राचे पैसे एका आठवड्यात दुप्पट झाल्याचे समजते आणि तो तुम्हाला निवृत्तीची सर्व पुंजी त्यात गुंतवण्याचा आग्रह करतो.",
        "question": "What is the best psychological approach?",
        "question_hi": "सबसे उचित मानसिक दृष्टिकोण क्या है?",
        "question_mr": "अशा वेळी सर्वात योग्य दृष्टिकोन कोणता?",
        "options": {
            "A": "Invest everything immediately because a trusted friend recommended it.",
            "B": "Apply a 'Decision Pause': Acknowledge the emotional excitement, recognize Ponzi schemes pay early members to recruit others, and verify independently.",
            "C": "Borrow money to invest twice as much.",
            "D": "Assume your friend has conducted a complete forensic regulatory audit."
        },
        "options_hi": {
            "A": "तुरंत सारा पैसा लगा दें क्योंकि भरोसेमंद दोस्त ने कहा है।",
            "B": "'डिसीजन पॉज' लें: लालच और जल्दबाजी पर रोक लगाएं, समझें कि पोंजी स्कीम शुरुआती लोगों को पैसे देकर दूसरों को फंसाती हैं, और स्वतंत्र जांच करें।",
            "C": "कर्ज लेकर दोगुना पैसा लगा दें।",
            "D": "मान लें कि दोस्त ने पूरी कानूनी जांच कर ली होगी।"
        },
        "options_mr": {
            "A": "जवळच्या मित्राने सांगितल्यामुळे त्वरित सर्व पैसे गुंतवा.",
            "B": "'डिसीजन पॉज' घ्या: तात्पुरत्या मोहाला बळी न पडता थांबा, पॉन्झी योजना सुरुवातीला परतावा देऊन इतरांना अडकवतात हे समजून घ्या आणि खात्री करा.",
            "C": "कर्ज काढून दुप्पट रक्कम गुंतवा.",
            "D": "मित्राने सर्व कायदेशीर खात्री केली असेल असे गृहीत धरा."
        },
        "correct_option": "B",
        "concept_tested": "Decision Pause & Ponzi Awareness",
        "explanation": "Ponzi schemes frequently use early payouts to friends and relatives to turn them into unwitting recruiters. Taking a deliberate decision pause prevents impulsive financial damage.",
        "explanation_hi": "पोंजी स्कीम्स अक्सर शुरुआती लोगों को मुनाफा देकर दूसरों को फंसाने के लिए तैयार करती हैं। 'सोच-समझकर रुकना' नुकसान से बचाता है।",
        "explanation_mr": "पॉन्झी योजनांमध्ये सुरुवातीच्या लोकांना पैसे देऊन इतरांना आकर्षित केले जाते. विचार करण्यासाठी थांबणे हाच बचावाचा उत्तम मार्ग आहे."
    },
    {
        "id": 8,
        "scenario": "Where can a retail investor in India independently verify whether a stock broker or investment advisor is legally registered?",
        "scenario_hi": "भारत में कोई सामान्य निवेशक स्वतंत्र रूप से यह कैसे जांच सकता है कि कोई स्टॉक ब्रोकर या सलाहकार कानूनी रूप से सेबी में पंजीकृत है या नहीं?",
        "scenario_mr": "भारतातील सामान्य गुंतवणूकदार ब्रोकर किंवा सल्लागार कायदेशीर नोंदणीकृत आहे की नाही हे स्वतः कोठे तपासू शकतो?",
        "question": "Which official source should you check?",
        "question_hi": "आपको किस आधिकारिक स्रोत की जांच करनी चाहिए?",
        "question_mr": "कोणत्या अधिकृत संकेतस्थळावर तपासणी करावी?",
        "options": {
            "A": "Search Telegram for the advisor's username.",
            "B": "Visit the official SEBI portal (sebi.gov.in) -> 'Recognised Intermediaries' database.",
            "C": "Check how many Instagram followers the person has.",
            "D": "Read WhatsApp forwards sent by community members."
        },
        "options_hi": {
            "A": "टेलीग्राम पर सलाहकार का नाम खोजें।",
            "B": "सेबी की आधिकारिक वेबसाइट (sebi.gov.in) पर 'Recognised Intermediaries' डेटाबेस देखें।",
            "C": "देखें कि उस व्यक्ति के इंस्टाग्राम पर कितने फॉलोअर्स हैं।",
            "D": "व्हाट्सएप ग्रुप्स में भेजे गए मैसेज पढ़ें।"
        },
        "options_mr": {
            "A": "टेलिग्रामवर त्या व्यक्तीचे नाव शोधा.",
            "B": "सेबीच्या अधिकृत पोर्टलवर (sebi.gov.in) 'Recognised Intermediaries' यादी तपासा.",
            "C": "त्या व्यक्तीचे इन्स्टाग्रामवर किती फॉलोअर्स आहेत ते पहा.",
            "D": "व्हॉट्सअ‍ॅपवरील मेसेज वाचा."
        },
        "correct_option": "B",
        "concept_tested": "Official Regulatory Verification",
        "explanation": "The official SEBI directory at sebi.gov.in provides the legal registration number, validity, and contact details of all genuine registered stock brokers, research analysts, and investment advisors.",
        "explanation_hi": "सेबी की आधिकारिक वेबसाइट sebi.gov.in पर सभी वैध ब्रोकर्स और सलाहकारों का 12 अंकों का रजिस्ट्रेशन नंबर और संपर्क विवरण उपलब्ध होता है।",
        "explanation_mr": "सेबीच्या अधिकृत sebi.gov.in संकेतस्थळावर सर्व कायदेशीर ब्रोकर्स आणि सल्लागारांची अधिकृत माहिती उपलब्ध असते."
    }
]
