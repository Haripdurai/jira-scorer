# 🚀 JIRA Ticket Scorer - OpenAI POC Setup Guide

## Quick Setup (5 Minutes)

### Step 1: Extract the Archive
```bash
tar -xzf jira-scorer-openai.tar.gz
cd jira-scorer
```

### Step 2: Get Your Credentials

#### JIRA Credentials
1. **JIRA URL:** Your instance URL (e.g., `https://yourcompany.atlassian.net`)
2. **JIRA Username:** Your email address (e.g., `you@company.com`)
3. **JIRA API Token:**
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Name it (e.g., "Ticket Scorer POC")
   - Copy the token

#### OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it (e.g., "JIRA Scorer POC")
4. Copy the key (starts with `sk-proj-...`)

### Step 3: Configure Backend
```bash
cd backend
cp .env.example .env
```

Edit `.env` file:
```env
JIRA_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=you@company.com
JIRA_TOKEN=your_jira_api_token_here
OPENAI_API_KEY=sk-proj-your_openai_key_here
FLASK_ENV=development
FLASK_PORT=5000
```

### Step 4: Install Dependencies

**Backend:**
```bash
# In backend/ directory
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
# In frontend/ directory
cd ../frontend
npm install
```

### Step 5: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
You should see: `Local: http://localhost:3000`

### Step 6: Test It!

1. Open: http://localhost:3000
2. Click "Single Ticket" tab
3. Fill in the form:
   - **JIRA URL:** `https://yourcompany.atlassian.net`
   - **JIRA Username:** `you@company.com`
   - **Ticket ID:** Any valid ticket (e.g., `PROJ-123`)
   - **JIRA API Token:** Paste your token
   - **OpenAI API Key:** Paste your OpenAI key
4. Click "Score Ticket"

## 🎯 What You'll Get

The AI will analyze your ticket and provide:
- **Description Clarity Score** (0-10)
- **Technical Details Score** (0-10)
- **Acceptance Criteria Score** (0-10)
- **Overall Score** (0-10)
- **Strengths** of the ticket
- **Areas for Improvement**
- **Actionable Recommendations**
- **Risk Level Assessment**

## 🔧 JIRA Authentication Explained

JIRA uses **Basic Authentication** with:
- **Username:** Your JIRA email address
- **Password:** API token (NOT your JIRA password)

The app automatically encodes these as: `base64(email:token)`

## 💡 POC Testing Tips

### Test Single Tickets First
1. Find a well-written ticket → See what high scores look like
2. Find a poorly-written ticket → See improvement suggestions
3. Compare scores to validate the AI's assessment

### Try Batch Scoring (5-10 tickets)
1. Go to "Batch Scoring" tab
2. Enter ticket IDs like:
   ```
   PROJ-123
   PROJ-124
   PROJ-125
   ```
3. Export results to CSV for analysis

### Customize the Scoring
1. Go to "Customize Prompt" tab
2. View the current prompt
3. To modify permanently: Edit `backend/scoring_prompt.md`
4. Restart backend server

## 📊 Cost Estimation (OpenAI)

**GPT-4o Pricing:**
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens

**Typical ticket scoring:**
- ~1,500 input tokens (prompt + ticket)
- ~500 output tokens (score)
- **Cost per ticket:** ~$0.005 (half a cent)

**For POC with 100 tickets:**
- Total cost: ~$0.50

## 🐛 Common Issues

### "Failed to fetch JIRA ticket: 401"
- ✅ Check your JIRA username is your email
- ✅ Verify your API token is correct
- ✅ Make sure token hasn't expired

### "Failed to score ticket: 401" (OpenAI)
- ✅ Check your OpenAI API key
- ✅ Verify you have credits in your OpenAI account
- ✅ Key should start with `sk-proj-`

### "CORS error"
- ✅ Make sure backend is running on port 5000
- ✅ Frontend should be on port 3000
- ✅ Check both terminals are running

### Port already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## 📝 Next Steps After POC

1. **Collect Feedback:** Get team input on scoring accuracy
2. **Refine Prompt:** Customize scoring criteria for your team
3. **Scale Testing:** Try with 50-100 tickets
4. **Integration:** Consider integrating with your workflow
5. **Automation:** Set up scheduled batch scoring

## 🔐 Security Notes for POC

- Keep API keys secure (never commit to git)
- JIRA tokens can be revoked anytime
- OpenAI keys can be restricted by IP
- Consider using environment-specific keys

## 📚 Files to Know

| File | Purpose | When to Edit |
|------|---------|--------------|
| `backend/.env` | Credentials | Setup |
| `backend/scoring_prompt.md` | AI scoring criteria | Customize scoring |
| `backend/app.py` | Backend API | Add features |
| `frontend/src/components/` | UI components | Change interface |

## 🎓 Learn More

- **Full Documentation:** See `README.md`
- **Quick Reference:** See `QUICK_REFERENCE.md`
- **Jupyter Notebook:** See `backend/jira_scorer.ipynb` for advanced usage

---

**Need Help?** Check the troubleshooting section or review the full README.md

**Ready for Production?** Consider security hardening, rate limiting, and proper key management.
