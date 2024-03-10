import re


def telegram_validator(tg_acc):
    """
    Производит валидацию телеграмм акканта возвращая чистый username.
    При валдиации удаляет @ / t.me/ https://
    """
    if "@" or "t.me/" or "https://t.me/" in tg_acc:
        tg_acc = re.sub(r"@|t.me\/|https\/\/t.me\/", "", tg_acc)
    return tg_acc


def gender_validator(gender):
    """
    Валидатор поля гендера для запросов с Яндекс формы.
    Превращает русские М / Ж в Male / Female.
    """
    genders = {"М": "Male", "Ж": "Female"}
    return genders.get(gender)


def tg_acc_validator(data):
    tg_acc = data.get("tg_acc")
    if "@" or "t.me/" or "https//t.me/" in tg_acc:
        tg_acc = re.sub(r"@|t.me\/|https\/\/t.me\/", "", tg_acc)
    data["tg_acc"] = tg_acc
    return data
