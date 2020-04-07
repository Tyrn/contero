"""Helpers and utilities unrelated to Kivy.
"""
import re
import random
from functools import partial


random.seed()


MAC_MAX = 0xFF_FF_FF_FF_FF_FF


def mac_to_int(mac):
    res = re.match("^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$", mac.lower())
    if res is None:
        raise ValueError("invalid mac address")
    return int(res.group(0).replace(":", ""), 16)


def int_to_mac(macint):
    if type(macint) != int:
        raise ValueError("invalid integer")
    return ":".join([f"{a}{b}" for a, b in zip(*[iter(f"{macint:012x}")] * 2)])


def rand_mac():
    v = partial(random.getrandbits, 8)
    return f"{v():02x}:{v():02x}:{v():02x}:{v():02x}:{v():02x}:{v():02x}"
