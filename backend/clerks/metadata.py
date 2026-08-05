def generate_metadata(chunks: list[str], filename: str) -> list[dict]:
    """Generate minimal metadata for each chunk."""
    return [
        {"filename": filename, "chunk_index": i, "length": len(chunk)}
        for i, chunk in enumerate(chunks)
    ]