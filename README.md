# Retreival Augmented Generation System.

## Introduction
Large language models (LLMs) are great at a multitude of language processing tasks, like code generation, reasoning, summarising text and so on. However, these model being trained on data upto a certain time in past, their knowledge is limited. This causes these models to be unable to provide response to queries that are relevant today creating a limitation for users and businesses.<br>
<br>
This is called **hallucination**. Meaning, the LLM is capable of going completely off topic, where the response does not align with the intent in the users query. To solve for this, we can provide the language model a memory storage with all the information we want it to know about.<br>
<br>
Since, we know how good these LLMs are at performing simple natural language processing tasks like summarization and data extraction. They can be provided with context relevant to a particular user search query to provide a more aligned response improving the user experience. This process is called *Retrival Augmentated Generation (RAG)*.

## Technical Details
LLM integration framework: Langchain<br>
Vector Database : Pinecone<br>
Embedding Model: ``text-embedding-ada-001`` (OpenAI)<br>
LLM : ``gpt-3.5-turbo``<br>

## Setup
1. Clone the repository.<br>
</t> ``git clone https://github.com/umang299/lets_get_rich_chatbot.git``

2. Create a .env file with your OpenAI API, Pinecone API<br>
</t> ``OPENAI_API_KEY : <<OPENAI_API_KEY>>``<br>
</t> ``PINECONE_API_KEY: <<PINECONE_API_KEY>>``<br>

3. Install dependencies into virtual environment.<br>
</t>``cd lets_get_rich_chatbot`` <br>
</t>``pip install -r requirements.txt``<br>

4. For the sake of simplicity I have used chapters from the book rich dad poor dad. You can find all the chapter wise text under lessons.<br>
</t>Run the following command to insert data into the pinecone index you have created. Make sure to create pinecone index with dimensions as *1536*.
</t>``assistant = Assistant(openai_api_key= openai_api, pinecone_api_key= pinecone_api)``<br>
<t>``assistant.upsert(data_dir='lessons', batch_limit= 100)``<br>

5. Now you are all set to interact with the book using this assistant.
</t> run ``python main.py``