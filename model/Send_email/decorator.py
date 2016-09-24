from functools import wraps
from model.Email_log import EmailLog
from datetime import *


def log_decorator(function):
    @wraps(function)
    def wrapper(self, log, full_name, *args, **kwargs):
        if log:
            EmailLog.create_email_log(log['subject'], log['body'], log['type'],
                                      datetime.utcnow(), full_name, self.recipient)
        return function(self, *args, **kwargs)

    return wrapper
