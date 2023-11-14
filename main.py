import dotenv
from assistant import Assistant

import warnings


warnings.filterwarnings("ignore")
env_var = dotenv.dotenv_values(".env")
assistant = Assistant(openai_api=env_var['OPENAI_API_KEY'], 
                      pinecone_api=env_var['PINECONE_API_KEY'])
    
if __name__ == "__main__":
    while True:
        msg = str(input("USER: "))
        response, sources = assistant.response(query=msg)
        print(f"ASSISTANT: {response}\nSources: {sources}")