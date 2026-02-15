def chunk_transcript(transcript:str, chunk_size: int=4000):
    """
    Splits transcript into character based chunks.
    Returns list of transcript chunks.
    """
    chunks=[]
    start = 0
    length = len(transcript)

    while start < length:
        end = start + chunk_size
        chunk = transcript[start:end]
        chunks.append(chunk)
        start = end
    return chunks