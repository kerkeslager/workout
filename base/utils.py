import datetime

def round_to_nearest(n, nearest):
    assert isinstance(nearest, int)
    return nearest * round(n / nearest)

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)
