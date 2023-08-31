import dotenv
from uuid import uuid4
from datetime import datetime
from assistant import Assistant

import streamlit as st
from streamlit_chat import message

from utils import save_json

env_var = dotenv.dotenv_values(".env")
assistant = Assistant(openai_api=env_var['OPENAI_API_KEY'], 
                      pinecone_api=env_var['PINECONE_API_KEY'])
    
if __name__ == "__main__":
    msg = str(input("USER: "))
    response = assistant.response(query=msg)
    print(response)