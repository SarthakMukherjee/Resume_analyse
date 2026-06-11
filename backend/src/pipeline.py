from src.loader import load_resume, load_JD
from src.chunking import chunk_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store
from src.retriever import get_retriever, retrieve_docs
from src.llm import get_llm, generate_response


# # Global Initialization
# embedding_model = get_embedding_model()
# llm = get_llm()

# # ==================================================

# # Main Pipeline

# def run_pipeline(resume_path, job_path):

#     # document loader
#     resume_docs = load_resume(resume_path)
#     job_docs = load_JD(job_path)

#     # chunking
#     resume_chunks = chunk_documents(resume_docs)
#     job_chunks = chunk_documents(job_docs)

#     # vector store
#     vectorstore = create_vector_store(job_chunks, embedding_model)

#     # retriever
#     retriever = get_retriever(vectorstore)

#     # resume text 
#     resume_text = " ".join([doc.page_content for doc in resume_chunks])

#     # retrieve relevant job info
#     retrieved_docs = retrieve_docs(retriever, resume_text)

    
#     response = generate_response(llm, resume_text, retrieved_docs)
#     return response

# #lazy loading
# embedding_model = None
# llm = None

# def get_models():
#     global embedding_model, llm

#     if embedding_model is None:
#         print("Loading embedding model....")
#         embedding_model = get_embedding_model()

#     if llm is None:
#         print("Loading LLM....")
#         llm = get_llm()

#     return embedding_model, llm

# def run_pipeline(resume_path, job_path):
    
#     # Load models only once (lazy)
#     embedding_model, llm = get_models()

#     # document loader
#     resume_docs = load_resume(resume_path)
#     job_docs = load_JD(job_path)

#     # chunking
#     resume_chunks = chunk_documents(resume_docs)
#     job_chunks = chunk_documents(job_docs)

#     # vector store (per request correct)
#     vectorstore = create_vector_store(job_chunks, embedding_model)

#     # retriever
#     retriever = get_retriever(vectorstore)

#     # resume text 
#     resume_text = " ".join([doc.page_content for doc in resume_chunks])

#     # retrieve relevant job info
#     retrieved_docs = retrieve_docs(retriever, resume_text)

#     # LLM
#     response = generate_response(llm, resume_text, retrieved_docs)
#     return response


def run_pipeline(resume_path, job_path):

    # document loader
    resume_docs = load_resume(resume_path)
    job_docs = load_JD(job_path)

    # chunking
    resume_chunks = chunk_documents(resume_docs)
    job_chunks = chunk_documents(job_docs)

    # embeddings (still local, but lightweight)
    embedding_model = get_embedding_model()

    # vector store
    vectorstore = create_vector_store(job_chunks, embedding_model)

    # retriever
    retriever = get_retriever(vectorstore)

    # resume text 
    resume_text = " ".join([doc.page_content for doc in resume_chunks])

    # retrieve relevant job info
    retrieved_docs = retrieve_docs(retriever, resume_text)

    # LLM via API (fast)
    llm = get_llm()
    response = generate_response(llm, resume_text, retrieved_docs)

    return response