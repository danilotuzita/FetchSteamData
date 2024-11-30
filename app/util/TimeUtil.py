from datetime import datetime as dt


@staticmethod
def minutes_to_hours(playtime: int) -> str:
    return '"{:02d}h{:02d}m"'.format(*divmod(playtime, 60))


@staticmethod
def unixtime_to_localtime_str(unixtime: int) -> str:
    return dt.fromtimestamp(unixtime).strftime('"%d/%m/%Y %H:%M:%S"')


@staticmethod
def unixtime_to_localtime(unixtime: int) -> dt:
    return dt.fromtimestamp(unixtime)
