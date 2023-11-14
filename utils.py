import os
import re
import json
from uuid import uuid4
from datetime import datetime



def logger(message, role):
    payload = {
            'Id' : str(uuid4()),
            'Role' : role,
            'Timestamp' : datetime.isoformat(datetime.now()),
            'Message' : message}
    
    dst_path = os.path.join("conversation", f"{payload['Id']}.json")
    with open(dst_path, 'w') as f:
        json.dump(payload, f)


def load_conversation(top_n):
    data_list = []
    for filename in os.listdir("conversation"):
        if filename.endswith(".json"):
            file_path = os.path.join("conversation", filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                data_list.append(data)

    
    data_list.sort(key=lambda x: datetime.strptime(x["Timestamp"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=False)


    output_string = ""
    for data in data_list[:top_n*2]:
        output_string += f"{data['Role']} : {data['Message'].strip()} \n"

    return output_string

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def preprocess_sentence(text):
    text = re.sub(r'\d', '', text)
    text = text.strip()
    return text