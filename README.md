# webhook-repo

GitHub Webhook Receiver

## Features

Real-time processing of GitHub webhooks

MongoDB storage with proper schema

Auto-refreshing UI (15s interval)

Supports:

   -Push events
   
   -Pull request events

   -Merge events

## Installation

Clone repository:

```bash
git clone https://github.com/yourusername/webhook-repo.git
cd webhook-repo
```

Set up environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure environment:

config.py

    MONGO_URI=mongodb://localhost:27017/webhook
    SECRET_KEY=your-secret-key-here
    
## Running the Application
    python run.py
    
Access UI at: http://localhost:5000

## Ngrok 

```bash
ngrok http 50
```

Will get the link https://1234-990-92i9333.ngrok-free.app/webhook and add it in action-repo webhook 

Can access the Github UI by accesing this link https://1234-990-92i9333.ngrok-free.app

## MongoDB Schema

Field	Type	Description
_id	ObjectID	Auto-generated ID
request_id	String	Commit hash or PR ID
author	String	GitHub username
action	String	PUSH/PULL REQUEST/MERGE
from_branch	String	Source branch
to_branch	String	Target branch
timestamp	ISODate	Event time (UTC)

## API Endpoints

POST /webhook - GitHub webhook receiver

GET / - Web interface

GET /api/events - JSON event data

## UI Features

Real-time updates (15s polling)

Clean event display:

```text
[User] [action] from [branch] to [branch] at [time]
```

IST timezone conversion

Responsive design
