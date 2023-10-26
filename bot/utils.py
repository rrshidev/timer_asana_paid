import json
from datetime import timedelta
from typing import Tuple


# using:
# d = Dict(
#   first="hello"
# )
# d.second = 5
# print(d.first, d.second)
class Dict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__getitem__


def callback(data):
    d = json.dumps(data)
    print("SIZE", len(d.encode("utf-8")))
    return d


def get_callback(callback_data):
    return json.loads(callback_data)


def get_redis_entry(user_id: int, practice: str) -> str:
    return f"{user_id}_{practice}"


def get_time_str(minutes: int = 0, seconds: int = 0) -> str:
    time_value = get_time(minutes=minutes, seconds=seconds)
    return ":".join(str(time_value).split(":")[1:])


def get_time(minutes: int = 0, seconds: int = 0) -> timedelta:
    return timedelta(
        minutes=minutes,
        seconds=seconds,
    )


def str_to_time(input: str) -> timedelta:
    parts = input.split(":")

    return get_time(
        minutes=int(parts[0]),
        seconds=int(parts[1]) if len(parts) > 1 else 0,
    )
