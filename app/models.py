from datetime import datetime
from flask import current_app

def save_github_event(data):
    try:
        event = {
            'request_id': get_request_id(data),
            'author': data.get('sender', {}).get('login', 'unknown'),
            'action': determine_action(data),
            'from_branch': get_source_branch(data),
            'to_branch': get_target_branch(data),
            'timestamp': datetime.utcnow().isoformat()
        }
        return current_app.mongo.db.events.insert_one(event)
    except Exception as e:
        current_app.logger.error(f"Failed to save event: {e}")
        raise

def get_request_id(data):
    if 'head_commit' in data:
        return data['head_commit']['id'][:7]  
    elif 'pull_request' in data:
        return f"PR-{data['pull_request']['number']}"
    return 'N/A'

def determine_action(data):
    if 'pusher' in data:  
        return 'PUSH'
    elif 'pull_request' in data:
        if data.get('action') == 'closed' and data['pull_request']['merged']:
            return 'MERGE'
        return 'PULL REQUEST'
    return 'UNKNOWN'

def get_source_branch(data):
    if 'pull_request' in data:
        return data['pull_request']['head']['ref']
    return data.get('ref', '').replace('refs/heads/', '')

def get_target_branch(data):
    if 'pull_request' in data:
        return data['pull_request']['base']['ref']
    return data.get('ref', '').replace('refs/heads/', '')