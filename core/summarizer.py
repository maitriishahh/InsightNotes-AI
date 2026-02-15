from groq import Groq
from config.settings import GROQ_API_KEY
from core.chunking import chunk_transcript
from utils.rate_limiter import safe_groq_call
import time

client = Groq(api_key=GROQ_API_KEY)

def generate_notes(transcript: str, content_type:str, title:str):
    """
    Multi-stage summarization:
    1. Chunk transcript
    2. Summarize each chunk
    3. Merge summaries
    4. Generate final structured notes
    """
    chunks = chunk_transcript(transcript, chunk_size=4000)
    print(f"Total chunks created: {len(chunks)}")

    chunk_summaries = []

    for i,chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}")
        chunk_prompt = f"""
        Summarize the following transcript section clearly and concisely.
        Focus on key ideas, major points, and important discussions.

        Transcript Section:
        {chunk}
        """

        chunk_response = safe_groq_call(client.chat.completions.create,model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a professional knowledge extraction assistant."
            },
            {
                "role": "user",
                "content": chunk_prompt
            }
        ],
        temperature=0.3
    )

    chunk_summaries.append(
    chunk_response.choices[0].message.content.strip()
    )
    time.sleep(1)
    combined_summary = "\n\n".join(chunk_summaries)

    
    if content_type == "Lecture":
        structure = """
        Generate structured notes with:
        1. Overview
        2. Concepts Explained
        3. Definitions
        4. Examples (if any)
        5. Key Takeaways
        """
    
    elif content_type == "Meeting":
        structure = """
        Generate structured notes with:
        1. Meeting Agenda
        2. Key Discussions
        3. Decisions Made
        4. Action Items (with responsible person if mentioned)
        5. Deadlines (if mentioned)
        """

    elif content_type == "Podcast":
        structure = """
        Generate structured notes with:
        1. Main Themes
        2. Guest Insights
        3. Important Opinions
        4. Memorable Quotes
        5. Key Takeaways
        """

    else:
        structure = """
        Generate structured notes with:
        1. Overview
        2. Major Topics
        3. Important Points
        4. Actionable Insights
        5. Final Takeaways
        """

    prompt = f"""
You are a professional knowledge extraction system.

Your job is to deeply analyze the ENTIRE provided transcript and produce comprehensive, well-structured notes.

STRICT INSTRUCTIONS:
- Cover ALL major topics discussed.
- Ensure coverage of beginning, middle, and end of the transcript.
- Do NOT summarize only the first portion.
- Provide detailed explanations where necessary.
- Do NOT be overly brief.
- Expand on technical concepts if present.
- Use clear headings and bullet points.
- If the transcript appears truncated, clearly state that analysis is based on provided portion only.


Video Title: {title}
Content Type: {content_type}

Based on the following combined summaries from the full transcript,
    generate comprehensive structured notes.

    {structure}

    Combined Summary:
    {combined_summary}
"""

    response = safe_groq_call(client.chat.completions.create,model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a professional knowledge extraction system."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
    )

    return response.choices[0].message.content.strip()

    