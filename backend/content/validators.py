def validate_start_guide(data: dict) -> dict:
    start_guide_dict = {
        "Да": True,
        "Нет": False,
    }
    data["start_guide"] = start_guide_dict[data["start_guide"]]
    return data
