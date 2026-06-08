from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from typing import Dict, List
import os
from pathlib import Path
import markdown
import base64

app = Flask(__name__)
CORS(app)

# Load prompt from markdown file
def load_prompt() -> str:
    prompt_file = Path(__file__).parent / 'scoring_prompt.md'
    if prompt_file.exists():
        with open(prompt_file, 'r') as f:
            return f.read()
    return """Score this JIRA ticket based on:
1. Description clarity (0-10)
2. Technical details completeness (0-10)
3. Acceptance criteria quality (0-10)

Provide an overall score (0-10) and brief feedback."""

# JIRA API functions
def extract_ticket_key(ticket_id: str) -> str:
    """Extract ticket key from either 'PROJ-123' or full URL format"""
    if '/' in ticket_id:
        # Extract from URL like 'https://domain/browse/PROJ-123'
        return ticket_id.split('/')[-1]
    return ticket_id

def get_jira_ticket(jira_url: str, ticket_id: str, jira_username: str, auth_token: str) -> Dict:
    """Fetch a JIRA ticket via API using Basic Auth"""
    # Extract the ticket key in case a full URL was passed
    ticket_key = extract_ticket_key(ticket_id)
    
    # Create basic auth string: username:token encoded in base64
    auth_string = f"{jira_username}:{auth_token}"
    auth_bytes = auth_string.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {base64_auth}',
        'Content-Type': 'application/json'
    }
    
    url = f"{jira_url}/rest/api/3/issue/{ticket_key}"
    # Disable SSL verification for development (can be enabled via env var)
    verify_ssl = os.getenv('VERIFY_SSL', 'false').lower() == 'true'
    
    try:
        response = requests.get(url, headers=headers, verify=verify_ssl)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch JIRA ticket: HTTP {response.status_code} - {response.text}")
    except requests.exceptions.SSLError as e:
        raise Exception(f"SSL Error connecting to JIRA: {str(e)}. Check your JIRA URL and try disabling SSL verification.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to JIRA: {str(e)}")

def extract_ticket_info(ticket_data: Dict) -> Dict:
    """Extract relevant information from JIRA ticket"""
    fields = ticket_data.get('fields', {})
    
    return {
        'key': ticket_data.get('key', ''),
        'summary': fields.get('summary', ''),
        'description': fields.get('description', ''),
        'acceptance_criteria': fields.get('customfield_10000', ''),  # Adjust field ID
        'labels': fields.get('labels', []),
        'priority': fields.get('priority', {}).get('name', ''),
        'status': fields.get('status', {}).get('name', '')
    }

def score_ticket_with_llm(ticket_info: Dict, api_key: str) -> Dict:
    """Score ticket using OpenAI API"""
    prompt_template = load_prompt()
    
    # Build the full prompt
    ticket_text = f"""
JIRA Ticket: {ticket_info['key']}
Summary: {ticket_info['summary']}

Description:
{ticket_info['description']}

Acceptance Criteria:
{ticket_info['acceptance_criteria']}

Priority: {ticket_info['priority']}
Status: {ticket_info['status']}
Labels: {', '.join(ticket_info['labels'])}
"""
    
    full_prompt = f"{prompt_template}\n\n{ticket_text}\n\nPlease provide the scoring."
    
    # Call OpenAI API
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-4o',  # Using GPT-4o for better performance
        'messages': [
            {
                'role': 'user',
                'content': full_prompt
            }
        ],
        'temperature': 0.7,
        'max_tokens': 1500
    }
    
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            'score_text': result['choices'][0]['message']['content'],
            'ticket_key': ticket_info['key'],
            'usage': result.get('usage', {})
        }
    else:
        raise Exception(f"Failed to score ticket: {response.status_code} - {response.text}")

@app.route('/api/score-ticket', methods=['POST'])
def score_ticket():
    """Main endpoint to score a JIRA ticket"""
    try:
        data = request.json
        
        jira_url = data.get('jira_url')
        ticket_id = data.get('ticket_id')
        jira_username = data.get('jira_username')
        jira_token = data.get('jira_token')
        openai_api_key = data.get('openai_api_key')
        
        if not all([jira_url, ticket_id, jira_username, jira_token, openai_api_key]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Fetch JIRA ticket
        ticket_data = get_jira_ticket(jira_url, ticket_id, jira_username, jira_token)
        
        # Extract relevant info
        ticket_info = extract_ticket_info(ticket_data)
        
        # Score with LLM
        score_result = score_ticket_with_llm(ticket_info, openai_api_key)
        
        return jsonify({
            'success': True,
            'ticket_info': ticket_info,
            'score': score_result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-score', methods=['POST'])
def batch_score():
    """Score multiple JIRA tickets"""
    try:
        data = request.json
        
        jira_url = data.get('jira_url')
        ticket_ids = data.get('ticket_ids', [])
        jira_username = data.get('jira_username')
        jira_token = data.get('jira_token')
        openai_api_key = data.get('openai_api_key')
        
        results = []
        
        for ticket_id in ticket_ids:
            try:
                ticket_data = get_jira_ticket(jira_url, ticket_id, jira_username, jira_token)
                ticket_info = extract_ticket_info(ticket_data)
                score_result = score_ticket_with_llm(ticket_info, openai_api_key)
                
                results.append({
                    'ticket_id': ticket_id,
                    'success': True,
                    'ticket_info': ticket_info,
                    'score': score_result
                })
            except Exception as e:
                results.append({
                    'ticket_id': ticket_id,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prompt', methods=['GET'])
def get_prompt():
    """Get the current scoring prompt"""
    return jsonify({'prompt': load_prompt()})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
