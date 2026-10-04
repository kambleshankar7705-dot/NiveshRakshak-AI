# NiveshRakshak AI (निवेशरक्षक AI)
> *"Verify Before You Invest."*

**NiveshRakshak AI** is an AI-powered investor protection and financial misinformation detection platform built for the **SANGYAN Investor Resilience Hackathon**.

The platform safeguards Indian retail investors—particularly first-time market participants, Tier-2/Tier-3 city residents, and senior citizens—from fraudulent investment schemes, unrealistic profit promises, artificial urgency, and impersonation scams on WhatsApp, Telegram, and social media.

---

## Key Features

1. **Screenshot Analyzer (Core Feature)**: Upload or drag-and-drop screenshots of WhatsApp forwards, Telegram messages, or SMS alerts. Optical Character Recognition (OCR) extracts text, lets users review or edit it, and performs a 5-stage explainable risk assessment.
2. **Deterministic & Explainable Risk Scoring Engine**: Calculates risk from 0 to 100 with weighted signals (Guaranteed returns: +20, Unrealistic profit: +15, Urgency/FOMO: +10, Fake regulatory claims: +15, Unusual payment requests: +10, Credential requests: +20).
3. **Multilingual Support (English, Hindi, Marathi)**: Explanations, alerts, and navigation in English, हिंदी, and मराठी with instant dynamic switching and localized audio synthesis (TTS).
4. **Voice-First Assistant**: Real-time microphone capture in Marathi (`mr-IN`), Hindi (`hi-IN`), and English (`en-IN`) with concise, spoken answers.
5. **URL Safety Checker**: Evaluates HTTPS security, domain structure, disposable TLDs (`.xyz`, `.top`, etc.), URL shorteners, and fake regulator domains (`sebi`, `rbi`).
6. **Regulatory Claim Evidence Checker**: Validates claims like *"SEBI Approved"* against regulatory standards and provides step-by-step official verification instructions.
7. **Promotion vs. Education Classifier**: Differentiates between genuine investor education and high-risk promotional funnels on YouTube, Instagram, and Telegram.
8. **Behavioral Decision Pause ("Cooling-Off Period")**: Triggers an interactive reflection modal when high urgency or psychological pressure is detected.
9. **Financial Concept Explainer (12 Topics)**: Everyday Indian analogies and mini-quizzes explaining risk, volatility, diversification, compounding, NAV, FOMO, and scam mechanics.
10. **Educational Consequence Simulator**: Demonstrates two-way market risk (+10%/-10%, +25%/-25%, +50%/-50%) on a hypothetical ₹10,000 without offering real trading or stock advice.
11. **Investor Resilience Quiz**: 8 scenario-based questions assessing vulnerability against real-world Indian scams with immediate diagnostic scoring.
12. **Senior Citizen / Simple Mode**: One-touch toggle for high-contrast, extra-large typography and simplified 4-card navigation.
13. **Privacy Center & Data Sovereignty**: Guarantees zero collection of OTPs, passwords, or banking logins, with a 1-click history purge tool.
14. **Judge Demo Mode**: 5 preloaded scenarios for rapid 1-click evaluation.
15. **Aggregated Security Analytics**: Real-time visibility into intercepted risk levels, common red flags, and input channel distribution.

---

## Strict Guardrails & Public Good Mandate

- **NOT a trading or stock-tipping app**: Strictly does not recommend stocks, predict prices, or give buy/sell/hold calls.
- **NOT an investment advisor**: Does not generate personalized financial plans or recommend mutual funds.
- **Zero credential collection**: Strictly prohibits requesting OTPs, passwords, PINs, or bank account balances.
- **No commercial bias**: No broker promotions, referral commissions, or subscription funnels.

---

## Technology Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Lucide Icons, Web Speech API.
- **Backend**: Python 3.13, FastAPI, Uvicorn, Pydantic v2, HTTPX, Pillow, SQLite.
- **AI & Rule Engine**: Hybrid architecture with Gemini/OpenAI API integration and an automated deterministic rule-based fallback engine.
- **Database**: Local SQLite database with automated schema migration.

---

## Project Structure

```text
Sangyan Hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI REST API & routes
│   │   ├── models/schemas.py         # Pydantic v2 schemas
│   │   ├── services/
│   │   │   ├── rule_engine.py        # Weighted red flag scoring & multilingual explanations
│   │   │   ├── ai_engine.py          # LLM integration with graceful rule fallback
│   │   │   ├── ocr_engine.py         # OCR image text extraction
│   │   │   ├── url_engine.py         # URL security & domain inspection
│   │   │   ├── classifier_engine.py  # Intent classifier (Educational vs Promo)
│   │   │   └── database.py           # SQLite connection & history queries
│   │   └── data/seeds.py             # Pre-seeded topics, quizzes, and demo cases
│   ├── generate_demo_images.py       # Generates sample screenshot PNGs
│   ├── test_backend.py               # Complete test suite for all endpoints
│   └── requirements.txt              # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/                      # Next.js App Router pages
│   │   │   ├── page.tsx              # Landing page
│   │   │   ├── dashboard/page.tsx    # Safety command center
│   │   │   ├── analyze/screenshot/   # Core Screenshot Analyzer
│   │   │   ├── analyze/text/         # Text & message checker
│   │   │   ├── check-url/            # URL safety checker
│   │   │   ├── verify-claim/         # Claim evidence validator
│   │   │   ├── content-checker/      # Promotion vs Education classifier
│   │   │   ├── voice/                # Regional voice assistant
│   │   │   ├── learn/                # 12 financial concept explainers
│   │   │   ├── simulator/            # Educational risk simulator
│   │   │   ├── resilience-test/      # Investor resilience quiz
│   │   │   ├── history/              # Analysis audit log
│   │   │   ├── privacy/              # Privacy & safety center
│   │   │   ├── demo/                 # Judge demonstration showcase
│   │   │   ├── analytics/            # Threat trend analytics
│   │   │   └── about/                # Mission & guardrails
│   │   ├── components/               # Navbar, Footer, RiskMeter, RedFlagCard, etc.
│   │   ├── context/AppContext.tsx    # i18n & Simple Mode state
│   │   ├── locales/                  # en.json, hi.json, mr.json
│   │   └── lib/api.ts                # Backend API client
│   └── public/demo_screenshots/      # Sample PNG screenshots
├── .env.example                      # Environment variables template
└── README.md
```

---

## Quick Start & Installation

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Node.js 18+** (Tested on Node v24)
- **npm** (Tested on npm 11)

### 2. Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
python test_backend.py  # Run the full test suite
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Backend runs on `http://localhost:8000` (API documentation at `http://localhost:8000/docs`).

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run build
npm run start -- -p 3000
```
Frontend runs on `http://localhost:3000`.

---

## Environment Variables (`.env`)

Copy `.env.example` to `.env`:
```ini
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional: Set your Gemini or OpenAI API Key
# If left empty, the deterministic Rule-Based Red Flag Engine executes automatically
AI_API_KEY=
AI_PROVIDER=gemini

# Database & CORS
DATABASE_URL=sqlite:///./niveshrakshak.db
FRONTEND_URL=http://localhost:3000
```

---

## 3-Minute Hackathon Demo Script

1. **Open Application**: Navigate to `http://localhost:3000`. Toggle language between **English**, **हिंदी**, and **मराठी**.
2. **Senior Mode**: Click **"Senior / Simple Mode"** in the top navigation to view the high-contrast interface designed for elderly users.
3. **Screenshot Analyzer**: Navigate to `/analyze/screenshot`.
   - Click the preset: **"Guaranteed Return WhatsApp Forward"** (or upload any screenshot).
   - Observe the OCR extraction and review the message in the editable text area.
   - Click **"STEP 2: Analyze Risk"** and observe the 5-stage progress animation.
   - View the **Risk Meter (HIGH RISK)**, detected red flags with quotes, and plain-language explanation.
   - Click **"Explain in Marathi"** to see the vernacular breakdown.
   - Click **"Why is this suspicious?"** for a breakdown of FOMO and regulatory red flags.
4. **Voice Assistant**: Navigate to `/voice`. Click the microphone and ask in Marathi: *"मला WhatsApp वर investment चा message आला आहे. तो safe आहे का?"* Listen to the voice summary.
5. **Resilience Test**: Navigate to `/resilience-test` and complete the 8-question scenario test to generate an **Investor Resilience Score**.
6. **Privacy Center**: Navigate to `/privacy` to inspect the zero-credential policy and click **"Delete My Analysis History"** to demonstrate complete user data sovereignty.

---

## Future Scope

- Direct live integration with the official SEBI SCORES API and RBI Intermediary directory.
- Integration with Government of India **Bhashini** APIs for speech recognition across 22 scheduled Indian languages.
- On-device local SLM (Small Language Model) inference for offline Tier-3 smartphone operation.
- Automated reporting integration with the National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in).
