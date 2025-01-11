import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import os
import environ

# Initialize the environment
env = environ.Env()

# Get the parent directory of the current script
parent_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(parent_dir)  # Move one level up

# Build the path to the .env file in the parent directory
env_file = os.path.join(parent_dir, '.env')

# Load the .env file
environ.Env.read_env(env_file)

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)
document_1 = Document(
    page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)
document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

documents = [
    document_1,
    document_2
    #["blue hotdogs", "red flower"]
]
from uuid import uuid4

#uuids = [str(uuid4()) for _ in range(len(documents))]
#print(uuids)
vector_store.add_documents(documents=documents)

results = vector_store.similarity_search(
    "tell me about breakfast",
    k=2,
    #filter={"source": "tweet"},
)
for res in results:
    #print(f"* {res.page_content} [{res.metadata}] [{res.id}]")
    print(res)

