import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "demo_screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_chat_screenshot(filename, header_title, sender_phone, message_lines, bubble_color, is_urgent=True):
    width, height = 600, 420
    img = Image.new("RGB", (width, height), color=(18, 27, 34))  # WhatsApp dark theme background
    draw = ImageDraw.Draw(img)

    # WhatsApp Top Bar
    draw.rectangle([(0, 0), (width, 65)], fill=(31, 44, 52))
    draw.ellipse([(15, 12), (55, 52)], fill=(0, 168, 132))  # Profile circle
    draw.text((26, 20), "VIP", fill=(255, 255, 255))
    draw.text((70, 16), header_title, fill=(233, 237, 239))
    draw.text((70, 38), sender_phone, fill=(134, 150, 160))

    # Date badge
    draw.rounded_rectangle([(240, 80), (360, 105)], radius=6, fill=(24, 34, 41))
    draw.text((275, 85), "TODAY", fill=(134, 150, 160))

    # Urgent banner if applicable
    start_y = 125
    if is_urgent:
        draw.rounded_rectangle([(30, 120), (570, 155)], radius=8, fill=(120, 20, 20))
        draw.text((45, 128), "⚠️ HIGH RETURN ALERT - LIMITED TIME OFFER ⚠️", fill=(255, 230, 230))
        start_y = 170

    # Chat Bubble
    draw.rounded_rectangle([(30, start_y), (570, start_y + 190)], radius=12, fill=bubble_color)

    y_offset = start_y + 15
    for line in message_lines:
        draw.text((45, y_offset), line, fill=(240, 245, 248))
        y_offset += 24

    # Timestamp and double tick
    draw.text((480, start_y + 165), "10:45 AM  ✓✓", fill=(110, 180, 240))

    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Generated demo screenshot: {out_path}")

# 1. WhatsApp Scam (English)
create_chat_screenshot(
    "whatsapp_scam.png",
    "VIP Wealth Multiplication Group",
    "+91 98234 56789 • 2,450 members",
    [
        "URGENT! SEBI APPROVED OPPORTUNITY.",
        "Invest Rs 10,000 today and get Rs 50,000 guaranteed",
        "within 30 days! No risk, 100% fixed profit.",
        "Only 5 slots left! Send money immediately via UPI",
        "to secure your spot.",
        "Join our VIP Telegram group: https://t.me/vip_invest_sure"
    ],
    (5, 94, 82),
    is_urgent=True
)

# 2. Marathi Scam
create_chat_screenshot(
    "marathi_scam.png",
    "खात्रीशीर परतावा ग्रुप (SEBI Approved)",
    "+91 94220 12345 • महाराष्ट्र",
    [
        "नमस्कार! सेबी मान्यताप्राप्त खात्रीशीर योजना!",
        "फक्त रु. ५,००० गुंतवा आणि दरमहा रु. २५,००० नक्की परतावा मिळवा.",
        "कोणतेही नुकसान नाही, १००% गॅरंटीड नफा.",
        "शेवटची संधी! त्वरित पैसे पाठवा आणि व्हीआयपी ग्रुप जॉईन करा.",
        "संपर्क: @nivesh_guru_telegram"
    ],
    (15, 80, 60),
    is_urgent=True
)

# 3. Hindi Scam
create_chat_screenshot(
    "hindi_scam.png",
    "दैनिक मुनाफा सेवा (SEBI Certified)",
    "+91 88776 54321 • उत्तर प्रदेश",
    [
        "अंतिम अवसर! सेबी अप्रूव्ड स्कीम।",
        "रु. 10,000 निवेश करें और 30 दिनों में रु. 1,00,000 पाएं।",
        "100% गारंटीड रिटर्न। बिना किसी जोखिम के।",
        "तुरंत दिए गए UPI पर पेमेंट करें और टेलीग्राम ग्रुप से जुड़ें।",
        "सीमित सीटें शेष हैं।"
    ],
    (20, 65, 85),
    is_urgent=True
)

# 4. Fake Authority / Impersonation
create_chat_screenshot(
    "authority_fake.png",
    "National Wealth Scheme Officer (RBI/SEBI)",
    "official-regulator-notice@gov.in (Unverified)",
    [
        "Official Notification: RBI & SEBI Joint Scheme 2025.",
        "Pay mandatory registration fee Rs 2,500 to authorized",
        "executive personal UPI account.",
        "Send your OTP and Aadhaar card photo to claim guaranteed",
        "Rs 1,00,000 subsidy grant immediately."
    ],
    (40, 45, 60),
    is_urgent=True
)

# 5. Genuine Educational Notice
create_chat_screenshot(
    "educational.png",
    "Investor Awareness & Education Forum",
    "Verified Education Channel",
    [
        "Investor Awareness Notice:",
        "Asset allocation and diversification help manage portfolio",
        "risk over the long term. Market securities are subject to",
        "market volatility. Mutual fund NAV fluctuates daily.",
        "Always read scheme documents carefully before investing."
    ],
    (30, 50, 70),
    is_urgent=False
)

print("All 5 realistic demo screenshots generated successfully!")
