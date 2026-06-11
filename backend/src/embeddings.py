from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_embedding_model():
    return HuggingFaceBgeEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

# def get_embedding_model():
#     return OpenAIEmbeddings(
#         model = "text-embedding-3-small",
#         api_key=os.getenv('OPENAI_API_KEY')
#     )
