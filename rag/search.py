from database.crud import get_all_notes, get_note_by_id
from core.chunking import chunk_transcript
from rag.embeddings import get_embedding
from rag.vector_store import VectorStore
from groq import Groq
from config.settings import GROQ_API_KEY
from utils.rate_limiter import safe_groq_call

client = Groq(api_key=GROQ_API_KEY)

def build_index():
    """
    Build FAISS index from all saved transcripts.
    """

    all_notes = get_all_notes()
    

    # Get embedding dimension once
    test_embedding = get_embedding("dimension test")
    dimension = len(test_embedding)

    vector_store = VectorStore(dimension)

    for note in all_notes:
        note_id = note[0]
        title = note[1]

        full_note = get_note_by_id(note_id)

        if not full_note:
            continue

        transcript = full_note[2]

        chunks = chunk_transcript(transcript, chunk_size=4000)

        

        for chunk in chunks:
            embedding = get_embedding(chunk)

            metadata = {
                "video_id": note_id,
                "title": title,
                "text": chunk
            }

            vector_store.add(embedding, metadata)

    vector_store.save()
    


def query_index(question: str, top_k: int = 6):
    """
    Search FAISS index and generate grounded answer using Groq.
    Includes relevance threshold filtering to prevent hallucination.
    """

    # Load vector store
    test_embedding = get_embedding("dimension test")
    dimension = len(test_embedding)
    vector_store = VectorStore(dimension)

    # Embed question
    question_embedding = get_embedding(question)

    # Retrieve similar chunks
    distances, results = vector_store.search(question_embedding, top_k=top_k)

    if not results:
        return "No relevant information found in the knowledge base."

    # ---------------------------
    # Relevance Threshold Filtering
    # ---------------------------
    RELEVANCE_THRESHOLD = 1.2  # Tune if needed

    filtered_results = []

    for dist, res in zip(distances, results):
        if dist < RELEVANCE_THRESHOLD:
            filtered_results.append(res)

    if not filtered_results:
        return "No relevant information found in the knowledge base.",[]

    # ---------------------------
    # Build Context
    # ---------------------------
    context = "\n\n".join(
        [f"From '{r['title']}':\n{r['text'][:1500]}" for r in filtered_results]
    )

    # ---------------------------
    # Strict Grounded Prompt
    # ---------------------------
    prompt = f"""
You are a grounded knowledge assistant.

Answer the question using ONLY the provided context.

Important Rules:
- If the topic is not explicitly mentioned in the context, say:
  "No relevant information found in the knowledge base."
- Do NOT reinterpret unrelated content.
- Do NOT use outside knowledge.
- Do NOT invent frameworks, ideas, or summaries.
- Always mention the source video title when presenting information.
- If comparing videos, clearly explain differences using only retrieved context.
- If synthesizing across videos, integrate insights carefully and accurately.

Answer clearly and directly.
Do not repeat the question.
Do not include meta-instructions.
Do not fabricate missing information.

Question:
{question}

Context:
{context}
"""

    response = safe_groq_call(
        client.chat.completions.create,
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a precise and grounded intelligent knowledge  assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2  # Lower = less creative = safer
    )

    return response.choices[0].message.content.strip(), filtered_results



def add_video_to_index(note_id):
    from database.crud import get_note_by_id

    # Get single note
    full_note = get_note_by_id(note_id)

    if not full_note:
        return

    transcript = full_note[2]
    title = full_note[0]

    # Get embedding dimension once
    test_embedding = get_embedding("dimension test")
    dimension = len(test_embedding)

    vector_store = VectorStore(dimension)

    chunks = chunk_transcript(transcript, chunk_size=4000)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        metadata = {
            "video_id": note_id,
            "title": title,
            "text": chunk
        }

        vector_store.add(embedding, metadata)

    vector_store.save()
