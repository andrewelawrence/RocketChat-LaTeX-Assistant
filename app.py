from flask import Flask, request, jsonify
from config import get_logger
from utils import extract, upload
from chat import welcome, query

_LOGGER = get_logger(__name__)
_LOGGER.info("Application started")

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def main():
    # Enforce only JSON requests
    if not request.is_json:
        _LOGGER.warning("[SECURITY] Non-JSON request blocked.")
        return jsonify({"error": "Invalid content type"}), 400
    
    data = request.get_json() 
    
    # Extract relevant information
    # (Extract also does some very important cataloguing.)
    user, uid, new, sid, msg = extract(data)

    # Do not respond to bots
    if data.get("bot") or not msg:
        return jsonify({"status": "ignored"})
        
    if new:
        return welcome(uid, user)
    else:
        return query(msg, sid)

@app.route('/commands', methods=['POST'])
def handle_commands():
    # Enforce only JSON requests
    if not request.is_json:
        _LOGGER.warning("[SECURITY] Non-JSON request blocked.")
        return jsonify({"error": "Invalid content type"}), 400
    
    data = request.get_json() 
    _LOGGER.info(data)
    
    # Simple information extract
    command = data.get("command")
    uid = data.get("user_id")
    user = data.get("user_name")

    if command == "/show_sources":
        # sources = user_sources.get(user_id, ["No sources available."])
        # return jsonify({"text": f"Here are the sources used:\n- " + "\n- ".join(sources)})
        return jsonify({"text": "Feature in development."})

    elif command == "/upload_document":
        return jsonify({"text": "Feature in development."})
        # return jsonify({"text": "Please upload your document(s) as an attachment in the chat. The bot will process it automatically."})

    elif command == "/report_issue":
        return jsonify({"text": f"To report an issue, please message @andrew.lawrence directly."})

    return jsonify({"text": "Unknown command."})

@app.route('/')
def hello_world():
   return jsonify({"message":'There is nothing on this page. Please return to where you came from!'})

@app.errorhandler(404)
def page_not_found(e):
    return "Error 404: Page Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)
    