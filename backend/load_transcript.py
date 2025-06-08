from vector_db import chroma_client, collection, embedder

sample_text = """
Today the team discussed the login bug and planned the upcoming sprint. 
We assigned John to resolve the issue by Friday. Sarah will update the sprint backlog.
Deployment is scheduled for next Monday.
"""

def split_text(text, chunk_size=30):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

chunks = split_text(sample_text)
embeddings = embedder.encode(chunks)

collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=[{"source": "Sample Meeting"} for _ in chunks],
    ids=[f"chunk-{i}" for i in range(len(chunks))]
)

print("✅ Sample transcript added.")
