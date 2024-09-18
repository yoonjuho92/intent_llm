import json

def load_intent_entities():
    try:
        with open('intent_entities.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dict if the file doesn't exist

def save_intent_entities(intent_entities):
    with open('intent_entities.json', 'w', encoding='utf-8') as f:
        json.dump(intent_entities, f, ensure_ascii=False, indent=4)