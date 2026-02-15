from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text:str):
    """
    Generate embedding using local SentenceTransformer
    """
    model = load_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()