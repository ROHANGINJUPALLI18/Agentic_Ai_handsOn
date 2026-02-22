from dotenv import load_dotenv

# this import is for taking path from the file
from pathlib import Path
# to import the file into the python project
from langchain_community.document_loaders import PyPDFLoader
# this import is for the text splitter to split the content into chunks for better processing
from langchain_text_splitters import RecursiveCharacterTextSplitter
# for the vector openAi vector store we need to import the OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
# for the qdrant db
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# to load the pdf file we need to give the path of the file
pdf_path = Path(__file__).parent/"Nodejs.pdf"

# laod this file in the current project
loader = PyPDFLoader(file_path=pdf_path)

# docs give the page by page content from the pdf
docs=loader.load()

# chunning with the langchain
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)

# to create an vector embeedings for the chunks we need to import the OpenAIEmbeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    
)
# this is stores in the qdrant vector store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning-rag",
)

