import dotenv
import pinecone
from uuid import uuid4
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings

env_var = dotenv.dotenv_values(".env")

class Assistant:
    def __init__(self, openai_api, pinecone_api, top_k):
        self.top_n = top_k
        self.openai_api = openai_api
        self.pinecone_api = pinecone_api


    def __load_embedding_model(self):
        model = OpenAIEmbeddings(model="text-embedding-ada-002", 
                                 openai_api_key=self.openai_api)
        return model


    def __load_pinecone_index(self):
        pinecone.init(api_key=self.pinecone_api,
                      environment="us-east1-gcp")
        
        index = pinecone.Index(index_name="doc-qa-rdpd")
        return index
    
    def __summarizer_model(self):
        model = OpenAI(model="text-davinci-002",
                       openai_api_key=self.openai_api)
        
        return model
    
    def __query_from_db(self, message_emb):
        index = self.__load_pinecone_index()
        db_respose = index.query(vector=message_emb, top_k=self.top_n)['matches']
        vector_ids = [resp['id'] for resp in db_respose]
        text = [index.fetch([i])['vectors'][i]['metadata']['text'] for i in vector_ids]
        text = " ".join(text)
        return text
    
    def __load_prompt(self, message):
        with open("prompts\summarizer.txt") as f:
            text = f.read().lower()

        text = text.replace("\n", " ")
        prompt = text.replace("<<text>>", message)
        return prompt
        
    
    def get_response(self, message):
        emb_model = self.__load_embedding_model()
        message_emb = emb_model.embed_query(text=message)

        text = self.__query_from_db(message_emb=message_emb)
        prompt = self.__load_prompt(message=text)
        
        llm = self.__summarizer_model()
        response = llm(prompt)
        return response
    

if __name__ == "__main__":
    assistant = Assistant(openai_api=env_var['OPENAI_API_KEY'], 
                          pinecone_api=env_var['PINECONE_API_KEY'],
                          top_k=50)
    user = str(input("USER:"))
    response = assistant.get_response(user)
    print(response)