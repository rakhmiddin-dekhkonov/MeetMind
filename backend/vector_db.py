import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Use PersistentClient now
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="meeting_transcripts")


# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def query_chunks(question, n_results=5):
    embedding = embedder.encode([question])
    results = collection.query(query_embeddings=embedding, n_results=n_results)
    documents = results['documents'][0] if results['documents'] else []
    return documents
