from dotenv import load_dotenv

from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# model for doing the vector embedding for the user query
# taking the user queya and converting it into vector embedding to do the similarity search in the vector database

openai_client = OpenAI() 

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",   
)

# now we need connection to the vector database to store the vector embeddings
vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning-rag",
    embedding=embeddings_model,
)



def process_query(query:str):
    print(f"Searching chunks for query: {query}")
    search_result = vector_db.similarity_search(query=query)
    context = [f"page_content: {doc.page_content}, page_number: {doc.metadata['page']}" for doc in search_result]
    SYSTEM_PROMPT = f"""
    You are an helpful who answers the user query based on the available context retrieved from a PDF file along with page_content and page number. If you don't know the answer, say you don't know.
    you should only ans the user based in the following context and navigate the user to open the right page number to know more
    context: {context}
    
    """
    response = openai_client.chat.completions.create(
        model="gpt-4",
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
    print(f"response from the model: {response.choices[0].message.content}")
    return response.choices[0].message.content