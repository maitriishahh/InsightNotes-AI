from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key = GROQ_API_KEY)

def classify_content(transcript: str):
    """
    Classify transcript into one of:
    Lecture, Meeting, Podcast, General Video
    """

    prompt = f"""
You are a professional content classification system.

Your task is to classify the transcript into EXACTLY ONE of the following categories based on STRUCTURE, not tone.

Categories:

1. Lecture
- Structured instructional or educational format
- Focused on explaining concepts, frameworks, or step-by-step learning
- Often includes definitions, examples, or teaching progression
- Typically one main speaker presenting material to an audience

2. Meeting
- Business or team discussion
- Multiple participants interacting
- Agenda, decisions, tasks, responsibilities, or deadlines mentioned
- Back-and-forth collaboration format

3. Podcast
- Requires clear multi-speaker interaction
- Transcript must show conversational back-and-forth
- Must include speaker turns, questions and responses, or interview dialogue
- If transcript reads like a continuous monologue, it is NOT a Podcast

4. General
- Single-speaker informational content
- Commentary, business advice, trends, announcements
- Marketing, trailers, corporate presentations
- News-style monologue
- Any content that does not clearly match Lecture, Meeting, or Podcast

Classification Rules:
- Focus on format and interaction structure.
- Do NOT classify based purely on topic.
- Teaching format = Lecture.
- Multi-speaker collaboration = Meeting.
- Multi-speaker conversational discussion = Podcast.
- Single-speaker informational or opinion content = General.
- If multiple conditions partially apply, choose the most structurally dominant format.

Respond with ONLY ONE word:
Lecture
Meeting
Podcast
General

Transcript:
{transcript[:4000]}
"""


    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a classification assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

    return response.choices[0].message.content.strip()
