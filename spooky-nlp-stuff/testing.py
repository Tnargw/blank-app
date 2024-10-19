import spacy
from transformers import pipeline
import streamlit as st

# Read text from file
with open("lecture.txt", "r") as file:
    transcript = file.read()

# Display text input in the app
st.title("Professor Parser")
text_input = st.text_area("Lecture Transcription", transcript, height=200)

if st.button("Extract"):
    # spaCy for NER
    nlp_spacy = spacy.load("en_core_web_sm")
    doc = nlp_spacy(text_input)
    
    # Extracting entities using spaCy and filtering out numerical entities
    spacy_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ not in ["CARDINAL", "QUANTITY", "PERCENT"]]
    
    # Transformers for NER
    nlp_transformers = pipeline("ner")
    result = nlp_transformers(text_input)
    
    # Extracting entities using transformers and filtering out numerical entities
    transformers_entities = [(item['word'], item['entity']) for item in result if item['entity'] not in ["CARDINAL", "QUANTITY", "PERCENT"]]
    
    # Combine and display all entities
    all_entities = spacy_entities + transformers_entities
    st.write(all_entities)
