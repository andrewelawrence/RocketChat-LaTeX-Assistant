# utils.py
import os, json, re, time, hashlib
from config import get_logger
from datetime import datetime
from llmproxy import upload, pdf_upload, text_upload

_LOGGER = get_logger(__name__)
_HASH = hashlib.sha1()
_UID_RE = re.compile(r'^[A-Za-z0-9]+$')
_USERS = os.environ.get("users")
_SIDS = os.environ.get("sids")
_INTERACTIONS = os.environ.get("interactionsDir")
_GLOBAL_UPLOADS = os.environ.get("globalUploadsDir")
_USER_UPLOADS = os.environ.get("userUploadsDir")

def _safe_json_load(filepath : str) -> dict:
    """Safely load JSON; return empty structure if file not found or invalid."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        _LOGGER.error(f"[FILE SYSTEM] Could not load JSON from {filepath}: {e}", exc_info=True)
        return {}
    
def _safe_json_save(filepath : str, data : dict) -> bool:
    """Safely save JSON."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            
        return True 
    except Exception as e:
        _LOGGER.error(f"[FILE SYSTEM] Could not save JSON to {filepath}: {e}", exc_info=True)
        return False
    
def _gen_sid() -> str:
    """Generate a hashed SID from the epoch time (or any other scheme)."""
    _HASH.update(str(time.time()).encode('utf-8'))
    return f"sid-{_HASH.hexdigest()[:10]}"

def _get_sid(uid: str, user: str = "UnknownName") -> str:
    """
    Determine if the UID is already tied to a SID.
    If not, try to use a free SID or create a new one.
    Returns the SID string.
    """

    sids  = _safe_json_load(_SIDS)
    users = _safe_json_load(_USERS)
    
    sid = None
    
    # User already exists and has SID
    if uid in sids:
        sid = sids[uid]
        _LOGGER.info(f"User <{uid}> has existing SID <{sid}>")
    # New user
    else:
        if "free" in sids:
            sid = sids["free"]
            sids[uid] = sid
            del sids["free"]
            _LOGGER.info(f"Assigned existing free SID <{sid}> to user <{uid}>")
        else:
            # No 'free' key found, create a new SID for the user
            # (This case should never happen as a new SID is always generated below)
            sid = _gen_sid()
            sids[uid] = sid
            _LOGGER.info(f"No free SID found. Created new SID <{sid}> for user <{uid}>")
        # Log new user info in users.json
        users[uid] = {
            "sid": sid,
            "user": user,
            "created_at": datetime.utcnow().isoformat()
        }
        _LOGGER.info(f"New user <{uid}> added with SID <{sid}>")    

    free_sid = _gen_sid()
    sids["free"] = free_sid
    _LOGGER.info(f"Reserved new free SID <{free_sid}> for future assignment.")
    
    _safe_json_save(_SIDS, sids)
    _safe_json_save(_USERS, users)
    
    return sid    

def _validate(vValue, vName : str = "unknown", vType : type = str, 
              vValueDefault = None,
              log_level = _LOGGER.warning) -> bool:
    """
    Verify that 'value' is an instance of 'desired_type'.
    If not, log a message at 'log_level' and return 'default_value'.
    Otherwise, return 'value'.
    """
    if not isinstance(vValue, vType):
        _LOGGER.log(
            log_level,
            f"Received non-{vType.__name__} for {vName}: {vValue}"
        )
        return vValueDefault

def _store_interaction(data: dict, user: str, uid: str, 
                       sid: str, msg: str) -> bool:
    """
    Saves the data payload to a file in:
      _INTERACTIONS/<uid>/<user>-YYYY-MM-DDTHH:MM:SS.MSMSMS.json
    """
    try:
        timestamp = data.get("timestamp", "UnknownTimestamp")
        interaction = {
                "user": user,
                "uid": uid,
                "sid": sid,
                "mid": data.get("message_id", "UnknownMessageID"),
                "cid": data.get("channel_id", "UnknownChannelID"),
                "timestamp": timestamp,
                "token": data.get("token", None),
                "bot": data.get("bot", False),
                "url": data.get("siteUrl", None),
                "msg": msg
            }
        
        fname = f"{user}-{timestamp}.json"
        fp = os.path.join(_INTERACTIONS, uid, fname)
        
        _safe_json_save(fp, interaction)
        _LOGGER.info(f"Conversation history saved to {fp}")
        return True
    
    except Exception as e:
        _LOGGER.error(f"Failed to save conversation history: {e}", exc_info=True)
        return False   

def upload(sid : str) -> bool:
    """Upload any file type"""
    return False

def extract(data : dict) -> tuple:
    """"""
    if not isinstance(data, dict):
        _LOGGER.warning("extract() called with non-dict data.")
        return ("UnknownUserID", "UnknownUserName", "")
    
    # Extract USER info
    uid  = data.get("user_id", "UnknownUserID")
    user = data.get("user_name", "UnknownUserName")
    msg  = data.get("text", "")
    
    uid  = _validate(uid, "uid", str, "UnknownUserID", _LOGGER.warning)
    user = _validate(user, "user", str, "UnknownUserName", _LOGGER.warning)
    msg  = _validate(msg, "msg", str, "", _LOGGER.warning)
    
    # Keep an eye out for suspect UIDs
    if not _UID_RE.match(uid):
        _LOGGER.warning(f"Potentially invalid characters in user_id: {uid}")

    # Get/create SID
    sid = _get_sid(uid, user)

    # Store conversation to database
    _store_interaction(data, user, uid, sid, msg)

    return (user, uid, sid, msg)
