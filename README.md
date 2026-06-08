# 🎯 JIRA Ticket Scorer

An AI-powered application to automatically score and evaluate JIRA tickets based on description quality, technical details, and acceptance criteria.

## 📋 Features

- **Single Ticket Scoring**: Score individual JIRA tickets with detailed feedback
- **Batch Processing**: Score multiple tickets at once and export results to CSV
- **Customizable Prompts**: Edit the scoring criteria via a markdown file
- **Interactive UI**: Clean, modern React interface
- **Jupyter Notebook**: Python notebook for advanced analysis and batch processing
- **REST API**: Flask backend with comprehensive API endpoints

## 🏗️ Architecture

```
jira-scorer/
├── frontend/                # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── backend/                # Flask application
    ├── app.py             # Flask REST API
    ├── jira_scorer.ipynb  # Jupyter notebook
    ├── scoring_prompt.md  # Customizable scoring prompt
    └── requirements.txt   # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- JIRA account with API access
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

Example `.env` file:
```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_TOKEN=your_jira_api_token
OPENAI_API_KEY=sk-proj-your_openai_key
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.example .env
# Edit if needed (default points to localhost:5000)
```

4. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## 📖 Usage

### Web Interface

1. Open `http://localhost:3000` in your browser
2. Choose a tab:
   - **Single Ticket**: Score one ticket at a time
   - **Batch Scoring**: Score multiple tickets
   - **Customize Prompt**: Edit scoring criteria

#### Single Ticket Scoring

1. Enter your JIRA URL (e.g., `https://your-domain.atlassian.net`)
2. Enter your JIRA username (your email address)
3. Enter the ticket ID (e.g., `PROJ-123`)
4. Provide your JIRA API token
5. Provide your OpenAI API key
6. Click "Score Ticket"

#### Batch Scoring

1. Enter your JIRA URL
2. Enter multiple ticket IDs (comma or newline separated)
3. Provide credentials
4. Click "Score All Tickets"
5. Export results to CSV

### Jupyter Notebook

The `jira_scorer.ipynb` notebook provides:
- Interactive JIRA API exploration
- Batch processing capabilities
- Data analysis and visualization
- Export to CSV/JSON

To use:
```bash
cd backend
jupyter notebook jira_scorer.ipynb
```

## 🔧 API Endpoints

### `POST /api/score-ticket`

Score a single JIRA ticket.

**Request:**
```json
{
  "jira_url": "https://your-domain.atlassian.net",
  "ticket_id": "PROJ-123",
  "jira_username": "your-email@example.com",
  "jira_token": "your-jira-token",
  "openai_api_key": "sk-proj-your-api-key"
}
```

**Response:**
```json
{
  "success": true,
  "ticket_info": {
    "key": "PROJ-123",
    "summary": "Ticket summary",
    "description": "...",
    "status": "To Do",
    "priority": "High"
  },
  "score": {
    "ticket_key": "PROJ-123",
    "score_text": "Detailed scoring..."
  }
}
```

### `POST /api/batch-score`

Score multiple JIRA tickets.

**Request:**
```json
{
  "jira_url": "https://your-domain.atlassian.net",
  "ticket_ids": ["PROJ-123", "PROJ-124", "PROJ-125"],
  "jira_username": "your-email@example.com",
  "jira_token": "your-jira-token",
  "openai_api_key": "sk-proj-your-api-key"
}
```

### `GET /api/prompt`

Get the current scoring prompt.

### `GET /api/health`

Health check endpoint.

## 🎨 Customizing the Scoring Prompt

The scoring criteria is defined in `backend/scoring_prompt.md`. This file uses markdown and can be edited to:

- Change scoring criteria
- Adjust scoring weights
- Modify output format
- Add domain-specific requirements

After editing, restart the Flask server for changes to take effect.

## 🔑 Getting API Credentials

### JIRA API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token
4. **Authentication Format:**
   - **Username:** Your JIRA email address (e.g., `you@company.com`)
   - **Token:** The API token you just created
   - **Auth Type:** Basic Authentication (username:token)

### OpenAI API Key

1. Go to https://platform.openai.com
2. Navigate to API Keys section
3. Create a new key
4. Copy and save it securely (starts with `sk-proj-...`)

## 📊 Scoring Criteria

The default scoring evaluates:

1. **Description Clarity (0-10)**
   - Problem articulation
   - Context and background
   - Developer comprehension

2. **Technical Details (0-10)**
   - Technical requirements
   - Dependencies
   - Constraints and scope

3. **Acceptance Criteria (0-10)**
   - Clarity and testability
   - Scenario coverage
   - Format quality

## 🛠️ Development

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Running Tests

```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
pytest
```

## 📝 Environment Variables

### Backend (.env)

```env
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_TOKEN=your_token
OPENAI_API_KEY=sk-proj-your_key
FLASK_ENV=development
FLASK_PORT=5000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - feel free to use this project for your needs.

## 🐛 Troubleshooting

### CORS Errors
- Ensure backend is running on port 5000
- Check CORS_ORIGINS in backend .env

### JIRA Authentication Errors
- Verify your API token is correct
- Ensure you're using your email address as the username
- JIRA uses Basic Authentication (email:token)
- Check JIRA URL format (include https://)

### API Rate Limits
- OpenAI has rate limits based on your plan tier
- Consider adding delays between batch requests
- Monitor your usage at platform.openai.com

## 💡 Tips

- Start with a small batch (5-10 tickets) to test
- Customize the prompt for your team's needs
- Export batch results to CSV for analysis
- Use the Jupyter notebook for advanced workflows

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation
- Open an issue on GitHub

---

Built with ❤️ using React, Flask, and OpenAI GPT-4o
