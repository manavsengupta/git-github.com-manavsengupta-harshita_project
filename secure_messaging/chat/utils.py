import hmac
import hashlib
import base64
from django.conf import settings

def generate_hmac(message: str) -> str:
    """Generates an HMAC-SHA256 signature for a given message."""
    secret_bytes = settings.HMAC_SHARED_SECRET.encode('utf-8')
    message_bytes = message.encode('utf-8')
    
    # Create the HMAC using SHA-256
    signature = hmac.new(secret_bytes, message_bytes, hashlib.sha256).digest()
    
    # Return it as a base64 encoded string for easy storage
    return base64.b64encode(signature).decode('utf-8')

def verify_hmac(message: str, provided_signature: str) -> bool:
    """Verifies if the provided signature matches the message."""
    expected_signature = generate_hmac(message)
    # Use compare_digest to prevent timing attacks
    return hmac.compare_digest(expected_signature, provided_signature)