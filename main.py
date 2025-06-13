import pdfplumber
import docx2txt
import os
from resume_parser_utils import extract_entities


def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def read_docx(file_path):
    return docx2txt.process(file_path)

def main():
    folder = "sample"
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if file.endswith(".pdf"):
            text = read_pdf(path)
        elif file.endswith(".docx"):
            text = read_docx(path)
        else:
            continue

        print(f"\nParsing: {file}")
        result = extract_entities(text)
        print(result)

if __name__ == "__main__":
    main()
