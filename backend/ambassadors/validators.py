import re


def gender_validator(data: dict) -> dict:
    """
    Валидатор поля гендера для запросов с Яндекс формы.
    Превращает русские М / Ж в Male / Female.
    """
    genders = {"М": "Male", "Ж": "Female"}
    if data["gender"] in genders.keys():
        data["gender"] = genders.get(data["gender"])
    return data


def tg_acc_validator(data: dict) -> dict:
    """
    Производит валидацию телеграмм акканта возвращая чистый username.
    При валдиации удаляет @ / t.me/ https://
    """
    tg_acc = data.get("tg_acc")
    if "@" or "t.me/" or "https//t.me/" in tg_acc:
        tg_acc = re.sub(r"@|t.me\/|https\/\/t.me\/", "", tg_acc)
    data["tg_acc"] = tg_acc
    return data
