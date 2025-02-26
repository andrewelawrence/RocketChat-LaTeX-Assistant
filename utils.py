# utils.py
import os, json, re, time, hashlib, boto3
from config import get_logger
from datetime import datetime
from llmproxy import upload, pdf_upload, text_upload

_LOGGER = get_logger(__name__)
_HASH = hashlib.sha1()

_BOTO3_SESSION = boto3.Session(
   aws_access_key_id=os.environ.get("awsAccessKey"),
   aws_secret_access_key=os.environ.get("awsSecretKey"),
   region_name=os.environ.get("awsRegion")
)
_S3_BUCKET = _BOTO3_SESSION.client("s3")
_DYNAMO_DB = _BOTO3_SESSION.resource("dynamodb")
_TABLE = _DYNAMO_DB.Table(os.environ.get("dynamoTable"))

_UID_RE = re.compile(r'^[A-Za-z0-9]+$')
_USERS = os.environ.get("users")
_SIDS = os.environ.get("sids")
_INTERACTIONS = os.environ.get("interactionsDir")

_GLOBAL_UPLOADS = os.environ.get("globalUploadsDir")
_USER_UPLOADS = os.environ.get("userUploadsDir")

# def _safe_json_load(filepath : str) -> dict:
#     """Safely load JSON; return empty structure if file not found or invalid."""
#     if not os.path.exists(filepath):
#         return {}
#     try:
#         with open(filepath, "r") as f:
#             return json.load(f)
#     except Exception as e:
#         _LOGGER.error(f"[FILE SYSTEM] Could not load JSON from {filepath}: {e}", exc_info=True)
#         return {}
    
# def _safe_json_save(filepath : str, data : dict) -> bool:
#     """Safely save JSON."""
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     try:
#         with open(filepath, "w") as f:
#             json.dump(data, f, indent=2)
#         return True 
#     except Exception as e:
#         _LOGGER.error(f"[FILE SYSTEM] Could not save JSON to {filepath}: {e}", exc_info=True)
#         return False
    
def _gen_sid() -> str:
    """Generate a hashed SID from the epoch time (or any other scheme)."""
    _HASH.update(str(time.time()).encode('utf-8'))
    return f"sid-{_HASH.hexdigest()[:10]}"

def _new_sid() -> bool:
    try:
        sid = _gen_sid()
        _TABLE.put_item(
            Item={
                "user_id": "free",
                "sid": sid,
                "created_at": datetime.isoformat()
            }
        )
        
        _LOGGER.info(f"Reserved new free SID <{sid}> for future assignment.")    
        return True
    except Exception as e:
        _LOGGER.error(f"Error creating overhead SID in DynamoDB: {e}", exc_info=True)
        return False
        
def _get_sid(uid: str, user: str = "UnknownName") -> tuple:
    """
    Determine if the UID is already tied to a SID. Otherwise, create a new SID.
    """
    sid = None
    
    try:
        # Check if SID already exists in DynamoDB
        resp = _TABLE.get_item(Key={"uid": uid})
        if "Item" in resp:
            sid = resp["Item"]["sid"]
            _LOGGER.info(f"User <{uid}> has existing SID <{sid}>")
            _new_sid()
            return (sid, False)
        
        # If not, the user is new and so we return True for second part of Tuple
        # Check if a "free" SID exists
        resp = _TABLE.get_item(Key={"uid": "free"})
        if "Item" in resp:
            sid = resp["Item"]["sid"]
            _TABLE.delete_item(Key={"uid": "free"})  # Remove old free SID
            _LOGGER.info(f"Assigned existing free SID <{sid}> to user <{uid}>")
        # If not, create a new SID and store it
        else:
            sid = _gen_sid()
            _LOGGER.info(f"No free SID found. Created new SID <{sid}> for user <{uid}>")

        # Store new SID for the user
        _new_sid()
        
        return (sid, True)
        
    except Exception as e:
        _LOGGER.error(f"Error accessing DynamoDB for SID: {e}", exc_info=True)
        return ("", False)

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
    """Stores the data payload in DynamoDB instead of local files."""
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
        
        # Store interaction in DynamoDB
        _TABLE.put_item(Item=interaction)
        _LOGGER.info(f"Conversation history saved for user <{uid}> at {timestamp}")
        return True
        
    except Exception as e:
        _LOGGER.error(f"Failed to save conversation history to DynamoDB: {e}", exc_info=True)
        return False   

def upload(sid : str) -> bool:
    """Upload any file type"""
    return False
# def generate_presigned_url(user_id: str, filename: str, action="get_object") -> str:
#     """Generate a pre-signed URL for secure file access in S3."""

#     try:
#         bucket = os.getenv("S3_BUCKET_NAME")
#         s3_key = f"uploads/users/{user_id}/{filename}"

#         url = _S3_BUCKET.generate_presigned_url(
#             action,
#             Params={"Bucket": bucket, "Key": s3_key},
#             ExpiresIn=3600  # Link expires in 1 hour
#         )
#         return url

#     except Exception as e:
#         _LOGGER.error(f"Failed to generate presigned URL: {e}", exc_info=True)
#         return None
# def upload_file_to_s3(file_path: str, user_id: str, filename: str) -> str:
#     """Uploads a file to S3 under the user's directory and returns the S3 URL."""

#     try:
#         bucket = os.getenv("S3_BUCKET_NAME")
#         s3_key = f"uploads/users/{user_id}/{filename}"

#         _S3_BUCKET.upload_file(file_path, bucket, s3_key)
        
#         s3_url = f"https://{bucket}.s3.amazonaws.com/{s3_key}"
#         _LOGGER.info(f"File uploaded to {s3_url}")
#         return s3_url

#     except Exception as e:
#         _LOGGER.error(f"File upload failed: {e}", exc_info=True)
#         return None

def extract(data : dict) -> tuple:
    """Extract user information and store conversation to DynamoDB."""
    
    if not isinstance(data, dict):
        _LOGGER.warning("extract() called with non-dict data.")
        return ("UnknownUserID", "UnknownUserName", "")
    
    uid  = data.get("user_id", "UnknownUserID")
    user = data.get("user_name", "UnknownUserName")
    msg  = data.get("text", "")
    
    uid  = _validate(uid, "uid", str, "UnknownUserID", _LOGGER.warning)
    user = _validate(user, "user", str, "UnknownUserName", _LOGGER.warning)
    msg  = _validate(msg, "msg", str, "", _LOGGER.warning)
    
    # if not _UID_RE.match(uid):
    #     _LOGGER.warning(f"Potentially invalid characters in user_id: {uid}")

    # Fetch/create SID from DynamoDB
    sid, new = _get_sid(uid, user)

    # Store conversation in DynamoDB
    _store_interaction(data, user, uid, sid, msg)

    return (user, uid, new, sid, msg)
