# AI Financial Mentor 💰🤖

An AI-powered personal finance management and financial education web platform built as an academic Software Engineering project.

The platform empowers users to manage their cashflow (income & expenses), track financial health via interactive visualizations, ask an AI Financial Mentor questions grounded in their spending habits, explore core financial literacy topics, and review conversation history with strict multi-user data isolation.

---

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Architecture & Structure](#project-architecture--structure)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Overview](#api-overview)
- [Automated & Isolation Testing](#automated--isolation-testing)
- [Security & Architecture Principles](#security--architecture-principles)
- [Educational Disclaimer](#educational-disclaimer)

---

## Features

1. **Secure Authentication & Authorization**
   - User registration and login using JWT access tokens.
   - Passwords hashed with `bcrypt`.
   - Protected endpoints enforced via HTTP Bearer token dependency (`/auth/me`).

2. **Income Management**
   - Full CRUD operations: add, view, update, and delete income records.
   - Categorized earnings (Salary, Freelance, Business, Investments, Rental, etc.).
   - Strict database scoping ensuring users only access their own income records.

3. **Expense Management**
   - Categorized expense tracking (Food, Transport, Education, Entertainment, Shopping, Bills, Healthcare, Other).
   - Input validation (`amount > 0`, non-empty category, valid dates).
   - Category filtering and INR (₹) formatting.

4. **Financial Dashboard & Analytics**
   - Key performance indicators: Total Income, Total Expenses, Net Savings, and Savings Rate percentage.
   - **Expense Breakdown Chart**: Interactive donut/pie chart powered by Recharts.
   - **Monthly Cashflow Trend**: Multi-bar chart comparing Income, Outgoings, and Savings over time.

5. **AI Financial Mentor**
   - Interactive chat interface guiding users through personal finance questions.
   - Answers educational concepts (Compound Interest, SIP, Budgeting, Emergency Funds).
   - Capable of personalized spending observations using aggregated financial summaries (without exposing PII or passwords).
   - Controlled system prompt preventing reckless speculative advice or claims of licensed financial credentials.
   - Offline fallback mode if an API key is not yet configured.

6. **Financial Education Center**
   - Beginner-friendly deep dives into 7 core topics:
     1. Budgeting & 50/30/20 Rule
     2. Smart Saving Habits
     3. Compound Interest
     4. Emergency Fund Essentials
     5. Systematic Investment Plans (SIP)
     6. Mutual Funds Demystified
     7. Credit Score & Responsible Debt
   - **Interactive SIP & Compounding Calculator**: Live slider/input tool computing total invested, estimated wealth gain, and future maturity corpus.

7. **Financial Profile & Investor Risk Questionnaire**
   - Structured user profile capturing Age, Risk Tolerance (Conservative, Moderate, Aggressive), Investment Horizon (<3 yrs, 3-5 yrs, 5-10 yrs, >10 yrs), Primary Financial Goal, Current Emergency Savings (₹), and Downside Volatility Reaction.
   - User-scoped persistence with real-time editing and validation.

8. **Personalized Investment Recommendations Engine (Rule-Based)**
   - Deterministic calculations: Average monthly income, expenses, net savings, savings rate, emergency fund runway months, and conservative investment capacity.
   - **Investment Readiness Heuristic**: Assigns categorical status (`NOT_READY`, `BUILD_EMERGENCY_FUND`, `READY_TO_EXPLORE`, `STRONG_INVESTMENT_CAPACITY`).
   - **Prioritized Recommendations**: Color-coded action items (HIGH / MEDIUM / LOW) across emergency fund buffers, discretionary spending trims, and horizon/risk-matched instruments (liquid debt, hybrid funds, diversified equity index fund SIPs).
   - Direct integration with AI Mentor via pre-filled contextual query chips.

9. **AI Chat History**
   - Automatically stores all interactions in reverse-chronological order.
   - User-isolated query and deletion capabilities.

---

## Technology Stack

### Backend
- **Language**: Python 3.14 / 3.10+
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Database & ORM**: SQLite & SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Security**: Passlib with Bcrypt (`bcrypt==4.0.1`), Python-Jose (JWT)
- **HTTP/LLM Client**: HTTPX
- **Testing**: Pytest

### Frontend
- **Framework**: React 19 + Vite
- **Styling**: Tailwind CSS v4
- **Routing**: React Router DOM v7
- **HTTP Client**: Axios (with JWT interceptors and auto-logout on 401)
- **Charts & Data Visualization**: Recharts
- **Icons**: Lucide React

---

## Project Architecture & Structure

The codebase maintains a clean layered architecture:
```
Client (React / Axios)
        ↓
FastAPI Router
        ↓
Service Layer (Business Logic & User Scoping)
        ↓
SQLAlchemy ORM Model
        ↓
SQLite Database
```

```
AI-Financial-Mentor/
│
├── backend/
│   ├── app/
│   │   ├── database/          # Database engine and model registrations
│   │   │   ├── base.py
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy database entities
│   │   │   ├── user.py
│   │   │   ├── income.py
│   │   │   ├── expense.py
│   │   │   ├── chat_history.py
│   │   │   └── financial_profile.py
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── income.py
│   │   │   ├── expense.py
│   │   │   ├── dashboard.py
│   │   │   ├── chat.py
│   │   │   ├── financial_profile.py
│   │   │   └── recommendation.py
│   │   ├── services/          # Business logic and user isolation
│   │   │   ├── auth_service.py
│   │   │   ├── income_service.py
│   │   │   ├── expense_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── financial_profile_service.py
│   │   │   ├── financial_analysis_service.py
│   │   │   ├── recommendation_service.py
│   │   │   ├── financial_ai_engine.py
│   │   │   └── ai_service.py
│   │   ├── routers/           # FastAPI API route controllers
│   │   │   ├── auth.py
│   │   │   ├── income.py
│   │   │   ├── expense.py
│   │   │   ├── dashboard.py
│   │   │   ├── chatbot.py
│   │   │   ├── profile.py
│   │   │   └── recommendations.py
│   │   ├── utils/             # Helpers, constants, and JWT security
│   │   │   ├── constants.py
│   │   │   ├── helpers.py
│   │   │   └── security.py
│   │   ├── config.py          # Centralized configuration & environment loader
│   │   └── main.py            # FastAPI app initialization, CORS, and routing
│   │
│   ├── tests/                 # Automated pytest test suites
│   │   ├── conftest.py        # Test database fixtures and overrides
│   │   ├── test_auth.py
│   │   ├── test_income.py
│   │   ├── test_expense.py
│   │   ├── test_dashboard.py
│   │   ├── test_ai.py
│   │   ├── test_isolation.py  # User A vs User B data boundary verification
│   │   └── test_profile_and_recommendations.py # Profile & recommendations verification
│   │
│   ├── .env                   # Environment variables (excluded from git)
│   ├── requirements.txt       # Backend dependencies
│   └── finance.db             # Local SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js      # Axios instance with Bearer token interceptor
│   │   ├── context/
│   │   │   └── AuthContext.jsx# User login state & JWT token lifecycle
│   │   ├── components/
│   │   │   ├── Layout.jsx     # Navigation bar, mobile drawer, and footer
│   │   │   └── ProtectedRoute.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx  # KPI summary cards & Recharts graphs
│   │   │   ├── Income.jsx     # Income records table & CRUD modal
│   │   │   ├── Expenses.jsx   # Expense records table & CRUD modal
│   │   │   ├── FinancialProfile.jsx # Investor questionnaire & risk assessment
│   │   │   ├── Recommendations.jsx # Prioritized investment recommendations & KPI bar
│   │   │   ├── AIMentor.jsx   # Interactive AI chat interface
│   │   │   ├── LearningCenter.jsx # 7 educational modules & SIP calculator
│   │   │   └── ChatHistory.jsx# Past conversation timeline
│   │   ├── App.jsx            # Application routing definitions
│   │   ├── main.jsx
│   │   └── index.css          # Tailwind CSS styles
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## Installation & Setup

### Prerequisites
- **Python**: Version 3.10 or newer (tested with Python 3.14.3)
- **Node.js**: Version 18 or newer (tested with Node v24.16.0)
- **Git**

---

### Backend Setup

1. Open a terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   - **Windows (Command Prompt / PowerShell)**:
     ```powershell
     venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

3. If creating a fresh virtual environment from scratch:
   ```bash
   python -m venv venv
   # activate venv, then:
   pip install -r requirements.txt
   ```

4. Verify or create your `backend/.env` file (see [Environment Variables](#environment-variables)).

---

### Frontend Setup

1. Open a second terminal window and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

---

## Environment Variables

Create or review `backend/.env` with the following variables:

```ini
# Application Settings
APP_NAME="AI Financial Mentor API"
APP_VERSION="1.0.0"

# Database Connection
DATABASE_URL="sqlite:///./finance.db"

# JWT Token Settings
SECRET_KEY="your-secure-random-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Financial Mentor (OpenAI or compatible LLM API)
OPENAI_API_KEY="your-openai-api-key-here"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_MODEL="gpt-4o-mini"
```

> **Note**: If `OPENAI_API_KEY` is not provided, the AI Mentor service automatically runs in an **offline educational mode**, answering questions and persisting conversations without throwing runtime exceptions.

---

## Running the Application

### 1. Start the Backend Server
From the `backend/` folder (with virtual environment activated):
```bash
uvicorn app.main:app --reload --port 8000
```
- API Base URL: `http://localhost:8000`
- Interactive Swagger Documentation: `http://localhost:8000/docs`
- Alternative ReDoc: `http://localhost:8000/redoc`

### 2. Start the Frontend Server
From the `frontend/` folder:
```bash
npm run dev
```
- Web Application URL: `http://localhost:5173`

---

## API Overview

All routes except `/auth/register`, `/auth/login`, and `/` require an `Authorization: Bearer <token>` header.

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Authenticate credentials and receive JWT | No |
| `GET` | `/auth/me` | Fetch authenticated user profile | Yes |
| `POST` | `/income` | Create new income record | Yes |
| `GET` | `/income` | List all incomes for current user | Yes |
| `GET` | `/income/{income_id}` | Retrieve specific income by ID | Yes |
| `PUT` | `/income/{income_id}` | Update existing income record | Yes |
| `DELETE` | `/income/{income_id}` | Delete income record | Yes |
| `POST` | `/expenses` | Create new expense record | Yes |
| `GET` | `/expenses` | List all expenses for current user | Yes |
| `GET` | `/expenses/{expense_id}`| Retrieve specific expense by ID | Yes |
| `PUT` | `/expenses/{expense_id}`| Update existing expense record | Yes |
| `DELETE` | `/expenses/{expense_id}`| Delete expense record | Yes |
| `GET` | `/dashboard/summary` | Summary: total income, total expense, savings | Yes |
| `GET` | `/dashboard/category-breakdown` | Expense totals and percentages by category | Yes |
| `GET` | `/dashboard/monthly-trend` | Monthly income, expense, and savings trends | Yes |
| `GET` | `/profile` | Retrieve user's financial & risk profile | Yes |
| `POST` | `/profile` | Create or update user's financial profile | Yes |
| `GET` | `/recommendations` | Get rule-based personalized investment recommendations | Yes |
| `POST` | `/ai/chat` | Send question to AI mentor & save to history | Yes |
| `GET` | `/ai/history` | Retrieve user's previous AI conversations | Yes |
| `DELETE` | `/ai/history/{chat_id}` | Delete an AI conversation entry | Yes |

---

## Automated & Isolation Testing

The backend includes a dedicated test suite using an isolated in-memory/test database (`test_finance.db`) to ensure existing user records in `finance.db` are never modified or overwritten during testing.

To run the automated tests:
```powershell
cd backend
venv\Scripts\activate
pytest tests -v
```

### Test Coverage Highlights:
- **`test_auth.py`**: User registration, duplicate email handling, login validation, invalid password rejection, and `/auth/me` security.
- **`test_income.py`**: Full CRUD operations for income and unauthorized request rejection.
- **`test_expense.py`**: Expense CRUD operations, validation rules (`amount > 0`), and unauthorized rejection.
- **`test_dashboard.py`**: Verifies exact mathematical computation of total income, total expenses, savings, and category distribution percentages.
- **`test_profile_and_recommendations.py`**:
  - Financial Profile creation, update, and validation (rejecting negative emergency funds, validating risk levels).
  - Rule-based investment readiness states (`NOT_READY`, `BUILD_EMERGENCY_FUND`, `READY_TO_EXPLORE`, `STRONG_INVESTMENT_CAPACITY`).
  - Prioritized recommendations matching investment horizons (<3 years debt, 3-5 years hybrid, >5 years index SIP).
  - Strict user boundary isolation: User B cannot access or modify User A's profile or recommendations.
- **`test_ai.py`**: Tests AI chat generation, automatic `ChatHistory` persistence, retrieval, and entry deletion.
- **`test_isolation.py`**: **Mandatory Multi-User Boundary Test**. Simulates User A and User B concurrently:
  - Verifies User B cannot retrieve, update, or delete User A's income (`404 Not Found`).
  - Verifies User B cannot retrieve, update, or delete User A's expenses (`404 Not Found`).
  - Verifies User B cannot see or delete User A's chat history.
  - Verifies User B's dashboard metrics reflect `0.0` and never leak User A's financial transactions.

---

## Security & Architecture Principles

1. **Strict User Scoping**: Every database query is explicitly filtered by `user_id == current_user.id`. Foreign key boundaries prevent horizontal privilege escalation.
2. **Password Security**: Passwords are saved exclusively as salted one-way hashes via bcrypt. The `password_hash` is stripped from all API response schemas.
3. **No Hardcoded Secrets**: Secrets and API keys are loaded via `python-dotenv`. `.env` is explicitly ignored in `.gitignore`.
4. **CORS Protected**: Configured FastAPI CORS middleware allows communication strictly with trusted frontend origins.
5. **Robust Error Handling**: Clean JSON error responses with standard HTTP status codes (`200`, `201`, `400`, `401`, `404`, `422`, `500`), suppressing raw internal stack traces from client visibility.

---

## Educational Disclaimer

**AI Financial Mentor** is developed strictly as an academic Software Engineering course project. All financial advice, budgeting tips, investment explanations, and AI responses are for general educational purposes only. It is not licensed by SEBI, SEC, or any regulatory financial authority, and should not be used as a substitute for certified financial or legal counsel.
