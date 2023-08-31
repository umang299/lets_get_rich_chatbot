import os
import re
import json
from datetime import datetime



def save_json(dictionary):
    dst_path = os.path.join("conversation", f"{dictionary['id']}.json")
    with open(dst_path, 'w') as f:
        json.dump(dictionary, f)


def load_conversation():
    data_list = []
    for filename in os.listdir("conversation"):
        if filename.endswith(".json"):
            file_path = os.path.join("conversation", filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                data_list.append(data)

    
    data_list.sort(key=lambda x: datetime.strptime(x["timestamp"], "%a %b %d %H:%M:%S %Y"), reverse=False)

    output_string = ""
    for data in data_list:
        output_string += f"{data['entity']} : {data['message'].strip()} \n"

    return output_string

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def preprocess_sentence(text):
    text = re.sub(r'\d', '', text)
    text = text.strip()
    return text