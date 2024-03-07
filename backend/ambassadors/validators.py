import re


def telegram_validator(data):
    tg_acc = data.get("tg_acc")
    if "@" or "t.me/" or "https//t.me/" in tg_acc:
        tg_acc = re.sub(r"@|t.me\/|https\/\/t.me\/", "", tg_acc)
    return tg_acc


def tg_acc_validator(data):
    tg_acc = data.get("tg_acc")
    if "@" or "t.me/" or "https//t.me/" in tg_acc:
        tg_acc = re.sub(r"@|t.me\/|https\/\/t.me\/", "", tg_acc)
    data["tg_acc"] = tg_acc
    return data
