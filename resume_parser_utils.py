import spacy
import re
from PyPDF2 import PdfReader
from docx import Document
import os

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {"NAME": None, "EMAIL": None, "PHONE": None, "SKILLS": []}

    # Name
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["NAME"]:
            entities["NAME"] = ent.text

    # Email
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    if email_match:
        entities["EMAIL"] = email_match.group()

    # Phone
    phone_match = re.search(r"\b(\+91[\-\s]?)?[6-9]\d{9}\b", text)
    if phone_match:
        entities["PHONE"] = phone_match.group()

    # Skills
    skills_list = ["Python", "Java", "SQL", "C++", "HTML", "CSS", "Machine Learning"]
    for skill in skills_list:
        # Escape special characters to prevent regex error
        skill_pattern = re.escape(skill)
        if re.search(rf"\b{skill_pattern}\b", text, re.IGNORECASE):
            entities["SKILLS"].append(skill)

    return entities

def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    return text
