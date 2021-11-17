import datetime


def lambda_handler(event, context):
    china_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    if china_now.isoweekday() in range(1, 6) and china_now.time() <= datetime.time(12, 00):
        return True
    else:
        return False
