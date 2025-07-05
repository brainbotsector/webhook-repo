from flask import Blueprint, request, jsonify, render_template, current_app
from datetime import datetime, timezone, timedelta
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    try:
        events = list(current_app.mongo_db.events.find().sort('timestamp', -1).limit(10))
        for event in events:
            event['timestamp'] = convert_utc_to_ist(event['timestamp'])
        return render_template('index.html', events=events)
    except Exception as e:
        print(f" Error: {e}")
        return render_template('index.html', events=[])

def convert_utc_to_ist(utc_str):
    utc_time = datetime.fromisoformat(utc_str.replace('Z', '+00:00'))
    ist_time = utc_time.astimezone(timezone(timedelta(hours=5, minutes=30)))
    return ist_time.isoformat()

@bp.route('/webhook', methods=['POST'])
def webhook():
    print("\n Github Webhook actions...")
    try:
        if not request.headers.get('X-GitHub-Event'):
            print("Missing event header")
            return jsonify({'error': 'Invalid GitHub webhook'}), 400

        event_type = request.headers['X-GitHub-Event']
        data = request.get_json()
        
        print(f"Processing {event_type} event")
        
        doc = {
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        if event_type == 'push':
            doc.update({
                'request_id': data.get('after', 'N/A'),
                'author': data.get('pusher', {}).get('name') or data.get('sender', {}).get('login', 'unknown'),
                'action': 'PUSH',
                'to_branch': data.get('ref', '').replace('refs/heads/', ''),
                'from_branch': None  
            })
        elif event_type == 'pull_request':
            pr_data = data.get('pull_request', {})
            doc.update({
                'request_id': f"PR-{data.get('number', 'N/A')}",
                'author': data.get('sender', {}).get('login', 'unknown'),
                'action': 'MERGE' if data.get('action') == 'closed' and pr_data.get('merged') else 'PULL REQUEST',
                'from_branch': pr_data.get('head', {}).get('ref', ''),
                'to_branch': pr_data.get('base', {}).get('ref', '')
            })
        else:
            return jsonify({'status': 'ignored'}), 200

        result = current_app.mongo_db.events.insert_one(doc)
        print(f" Event stored to MongoDB with id: {result.inserted_id}")
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f" Webhook event failed: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/api/events')
def get_events():
    try:
        events = list(current_app.mongo_db.events.find().sort('timestamp', -1).limit(10))
        formatted_events = []
        for event in events:
            event['_id'] = str(event['_id'])
            event['timestamp'] = convert_utc_to_ist(event['timestamp'])
            formatted_events.append(event)
        return jsonify(formatted_events)
    except Exception as e:
        return jsonify({'error': str(e)}), 500