# chat.py
import os, jsonify
from config import get_logger
from llmproxy import generate
from utils import safe_load_text

_LOGGER = get_logger(__name__)
_WELCOME = os.environ.get("welcomePage")
_SYSTEM = os.environ.get("systemPrompt")
_MODEL = os.environ.get("model")
_TEMP = os.environ.get("temperature")
_LAST_K = os.environ.get("lastk")
_RAG = os.environ.get("rag_usage")
_RAG_K = os.environ.get("rag_k")
_RAG_THR = os.environ.get("rag_threshold")

def welcome(uid, user):
    with open(_WELCOME, "r", encoding="utf-8") as f:
        welcome = f.read()
    
    _LOGGER.info(f"Welcomed {user} (uid: {uid})")
    return jsonify({"text": welcome})

def query(msg: str, sid: str):
    system = safe_load_text(_SYSTEM)
    
    response = generate(
        model = _MODEL,
        system= system,
        query= msg,
        temperature= _TEMP,
        lastk= _LAST_K,
        rag_usage= _RAG,
        rag_k= _RAG_K,
        rag_threshold= _RAG_THR,
        session_id= sid,
    )

    resp_text = response['response']
    # resp_context = response['rag???']
    
    # Send response back
    rc_resp = {
        "text": response['response'],
        "attachments": [
            {
                "actions": [
                    {
                        "type": "button",
                        "text": "Show Sources",
                        "msg": "/show_sources",
                        "msg_in_chat_window": True
                    },
                    {
                        "type": "button",
                        "text": "Upload a Document",
                        "msg": "/upload_document",
                        "msg_in_chat_window": True
                    },
                    {
                        "type": "button",
                        "text": "Report an Issue",
                        "msg": "/report_issue",
                        "msg_in_chat_window": True
                    }
                ]
            }
        ]
    }

    return jsonify(rc_resp)