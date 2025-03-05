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


def query_chromadb(
    query: str, 
    db_path: str = "./database/chromadb_store",
    collection_name: str = "text_chunks",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    top_k: int = 5
) -> List[Dict]:
    """
    Queries the ChromaDB collection for the most relevant text chunks.

    Args:
        query (str): The query text.
        db_path (str, optional): Path for ChromaDB storage. Default is './database/chromadb_store'.
        collection_name (str, optional): Name of the ChromaDB collection. Default is 'text_chunks'.
        embedding_model (str, optional): Embedding model to use. Default is 'all-MiniLM-L6-v2'.
        top_k (int, optional): Number of top results to return. Default is 5.

    Returns:
        List[Dict]: List of the top-k matching documents with metadata.
    """
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Load the embedding model
    model = SentenceTransformer(embedding_model)
    query_embedding = model.encode(query).tolist()

    # Perform the query
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    
    # Format the output
    retrieved_chunks = []
    for i in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "category": results["metadatas"][0][i]["category"],
            "score": results["distances"][0][i]
        })
    
    return retrieved_chunks
