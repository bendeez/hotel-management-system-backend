from slowapi import Limiter
from slowapi.util import get_remote_address
from admin.app.config import settings

limiter = Limiter(key_func=get_remote_address)
limit = f"{settings.LIMIT_REQUESTS_PER_ENDPOINT}/minute"
