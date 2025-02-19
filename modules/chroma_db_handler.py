import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

def store_chunks_in_chromadb(
    chunks: List[Dict], 
    db_path: str = "./database/chromadb_store",
    collection_name: str = "text_chunks",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
) -> None:
    """
    Stores text chunks into a ChromaDB collection with embeddings.

    Args:
        chunks (List[Dict]): List of text chunks.
        db_path (str, optional): Path for ChromaDB storage. Default is './text_chromadb'.
        collection_name (str, optional): Name of the ChromaDB collection. Default is 'text_chunks'.
        embedding_model (str, optional): Embedding model to use. Default is 'all-MiniLM-L6-v2'.

    Returns:
        None
    """

    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Load the embedding model
    model = SentenceTransformer(embedding_model)

    # Store each chunk in ChromaDB
    for chunk in chunks:
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[chunk["id"]],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{"category": chunk["category"]}]
        )

    print(f"✅ Successfully stored {len(chunks)} chunks in ChromaDB!")
