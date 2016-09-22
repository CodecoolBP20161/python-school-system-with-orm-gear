from functools import wraps
from model.Email_log import EmailLog

def log_decorator(function):
    @wraps(function)
    def wrapper(self, log, *args, **kwargs):
        if log:
            EmailLog.create_email_log(*log)
        return function(self, *args, **kwargs)
    return wrapper