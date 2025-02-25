## Rocket.Chat Bot Development Reference

### 1. **User Input Handling (Message Event)**
User-generated messages initiate JSON payloads directed to the bot endpoint, enabling session contextualization.
```json
{
  "user": {"username": "john_doe", "_id": "u12345"},
  "room": {"_id": "r12345"},
  "message": {"_id": "m12345", "msg": "How do I add an image in LaTeX?"}
}
```
**Key Fields:** `user`, `room`, and `message` enable session and user-specific context tracking.

---

### 2. **File Upload Handling (File Upload Event)**
Bot endpoints process file uploads, including `.tex` and `.pdf` formats, ensuring contextual file association.
```json
{
  "file": {
    "_id": "f12345",
    "name": "document.pdf",
    "type": "application/pdf",
    "url": "https://chat.example.com/file-upload/f12345/document.pdf"
  },
  "user": {"username": "john_doe"},
  "room": {"_id": "r12345"}
}
```
**Key Fields:** `file.url` for file retrieval and `user._id` for session-specific tracking.

---

### 3. **Bot Response Formats**

**Basic Text Response:**
```json
{"msg": "To insert an image in LaTeX, use: `\\includegraphics{example.png}`"}
```

**Formatted Markdown:**
````json
{"msg": "**LaTeX Guide:** Inserting an Image:\n1. Ensure `graphicx` package inclusion.\n2. Use: ```\\includegraphics{example.png}```"}
````

**Attachment with Button:**
```json
{
  "attachments": [
    {
      "title": "LaTeX Image Guide",
      "text": "Access further documentation below:",
      "color": "#36a64f",
      "actions": [
        {"type": "button", "text": "View Documentation", "url": "https://ctan.org/pkg/graphicx"}
      ]
    }
  ]
}
```

**File Upload:**
```json
{
  "msg": "Access the LaTeX template below:",
  "attachments": [
    {"title": "LaTeX_Template.tex", "title_link": "https://your-server.com/files/latex_template.tex"}
  ]
}
```

---

### 4. **Interactive Button Event (Button Click Handling)**
User interactions via buttons generate action ID payloads for event-specific processing.
```json
{
  "actionId": "show_sources",
  "user": {"username": "john_doe", "_id": "u12345"},
  "room": {"_id": "r12345"}
}
```
**Key Field:** `actionId` identifies the specific button-triggered event.

---

### 5. **Input Validation (Sanitize User Inputs)**
To mitigate injection risks, sanitize user inputs rigorously.
```python
import re

def sanitize_input(user_input):
    return re.sub(r"[^\w\s.,!?-]", "", user_input)
```

---

### 6. **File Upload Validation**
Verify file integrity, type, and size prior to ingestion.
```python
ALLOWED_EXTENSIONS = {'tex', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_file(file):
    if file.content_length > MAX_FILE_SIZE:
        raise ValueError("File exceeds 10MB.")
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file format.")
```

---

### 7. **Session Isolation (User-Specific Upload Path)**
Enforce user-specific data segmentation for session integrity.
```python
import os

def user_upload_path(user_id):
    path = f"uploads/{user_id}/"
    os.makedirs(path, exist_ok=True)
    return path
```

---

### 8. **Error Handling (Message Processing)**
Implement robust exception handling to maintain operational stability.
```python
try:
    user_message = request.json.get("message", {}).get("msg")
    if not user_message:
        raise ValueError("Received empty message.")
except Exception as e:
    print(f"Error during message processing: {e}")
```

---

### 9. **API Request Handling (LLMProxy/CTAN)**
Ensure API call resilience through timeout and exception protocols.
```python
import requests

try:
    response = requests.post("https://api.llmproxy.com/generate", json=payload, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("API request timed out.")
except requests.exceptions.RequestException as e:
    print(f"API request encountered an error: {e}")
```

---

### 10. **Logging User Interactions**
Maintain comprehensive logs for user interactions and system events.
```python
import logging

logging.basicConfig(filename='logs/app.log', level=logging.INFO)

def log_interaction(user, message):
    logging.info(f"User: {user} | Message: {message}")
```

---

### 11. **Rate Limiting (Prevent Abuse)**
Enforce request thresholds to mitigate service abuse.
```python
from flask_limiter import Limiter

limiter = Limiter(get_remote_address, app=app, default_limits=["60 per minute"])
```

---

### 12. **Environment Security (API Keys)**
Secure sensitive credentials within environment variables.
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("LLM_PROXY_API_KEY")
```

---
