from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from typing import List, Dict


def load_and_split_text(file_path: str, chunk_size: int = 100, chunk_overlap: int = 20) -> List[Dict]:
    """
    Loads a JSON file containing structured text, splits the text into chunks by word count, and returns structured data.

    Args:
        file_path (str): Path to the JSON file.
        chunk_size (int, optional): Number of words per chunk. Default is 100.
        chunk_overlap (int, optional): Overlapping words between chunks. Default is 20.

    Returns:
        List[Dict]: A list of dictionaries containing chunked text data.
    """
    
    # Load extracted text data
    with open(file_path, "r", encoding="utf-8") as f:
        text_data = json.load(f)

    # Define word count function
    def word_count(text: str) -> int:
        return len(text.split())

    # Initialize LangChain's Text Splitter (Using Word Count)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Now splits by words instead of characters
        chunk_overlap=chunk_overlap,  # Ensures smooth transitions
        length_function=word_count  # Uses word count instead of character count
    )

    # Prepare Chunks
    chunks = []
    for section, content in text_data.items():
        split_chunks = text_splitter.split_text(content)
        for i, chunk in enumerate(split_chunks):
            chunks.append({
                "id": f"{section}_{i}",
                "text": chunk,
                "category": section
            })

    print(f"✅ Successfully split into {len(chunks)} chunks!")
    return chunks
