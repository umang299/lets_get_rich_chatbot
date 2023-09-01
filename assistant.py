import os
import dotenv
import pinecone
import tiktoken
from uuid import uuid4

from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils import save_json, read_file

env_var = dotenv.dotenv_values(".env")

class Assistant:
    def __init__(self, openai_api, pinecone_api):
        self.openai_api = openai_api
        self.pinecone_api = pinecone_api
        self.tokenizer = tiktoken.get_encoding('p50k_base')


    def __initialize_pinecone(self):
        pinecone.init(api_key=self.pinecone_api,
                      environment="us-east1-gcp")
        
    def __load_index(self):
        self.__initialize_pinecone()
        index = pinecone.Index(index_name=pinecone.list_indexes()[0])
        return index

    def __load_embedding_model(self):
        model = OpenAIEmbeddings(model="text-embedding-ada-002", 
                                 openai_api_key=self.openai_api)
        return model
    
    def __tiktoken_len(self, text):
        tokens = self.tokenizer.encode(text, 
                                       disallowed_special=()
                                       )
        return len(tokens)

    
    def __text_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, 
                                                       chunk_overlap=20, 
                                                       length_function=self.__tiktoken_len, 
                                                       separators=["."]
                                                       )
        return text_splitter
    
    def __initialize_vector_store(self):
        index = self.__load_index()
        embed = self.__load_embedding_model()
        text_field = 'text'
        vectorstore = Pinecone(index, 
                               embed.embed_query, 
                               text_field
        )
        return vectorstore
    
    def __llm(self):
        llm = ChatOpenAI(openai_api_key=self.openai_api,
                         model_name='gpt-3.5-turbo',
                         temperature=0.0)
        return llm

    
    def upsert(self, data_dir, batch_limit):
        text_splitter = self.__text_splitter()
        index = self.__load_index()
        embed = self.__load_embedding_model()

        batch_limit = 100
        texts = []
        metadatas = []

        for i, filename in enumerate(os.listdir(data_dir)):
            # first get metadata fields for this record
            metadata = {
                'source': filename.split('.')[0]
            }

            record = read_file(file_path=os.path.join('lessons', filename))
            # now we create chunks from the record text
            record_texts = text_splitter.split_text(record)
            # create individual metadata dicts for each chunk
            record_metadatas = [{
                "chunk": j, "text": text, **metadata
            } for j, text in enumerate(record_texts)]
            # append these to current batches
            texts.extend(record_texts)
            metadatas.extend(record_metadatas)
            # if we have reached the batch_limit we can add texts
            if len(texts) >= batch_limit:
                ids = [str(uuid4()) for _ in range(len(texts))]
                embeds = embed.embed_documents(texts)
                index.upsert(vectors=zip(ids, embeds, metadatas))
                texts = []
                metadatas = []

    def chain(self):
        llm = self.__llm()
        vectorstore = self.__initialize_vector_store()
        qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, 
                                                                      chain_type="stuff",
                                                                      retriever=vectorstore.as_retriever())
        return qa_with_sources
    
    def response(self, query):
        chain = self.chain()
        return chain(query)