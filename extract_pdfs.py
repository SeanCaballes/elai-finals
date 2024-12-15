import os
import PyPDF2

EXTRACTED_TEXT_FOLDER = 'extracted_text'
PDF_FOLDER = 'pdf_files'

# Ensure the extracted text folder exists
if not os.path.exists(EXTRACTED_TEXT_FOLDER):
    os.makedirs(EXTRACTED_TEXT_FOLDER)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        print(f"Extracted text from {pdf_path}:")
        print(text)  # Print the extracted text for debugging
        return text

def save_extracted_text(pdf_path, extracted_text):
    # Save the extracted text to a .txt file
    filename = os.path.basename(pdf_path).replace('.pdf', '.txt')
    with open(os.path.join(EXTRACTED_TEXT_FOLDER, filename), 'w', encoding='utf-8') as file:
        file.write(extracted_text)

def clean_text(text):
    # Normalize text by removing extra spaces, line breaks, etc.
    cleaned_text = ' '.join(text.split())  # Removes extra spaces and newlines
    return cleaned_text.lower()  # Convert to lowercase for case-insensitive search

# Extract and save text from PDFs
for pdf_filename in os.listdir(PDF_FOLDER):
    if pdf_filename.endswith('.pdf'):
        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
        extracted_text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(extracted_text)  # Clean and normalize text
        save_extracted_text(pdf_path, cleaned_text)
