import logging
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

def log_action(user, action, details=None, metadata=None):
    """
    Log user actions for auditing.
    """
    log_data = {
        "action": action,
        "user_id": getattr(user, 'id', None),
        "username": getattr(user, 'username', 'anonymous'),
        "details": details,
        "metadata": metadata
    }
    
    logger.info(
        "Action Log",
        extra={'log_data': log_data}
    )