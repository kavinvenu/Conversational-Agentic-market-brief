from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # updated import
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import pickle

def build_index(text_path: str, index_path: str = "faiss_index", persist_path: str = "faiss_store.pkl") -> None:
    """
    Build a FAISS vector store index from a raw text file and save it locally.
    
    Args:
        text_path (str): Path to the raw text file.
        index_path (str): Directory path to save the FAISS index files.
        persist_path (str): File path to save the pickled FAISS DB object.
    """
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(raw_text)
        docs = [Document(page_content=t) for t in texts]

        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.from_documents(docs, embedding)

        db.save_local(index_path)
        with open(persist_path, "wb") as f:
            pickle.dump(db, f)
        
        print(f"Index built and saved to {index_path} and {persist_path}")
    except Exception as e:
        print(f"Error building index: {e}")

def get_relevant_chunks(query: str, index_path: str = "faiss_index") -> list[str]:
    """
    Load FAISS index and retrieve relevant text chunks for the query.
    
    Args:
        query (str): User query string.
        index_path (str): Directory path where the FAISS index is stored.
    
    Returns:
        list[str]: List of top-k relevant document chunks.
    """
    try:
        embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        results = db.similarity_search(query, k=3)
        return [res.page_content for res in results]
    except Exception as e:
        print(f"Error loading index or searching: {e}")
        return []

