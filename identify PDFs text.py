import fitz  # PyMuPDF
import os
import shutil

# Directory containing the PDFs
dir_path = "C:/Users/phili/Desktop/EasyHealth/PDFs/Scan/"

# Function to process each PDF
def process_pdf(pdf_path):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Iterate through pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Search for the first term
            text_instances = page.search_for("Susan Suares")
            #print(text_instances)
            if len(text_instances) > 0:
                print(f"Processing {pdf_path}")
                print(f"Found {len(text_instances)} instances of 'oldText' on page {page_num}")
            else:
                continue

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")


# Get list of PDF files in the directory
pdf_files = [f for f in os.listdir(dir_path) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(dir_path, pdf_file)
    process_pdf(pdf_path)
