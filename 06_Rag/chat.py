from dotenv import load_dotenv

# for the vector openAi vector store we need to import the OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# for the qdrant db
from langchain_qdrant import QdrantVectorStore

# openAi
from openai import OpenAI

load_dotenv();

# this is the client for the openAi
openai_client = OpenAI() 


# to create an vector embeedings for the user query we need to import the OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",   
)

# now we need connection to the vector database to store the vector embeddings
vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning-rag",
    embedding=embeddings_model,
)

# take the query from the user
query = input("Ask SomeThing: ");

# revelant document retrieval from the vector database
search_result = vector_db.similarity_search(query=query)

context = [f"page_content: {doc.page_content}, page_number: {doc.metadata['page']}" for doc in search_result]


# system prompt for the llm
SYSTEM_PROMPT = """
    You are an helpful who answers the user query based on the available context retrieved from a PDF file along with page_content and page number. If you don't know the answer, say you don't know.
    
    you should only ans the user based in the following context and navigate the user to open the right page number to know more
    
    
    constext: {context}
    
"""

response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": query
        }
    ]
)

print(f"Answer: {response.choices[0].message.content}")