def clean_text(text: str) -> str:
    """Simple text cleaning - just normalize whitespace."""
    import re
    text = text.replace("\t", " ")
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

