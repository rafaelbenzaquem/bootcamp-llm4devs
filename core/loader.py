from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document


def loadPdf(file) -> list[Document]:
    loader = PyPDFLoader(file)
    return loader.load_and_split()


def loadPdfsDirectory(dir) -> list[Document]:
    loader = PyPDFDirectoryLoader(dir)
    docs = loader.load()
    return docs
