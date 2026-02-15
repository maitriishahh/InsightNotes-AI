import streamlit as st
import re
import os

from core.input_handler import download_yt_audio, extract_video_id
from core.audio_extractor import extract_audio
from core.transcriber import transcribe_audio
from core.classifier import classify_content
from core.summarizer import generate_notes
from database.models import create_tables
from database.crud import save_notes, get_all_notes, get_note_by_id
#from rag.search import build_index
from rag.search import add_video_to_index
from rag.search import query_index
from utils.pdf_export import export_notes_to_pdf
from utils.helpers import extract_video_id

create_tables()
#build_index()

st.set_page_config(page_title="Deep Dive Notes Tracker", layout="wide")

st.title("Deep Dive Video Notes Tracker")

tab1, tab2,tab3 = st.tabs(["📥 Process Video", "📂 Saved Notes","🔎 Ask Knowledge Base"])
    
with tab1:
    st.header("Process New Video / Audio")

    input_mode = st.radio(
        "Choose Input Type",
        ["YouTube URL", "Upload Audio/Video File"]
    )

    url = None
    uploaded_file = None

    if input_mode == "YouTube URL":
        url = st.text_input("Enter YouTube URL")

    elif input_mode == "Upload Audio/Video File":
        uploaded_file = st.file_uploader(
            "Upload Audio or Video",
            type = ["mp3","mp4","wav"]
        )

    if st.button("Generate Notes"):

        if input_mode == "YouTube URL":

            if not url or url.strip() == "":
                st.warning("Please enter a valid YouTube URL.")
                st.stop()

            with st.spinner("Downloading audio..."):
                audio_path, title = download_yt_audio(url)

            if not audio_path:
                st.error("Failed to download audio from YouTube.")
                st.stop()

            youtube_id = extract_video_id(url)


        else:

            if not uploaded_file:
                st.warning("Please upload an audio/video file.")
                st.stop()

            os.makedirs("storage/audio", exist_ok=True)

            file_path = f"storage/audio/{uploaded_file.name}"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            title = uploaded_file.name
            youtube_id = None

            # If video file → extract audio
            if file_path.endswith(".mp4"):
                with st.spinner("Extracting audio..."):
                    audio_path = extract_audio(file_path)
            else:
                audio_path = file_path



        with st.spinner("Transcribing..."):
            transcript, duration = transcribe_audio(audio_path)

        with st.spinner("Classifying content..."):
            content_type = classify_content(transcript)

        with st.spinner("Generating structured notes..."):
            notes = generate_notes(transcript, content_type, title)

        note_id = save_notes(
            title,
            content_type,
            duration,
            transcript,
            notes,
            youtube_id
        )

        add_video_to_index(note_id)

        st.success("Notes generated and saved successfully!")
        st.divider()

        st.subheader(title)
        st.write(f"**Type:** {content_type}")
        st.write(f"**Duration:** {duration // 60} min {duration % 60} sec")
        st.divider()

        st.markdown(notes)

        with st.expander("📜 View Transcript"):
            st.text(transcript[:5000])
                  


with tab2:
    st.header("Saved Notes")

    saved_notes = get_all_notes()

    if not saved_notes:
        st.info("No saved notes yet.")
        st.stop()

    youtube_notes = []
    audio_notes = []
    video_notes = []

    for note in saved_notes:
        note_id = note[0]
        title = note[1]

        full_note = get_note_by_id(note_id)
        youtube_id = full_note[4]

        if youtube_id:
            youtube_notes.append((title, note_id))
        else:
            if title.lower().endswith((".mp3", ".wav")):
                audio_notes.append((title, note_id))
            elif title.lower().endswith(".mp4"):
                video_notes.append((title, note_id))
            else:
                audio_notes.append((title, note_id))  # fallback


    category = st.radio(
        "Filter by Source",
        ["🎥 YouTube", "🎵 Audio Uploads", "🎬 Video Uploads"],
        horizontal=True
    )

    if category == "🎥 YouTube":
        selected_list = youtube_notes
    elif category == "🎵 Audio Uploads":
        selected_list = audio_notes
    else:
        selected_list = video_notes

    if not selected_list:
        st.info("No notes in this category.")
        st.stop()

   
    note_dict = {title: note_id for title, note_id in selected_list}
    selected_note = st.selectbox(
        "Select a note",
        ["-- Select --"] + list(note_dict.keys())
    )

    if selected_note == "-- Select --":
        st.stop()

    note_id = note_dict[selected_note]
    full_note = get_note_by_id(note_id)

    if full_note:
        title = full_note[0]
        content_type = full_note[1]
        transcript = full_note[2]
        structured_notes = full_note[3]
        youtube_id = full_note[4]

        st.divider()
        st.subheader(title)
        st.write(f"**Type:** {content_type}")

       
        if youtube_id:
            youtube_link = f"https://www.youtube.com/watch?v={youtube_id}"
            st.markdown(f"[▶ Watch on YouTube]({youtube_link})")

        st.divider()
        st.markdown(structured_notes)

       
        if st.button("📄 Export as PDF", key=f"export_{note_id}"):

            os.makedirs("storage/exports", exist_ok=True)

            safe_title = title[:30].replace(" ", "_").replace("/", "_")
            pdf_path = f"storage/exports/{safe_title}.pdf"

            export_notes_to_pdf(title, structured_notes, pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇ Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    key=f"download_{note_id}",
                    use_container_width=True
                )



with tab3:
    st.header("Ask Across All Saved Videos")

    question = st.text_input("Ask a question about your saved videos")

    if st.button("Search Knowledge Base"):

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching knowledge base..."):
                answer,sources = query_index(question)

            st.divider()
            st.subheader("Answer")
            st.markdown(answer)

            with st.expander("Sources Used"):
                if sources:
                    unique_titles = list(set([r["title"] for r in sources]))
                    for title in unique_titles:
                        st.write(f"- {title}")
                else:
                    st.write("No sources retrieved.")
