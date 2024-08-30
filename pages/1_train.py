import streamlit as st
from rasa.model_training import train_nlu
import yaml
import base64
import os
import shutil

st.title("Rasa Intent Classification Trainer")

def format_nlu_yaml(data):
    yaml_lines = [f"version: \"{data['version']}\"", "nlu:"]
    for item in data['nlu']:
        intent_line = f"- intent: {item['intent']}"
        yaml_lines.append(intent_line)
        yaml_lines.append("  examples: |")
        for example in item['examples'].split('\n'):
            if example.strip():
                yaml_lines.append(f"    {example.strip()}")
        yaml_lines.append("")  # Add an empty line after each intent
    return "\n".join(yaml_lines)

def parse_nlu_yaml(yaml_str):
    lines = yaml_str.split('\n')
    data = {'version': lines[0].split('"')[1], 'nlu': []}
    current_intent = None
    current_examples = []

    for line in lines[2:]:  # Skip "version:" and "nlu:"
        if line.startswith('-'):
            if current_intent:
                data['nlu'].append({'intent': current_intent, 'examples': '\n'.join(current_examples)})
                current_examples = []
            current_intent = line.split()[2]
        elif line.strip() and not line.startswith('examples:'):
            current_examples.append(line.strip())

    if current_intent:
        data['nlu'].append({'intent': current_intent, 'examples': '\n'.join(current_examples)})

    return data

def load_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            yaml_content = yaml.safe_load(content)
            formatted_content = format_nlu_yaml(yaml_content)
            return yaml_content, formatted_content
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None, None

def save_yaml(file_path, content):
    try:
        formatted_content = format_nlu_yaml(content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_content)
        return True
    except Exception as e:
        st.error(f"Error saving YAML file: {str(e)}")
        return False

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">현재 파일 다운로드</a>'
    return href

def train_model(training_data, config, model_path):
    # Delete previous model
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
        st.info("Previous model deleted.")

    # Train new model
    train_nlu(
        nlu_data=training_data,
        config=config,
        output=model_path
    )
    return model_path

# Fixed values for config and model path
config = "./config.yml"
model_path = "./models"
training_data_path = "./data/nlu.yml"

# File uploader
uploaded_file = st.file_uploader("Choose a YAML file", type="yml")
if uploaded_file is not None:
    try:
        yaml_content = yaml.safe_load(uploaded_file)
        formatted_yaml = format_nlu_yaml(yaml_content)
        st.success("File uploaded successfully!")
    except yaml.YAMLError as e:
        st.error(f"Error parsing uploaded YAML: {e}")

# Save YAML button
if st.button("Save YAML"):
    try:
        edited_yaml_content = yaml.safe_load(formatted_yaml)
        if save_yaml(training_data_path, edited_yaml_content):
            st.success("YAML content saved successfully!")
            yaml_content = edited_yaml_content
    except yaml.YAMLError as e:
        st.error(f"Error parsing edited YAML: {e}")

# Train button
if st.button("Train Model"):
    with st.spinner("Training in progress..."):
        try:
            trained_model_path = train_model(training_data_path, config, model_path)
            st.success(f"Model trained successfully! Saved at: {trained_model_path}")

            # Save the model path to a file for the execution page to use
            with open("model_path.txt", "w") as f:
                f.write(trained_model_path)
        except Exception as e:
            st.error(f"An error occurred during training: {str(e)}")

st.write("After training, go to the execution page to test the model.")