from datetime import datetime

from django.http import HttpResponseForbidden


def time_before(time):
    delta = datetime.now() - time
    if delta.total_seconds() < 60:
        return '방금전'
    elif delta.total_seconds() < 3600:
        minutes = round(delta.total_seconds() / 60)
        return f'{minutes}분 전'
    elif delta.total_seconds() < 86400:
        hours = round(delta.total_seconds() / 3600)
        return f'{hours}시간 전'
    elif delta.total_seconds() < 2592000:
        days = round(delta.total_seconds() / 86400)
        return f'{days}일 전'
    else:
        months = round(delta.total_seconds() / 2592000)
        return f'{months}달 전'


def time_after(time, limit):
    interval = datetime.now() - time
    delta = limit - interval
    if delta.total_seconds() < 300:
        return '잠시 후'
    elif delta.total_seconds() < 3600:
        minutes = round(delta.total_seconds() / 60)
        return f'{minutes}분 후'
    elif delta.total_seconds() < 86400:
        hours = round(delta.total_seconds() / 3600)
        return f'{hours}시간 후'
    elif delta.total_seconds() < 2592000:
        days = round(delta.total_seconds() / 86400)
        return f'{days}일 후'
    else:
        months = round(delta.total_seconds() / 2592000)
        return f'{months}달 후'


