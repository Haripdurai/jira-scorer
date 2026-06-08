# LangFlow Integration Guide

## Overview

While this application uses direct API calls to Claude, you can integrate LangFlow for more complex workflows and visual flow building.

## LangFlow Setup

### Installation

```bash
pip install langflow
```

### Creating a LangFlow Flow

1. **Start LangFlow:**
```bash
langflow run
```

2. **Access UI:** Open http://localhost:7860

3. **Create Flow:**
   - Add a "Text Input" node for the ticket data
   - Add a "Prompt Template" node with your scoring criteria
   - Add an "Anthropic" node (Claude)
   - Add a "Text Output" node for results
   - Connect the nodes

### Example Flow Structure

```
┌──────────────┐
│ JIRA Ticket  │
│ Input (JSON) │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Prompt Builder   │
│ (scoring_prompt) │
└──────┬───────────┘
       │
       ▼
┌──────────────┐
│ Claude API   │
│ (Anthropic)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Score Output │
└──────────────┘
```

## Integrating LangFlow with the Backend

### Option 1: Export Flow as Python

1. In LangFlow, click "Export" → "Python Code"
2. Save to `backend/langflow_scorer.py`
3. Import in `app.py`:

```python
from langflow_scorer import run_flow

def score_ticket_with_langflow(ticket_info):
    result = run_flow(ticket_info)
    return result
```

### Option 2: Use LangFlow API

Start LangFlow in API mode:

```bash
langflow run --host 0.0.0.0 --port 7860
```

Then call it from the backend:

```python
import requests

def score_with_langflow_api(ticket_data):
    response = requests.post(
        'http://localhost:7860/api/v1/run/your-flow-id',
        json={'input': ticket_data}
    )
    return response.json()
```

## Advanced LangFlow Features

### Memory/Context

Add a "Memory" node to maintain context across multiple ticket evaluations:

```
Ticket 1 → Memory → Claude → Score 1
Ticket 2 → Memory → Claude → Score 2 (with context)
```

### Chain of Thought

Create a multi-step evaluation:

```
Ticket → Analyze Description → Score
      → Analyze Technical → Score
      → Analyze Criteria → Score
      → Aggregate Scores → Final Score
```

### Custom Tools

Add custom tools for:
- JIRA API integration
- Database storage
- Slack notifications
- Email reports

## Environment Variables for LangFlow

Add to `backend/.env`:

```env
LANGFLOW_API_URL=http://localhost:7860
LANGFLOW_FLOW_ID=your-flow-id-here
```

## Example LangFlow Configuration

Create a file `backend/langflow_config.json`:

```json
{
  "flow": {
    "name": "JIRA Ticket Scorer",
    "nodes": [
      {
        "id": "input",
        "type": "TextInput",
        "data": {
          "name": "ticket_data"
        }
      },
      {
        "id": "prompt",
        "type": "PromptTemplate",
        "data": {
          "template": "{scoring_prompt}\n\nTicket: {ticket_data}"
        }
      },
      {
        "id": "llm",
        "type": "Anthropic",
        "data": {
          "model": "claude-sonnet-4-20250514",
          "max_tokens": 1500
        }
      },
      {
        "id": "output",
        "type": "TextOutput"
      }
    ],
    "edges": [
      {"source": "input", "target": "prompt"},
      {"source": "prompt", "target": "llm"},
      {"source": "llm", "target": "output"}
    ]
  }
}
```

## Benefits of Using LangFlow

1. **Visual Flow Building:** See your AI workflow visually
2. **No-Code Editing:** Modify flows without changing code
3. **Experimentation:** Try different prompts and models easily
4. **Version Control:** Save and version different flow configurations
5. **Debugging:** Step through flows to debug issues
6. **Integration:** Built-in connectors for many tools

## When to Use LangFlow vs Direct API

### Use LangFlow when:
- You need complex multi-step workflows
- You want visual flow management
- You're experimenting with different approaches
- You need to integrate multiple AI models
- Non-developers need to modify the flow

### Use Direct API when:
- You have simple, straightforward requests
- You need maximum performance
- You want full control over the code
- You're deploying to production with stable requirements

## Further Resources

- [LangFlow Documentation](https://docs.langflow.org/)
- [LangFlow GitHub](https://github.com/logspace-ai/langflow)
- [Example Flows](https://github.com/logspace-ai/langflow/tree/main/examples)
