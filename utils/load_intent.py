import yaml

def load_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading YAML file: {str(e)}")
        return None

# Function to extract intents from YAML content
def extract_intents(yaml_content):
    return [item['intent'] for item in yaml_content['nlu']]