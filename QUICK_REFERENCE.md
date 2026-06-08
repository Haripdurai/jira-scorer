# 🎯 JIRA Ticket Scorer - Quick Reference

## 📦 What's Included

```
jira-scorer/
├── 📱 Frontend (React + Vite)
│   ├── Single ticket scoring UI
│   ├── Batch processing UI
│   └── Prompt editor UI
│
├── 🔧 Backend (Flask + Python)
│   ├── REST API endpoints
│   ├── JIRA integration
│   └── Claude AI integration
│
├── 📓 Jupyter Notebook
│   └── Interactive analysis & batch processing
│
└── 📝 Documentation
    ├── README.md
    ├── LANGFLOW_GUIDE.md
    └── This quick reference
```

## 🚀 Quick Start (3 Steps)

### 1️⃣ Setup (One Time)
```bash
cd jira-scorer
./setup.sh
```

### 2️⃣ Configure
Edit `backend/.env`:
```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_TOKEN=your_jira_token
OPENAI_API_KEY=sk-proj-...
```

### 3️⃣ Run
**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Open:** http://localhost:3000

## 🔑 Getting API Keys

### JIRA Token
1. Visit: https://id.atlassian.com/manage-profile/security/api-tokens
2. Create token
3. **Important:** Use your email as username + token for auth

### OpenAI Key
1. Visit: https://platform.openai.com
2. Go to API Keys
3. Create new key (starts with sk-proj-...)

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/score-ticket` | POST | Score single ticket |
| `/api/batch-score` | POST | Score multiple tickets |
| `/api/prompt` | GET | Get scoring prompt |
| `/api/health` | GET | Health check |

## 🎨 Customization

### Edit Scoring Criteria
1. Open `backend/scoring_prompt.md`
2. Modify the prompt
3. Restart backend server

### Modify UI
1. Edit files in `frontend/src/components/`
2. Changes auto-reload in dev mode

## 💡 Common Tasks

### Score a Single Ticket
1. Go to "Single Ticket" tab
2. Enter JIRA URL & ticket ID
3. Add credentials
4. Click "Score Ticket"

### Batch Score
1. Go to "Batch Scoring" tab
2. Enter multiple ticket IDs (comma/newline separated)
3. Add credentials
4. Click "Score All Tickets"
5. Export results to CSV

### Use Jupyter Notebook
```bash
cd backend
jupyter notebook jira_scorer.ipynb
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| CORS errors | Check backend is on port 5000 |
| JIRA auth fails | Verify token & email |
| Module not found | Run `pip install -r requirements.txt` |
| Port in use | Kill process or change port |

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Main Flask API |
| `backend/scoring_prompt.md` | Scoring criteria |
| `backend/jira_scorer.ipynb` | Jupyter notebook |
| `frontend/src/App.jsx` | Main React app |
| `frontend/src/components/TicketScorer.jsx` | Single ticket UI |
| `frontend/src/components/BatchScorer.jsx` | Batch scoring UI |

## 🎯 Scoring Output

The AI evaluates:
- **Description Clarity** (0-10)
- **Technical Details** (0-10)
- **Acceptance Criteria** (0-10)
- **Overall Score** (0-10)
- **Recommendations**
- **Risk Level**

## 🔧 Tech Stack

- **Frontend:** React 18, Vite, Axios
- **Backend:** Flask, Python 3.8+
- **AI:** OpenAI GPT-4o
- **Integration:** JIRA REST API (Basic Auth)
- **Data:** Pandas, Jupyter

## 📚 Learn More

- Full docs: `README.md`
- LangFlow guide: `LANGFLOW_GUIDE.md`
- API docs: Check backend code comments

## 🆘 Getting Help

1. Check README.md troubleshooting
2. Review error messages
3. Verify API credentials
4. Check server logs

---

**Pro Tip:** Start with 5-10 tickets to test before running large batches!
