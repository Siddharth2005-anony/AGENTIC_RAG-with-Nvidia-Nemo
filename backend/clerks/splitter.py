def split_document(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Simple text splitting by characters with overlap."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
        if start >= len(text):
            break
    return chunks