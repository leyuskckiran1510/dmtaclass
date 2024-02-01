import re
import time
import datetime
import typing
import logging
from typing import Dict, Callable

pattrens: Dict[re.Pattern, str] = {
    re.compile(r"\d{1,2}", re.IGNORECASE): "%d",
    re.compile(r"\d{4}(.)\d{1,2}", re.IGNORECASE): "%Y{0}%m",
    re.compile(r"\d{4}(.)\d{1,2}\1\d{1,2}", re.IGNORECASE): "%Y{0}%m{0}%d",
    re.compile(r"\d{1,2}(.)\d{4}\1\d{1,2}", re.IGNORECASE): "%d{0}%Y{0}%m",
    re.compile(r"\d{1,2}(.)\d{1,2}\1\d{4}", re.IGNORECASE): "%m{0}%d{0}%Y",
}

DATE_EXCEEDE = False


def parse_annotation(annoted: type):
    if isinstance(annoted, typing._UnionGenericAlias):  # type:ignore
        all_args = []
        for of in annoted.__args__:
            if isinstance(of, typing._LiteralGenericAlias):  # type:ignore
                all_args.extend(of.__dict__.get("__args__"))
        return all_args
    return []


def find_date_format(dateLike: str) -> str:
    dateLike = dateLike.strip()
    for pattren, _format in pattrens.items():
        if _mtch := pattren.fullmatch(dateLike):
            if "{0}" in _format:
                return _format.format(_mtch.groups()[0])
            else:
                return _format
    return "%d"


def date_limit(_: str, annoted: type):
    global DATE_EXCEEDE
    ofs = parse_annotation(annoted=annoted)
    for of in ofs:
        _d = None
        try:
            _format = find_date_format(of)
            _d = datetime.datetime.strptime(of, _format)
            if datetime.datetime.today() > _d:
                DATE_EXCEEDE = True
        except Exception as e:
            # print(e)
            logging.info("Datetime format is worng. Read Docs")

def extract_float(ofs:list):
    for i in ofs:
        try:
            return float(i)
        except:
            continue
    return 0

def time_to_sleep(var: str, annoted: type):
    ofs = parse_annotation(annoted=annoted)
    factor = 1
    factor_map = {"s": 1, "h": 60 * 60, "m": 60, "d": 60 * 60 * 24}
    if ofs and DATE_EXCEEDE:
        for key,fact in factor_map.items():
            if var.endswith(key):
                factor = fact
        delay = extract_float(ofs)
        # print("Sleeping For",factor*delay,delay)
        time.sleep(factor*delay)

RULES: Dict[str, Callable[[str, type], None]] = {
    "d": date_limit,
    "t": time_to_sleep,
}


def choose_function(cls):
    rules = RULES.copy()
    properties = vars(cls).get("__annotations__")
    if not properties:
        return
    for key, value in properties.items():
        for rule, func in rules.items():
            if rule in key:
                func(key, value)
                rules.pop(rule)
                break
