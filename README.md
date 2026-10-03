# AI-Powered Customer Service Chatbot with Human Agent Handover

An enterprise-grade, real-time AI Customer Support system built with **Python 3.11+**, **Flask**, **SQLAlchemy ORM**, **Flask-SocketIO**, and a **hybrid scikit-learn NLP pipeline**.

The platform deflects routine queries using AI intent classification and semantic knowledge-base retrieval, monitors customer sentiment in real-time, and seamlessly transfers complex or frustrated inquiries to human customer service agents with zero data loss.

---

## 🚀 Key Highlights & Features

1. **Intelligent Conversational AI:**
   - Classifies customer messages across 11 core intents (`ORDER_TRACKING`, `RETURN`, `REFUND`, `ORDER_CANCELLATION`, `PAYMENT`, `DELIVERY`, `PRODUCT_INFORMATION`, `COMPLAINT`, `TECHNICAL_SUPPORT`, `HUMAN_AGENT`, `OTHER`).
   - Hybrid machine learning model combining **TF-IDF + calibrated Logistic Regression** with heuristic safeguards.
   - Dynamic Order ID extraction (e.g., `ORD1001`) and live order status lookups.

2. **Semantic Knowledge Base (FAQ) Retrieval:**
   - Database-backed FAQ search powered by TF-IDF cosine similarity.
   - Ready for plug-and-play `sentence-transformers` vector embeddings.

3. **Sentiment & Emotion Telemetry:**
   - Detects customer sentiment: `POSITIVE`, `NEUTRAL`, `NEGATIVE`, `ANGRY_FRUSTRATED`.
   - Real-time urgency escalation for angry or highly dissatisfied customers.

4. **Confidence Score & Routing Engine:**
   - Internal confidence score ($0.0$ to $1.0$) for every turn.
   - High Confidence ($\ge 0.70$): Direct AI answer.
   - Moderate Confidence ($0.45 - 0.69$): Contextual clarification question.
   - Low Confidence ($< 0.45$), repeated confusion, or explicit request: Handover to live agent queue.

5. **Human Agent Handover (Zero Waiting-Loss):**
   - Automated structured AI Handover Summary generation:
     ```text
     CUSTOMER: Rahul
     ISSUE: Order ORD1001 has not arrived.
     INTENT: Delivery
     SENTIMENT: Frustrated
     SUMMARY: Customer reports that order ORD1001 is delayed and wants an update.
     ```
   - Live handover transition: `AI` → `WAITING_FOR_AGENT` → `HUMAN_AGENT` → `RESOLVED`.
   - Instant system notification: *"Agent Priya Sharma has joined the conversation."*

6. **Agent & Admin Operations Hubs:**
   - **Agent Service Desk:** Live queue management, claim chats, real-time messaging, inter-agent transfer, and resolution.
   - **Executive Admin Dashboard:** Real-time deflection rate, CSAT ratings, Chart.js visualizations for intents and sentiments, and full Knowledge Base CRUD.

---

## 📐 Architecture & AI Pipeline

```text
Customer Message
       ↓
Preprocess & Entity Extraction (e.g. Order ID: ORD1001)
       ↓
Intent Classification (Hybrid ML + Rule Engine)
       ↓
Sentiment Analysis (Positive / Neutral / Negative / Angry)
       ↓
Knowledge Base Retrieval (Semantic Similarity)
       ↓
Confidence Evaluation & Threshold Gate
       ↓
Is Confidence Sufficient (>= 0.70)?
      /              \
    YES               NO
     ↓                 ↓
AI Direct Response  Clarification Question
                       ↓
                  Still Unresolved or Low Confidence?
                      /             \
                    NO               YES
                    ↓                 ↓
                AI Answer       Handover Triggered
                                      ↓
                                AI Summary Generated
                                      ↓
                                Agent Live Queue
                                      ↓
                             Agent Claims & Chats
                                      ↓
                                Resolution
```

---

## 📁 Project Structure

```text
customer-service-chatbot/
│
├── app.py                      # Flask app factory & SocketIO events
├── config.py                   # Environment configuration
├── extensions.py               # Shared extensions (SocketIO, LoginManager, AI bot)
├── requirements.txt            # Python dependencies
├── conftest.py                 # Pytest configuration
├── .env                        # Local environment variables
├── .env.example                # Example environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Comprehensive documentation
│
├── database/
│   ├── __init__.py
│   ├── database.py             # SQLAlchemy instance and init_db
│   └── seed.py                 # Seeds 10 customers, 5 agents, 20 orders, 30 FAQs
│
├── models/
│   ├── __init__.py
│   ├── user.py                 # User model (auth, password hashing, roles)
│   ├── customer.py             # Customer profile & orders relationship
│   ├── agent.py                # Agent profile, department, active chats
│   ├── order.py                # Mock retail orders & tracking
│   ├── conversation.py         # Support sessions, intent, sentiment, status
│   ├── message.py              # Individual message logs & metrics
│   └── knowledge_base.py       # FAQ entries for semantic retrieval
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Login, register, logout, API auth
│   ├── customer.py             # Chat view, past sessions, order tracking
│   ├── chatbot.py              # /api/chat orchestration, escalation, messages
│   ├── agent.py                # Agent inbox, live agent chat, chat claim
│   ├── admin.py                # Admin overview, Knowledge Base CRUD
│   └── analytics.py            # JSON analytics endpoint for Chart.js
│
├── ai/
│   ├── __init__.py
│   ├── intent_classifier.py    # Hybrid scikit-learn intent classifier
│   ├── sentiment_analyzer.py   # Emotion & frustration analyzer
│   ├── knowledge_base.py       # TF-IDF semantic FAQ retriever
│   ├── confidence.py           # Multi-factor confidence score calculator
│   ├── summarizer.py           # Structured handover summary generator
│   └── chatbot.py              # End-to-end AI pipeline coordinator
│
├── services/
│   ├── __init__.py
│   ├── conversation_service.py # Conversation lifecycle management
│   ├── escalation_service.py   # Handover trigger to agent queue
│   ├── order_service.py        # Order search & customer lookup
│   └── agent_service.py        # Agent assignment, transfers, resolution
│
├── templates/
│   ├── base.html               # Master layout with responsive nav & dark mode
│   ├── login.html              # Login with one-click demo credentials
│   ├── register.html           # Customer registration
│   ├── customer_chat.html      # ChatGPT-style support chat interface
│   ├── conversation_history.html # Past session transcripts & order history
│   ├── agent_dashboard.html    # Agent queue (Pending, Active, Resolved)
│   ├── agent_chat.html         # Agent workspace with customer intel & AI summary
│   ├── admin_dashboard.html    # Executive dashboard with Chart.js
│   ├── knowledge_base.html     # Knowledge Base CRUD manager
│   └── analytics.html          # Deep telemetry reports
│
├── static/
│   ├── css/
│   │   └── style.css           # Modern dark-mode UI styling
│   └── js/
│       └── chat.js             # Real-time WebSocket chat client
│
└── tests/
    ├── test_chatbot.py         # AI intent, sentiment, KB, confidence tests
    ├── test_auth.py            # Authentication, hashing, session tests
    └── test_escalation.py      # Full handover lifecycle unit tests
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.11+**
- **Git**

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Seed Demo Data
```bash
python database/seed.py
```
This automatically seeds:
- 10 Customers (including **Rahul**)
- 5 Agents (including **Priya Sharma**)
- 20 Orders (`ORD1001` through `ORD1020`)
- 30 Knowledge Base FAQs across 7 categories
- Pre-populated demo conversation transcripts

### 5. Run the Application
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🔑 Demo Login Credentials

All demo accounts share the password **`password123`**:

| Role | Email | Password | What You Can Test |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@example.com` | `password123` | Executive metrics, Chart.js telemetry, FAQ Knowledge Base CRUD |
| **Agent** | `agent@example.com` | `password123` | Agent inbox, claim escalated chats, real-time handover chat, resolve |
| **Customer** | `customer@example.com` | `password123` | Chat with AI, track `ORD1001`, trigger human handover |

*(Quick-login buttons are also provided directly on the login screen for instant testing!)*

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
pytest -v
```

---

## 🔌 REST API Endpoints

### Authentication
- `POST /api/login` - Authenticate user & start session
- `POST /api/register` - Create customer profile

### Customer Chatbot
- `POST /api/chat` - Send customer message through AI pipeline
- `GET /api/conversations` - List customer conversations
- `GET /api/conversations/<id>` - Retrieve conversation transcript
- `POST /api/conversations/<id>/message` - Append message
- `POST /api/conversations/<id>/escalate` - Manually request human agent handover

### Agent Operations
- `GET /api/agent/queue` - Retrieve pending and active queues
- `POST /api/conversations/<id>/assign` - Assign agent to conversation
- `POST /api/conversations/<id>/resolve` - Mark conversation as resolved
- `POST /api/conversations/<id>/transfer` - Transfer conversation to another agent

### Orders & Knowledge Base
- `GET /api/orders/<order_id>` - Fetch order details
- `GET /api/knowledge-base` - Search and list FAQ entries
- `POST /api/knowledge-base` - Create FAQ entry
- `PUT /api/knowledge-base/<id>` - Update FAQ entry
- `DELETE /api/knowledge-base/<id>` - Delete FAQ entry
- `GET /api/admin/analytics` - System metrics for Chart.js dashboards

---

## 🤖 Replacing the Local AI with OpenAI / Gemini / Claude

The local hybrid classifier in `ai/intent_classifier.py` and `ai/chatbot.py` is fully decoupled:

1. Add your API key in `.env`:
   ```bash
   OPENAI_API_KEY=sk-...
   # or
   GEMINI_API_KEY=...
   ```
2. In `ai/intent_classifier.py`, implement `predict_with_llm`:
   ```python
   def predict_with_llm(self, text, api_key=None, provider="openai"):
       # Call your LLM client with structured JSON output schema:
       # { "intent": "...", "confidence": 0.95, "order_id": "ORD..." }
       ...
   ```
3. Set your provider toggle in `config.py`.

---

## 🌐 Git Connection & Push Instructions

To push this codebase to your GitHub repository:

```bash
git add .
git commit -m "Complete AI Customer Service Chatbot with Human Agent Handover"
git push -u origin main
```
