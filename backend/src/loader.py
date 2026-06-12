from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, Docx2txtLoader

from pathlib import Path

def load_JD(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    return documents

# def load_resume(file_path):
#     loader = PyMuPDFLoader(file_path)
#     documents = loader.load()
#     return documents

def load_resume(file_path):
    extension=Path(file_path).suffix.lower()

    if extension==".pdf":
        loader=PyMuPDFLoader(file_path)

    elif extension==".docx":
        loader=Docx2txtLoader(file_path)

    else:
        raise ValueError(f"Unsupported resume format: {extension}. Supported are .pdf and .docx only.")
    
    return loader.load()


