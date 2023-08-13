import json


def read_json(path:str="data/messages.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        return data


def update_json_dict(new_dict: dict, path: str = "data/messages.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.update(new_dict)

    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)