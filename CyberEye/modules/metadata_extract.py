from PyPDF2 import PdfReader
from docx import Document
from colorama import Fore, Style

def extract_metadata(path):
    print(f"\nExtracting metadata from: {path}\n")
    try:
        if path.lower().endswith('.pdf'):
            reader = PdfReader(path)
            meta = reader.metadata
            if meta:
                for k, v in meta.items():
                    print(f"{k}: {v}")
            else:
                print("No metadata found in PDF.")
        elif path.lower().endswith('.docx'):
            doc = Document(path)
            core = doc.core_properties
            print("Author:", core.author)
            print("Title:", core.title)
            print("Created:", core.created)
            print("Last modified by:", core.last_modified_by)
        else:
            print("Unsupported file type. Use PDF or DOCX.")
    except FileNotFoundError:
        print("File not found. Provide a correct path.")
    except Exception as e:
        print("Error reading metadata:", e)
