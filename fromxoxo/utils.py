from datetime import timedelta, datetime


def time_before(time):
    delta = datetime.now() - time
    if delta.total_seconds() < 300:
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


def time_expire(time, expire_duration):
    interval_hours = expire_duration - round((datetime.now() - time) / timedelta(hours=1))
    if interval_hours <= 0:
        return '1시간'
    days, hours = divmod(interval_hours, 24)
    if days > 0:
        interval = f'{days}일'
    else:
        interval = f'{hours}시간'
    return interval

