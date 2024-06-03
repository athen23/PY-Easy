import fitz  # PyMuPDF
import os

# Define the dimensions of A4 size in points (1 point = 1/72 inch)
c_WIDTH = 612
c_HEIGHT = 792

def resize_pdf(input_path, output_path):
    # Check if the output file already exists and remove it to avoid conflicts
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except PermissionError:
            print(f"Error: The file '{output_path}' is currently open or locked. Please close it and try again.")
            return

    # Open the input PDF
    document = fitz.open(input_path)

    # Create a new PDF for the output
    new_document = fitz.open()

    # Iterate through each page
    for page_num in range(len(document)):
        original_page = document[page_num]
        
        # Create a new A4 page
        new_page = new_document.new_page(width=c_WIDTH, height=c_HEIGHT)

        # Get the original page size
        rect = original_page.rect
        original_width = rect.width
        original_height = rect.height
        #print(f"Page {page_num + 1}: Width = {original_width} points, Height = {original_height} points")

        # Calculate the scale factor to fit the original content into A4 size
        scale_factor = min(c_WIDTH / original_width, c_HEIGHT / original_height)

        # Calculate the position to center the original content on the new A4 page
        new_width = original_width * scale_factor
        new_height = original_height * scale_factor
        x_offset = (c_WIDTH - new_width) / 2
        y_offset = (c_HEIGHT - new_height) / 2

        # Define the position to place the original page content
        rect = fitz.Rect(x_offset, y_offset, x_offset + new_width, y_offset + new_height)

        # Insert the original page into the new page
        new_page.show_pdf_page(rect, document, page_num)

    # Save the new document to the output file
    new_document.save(output_path)
    print(f"PDF saved successfully to '{output_path}'.")

def pdf_size(pdf_path):
    # Open the input PDF
    document = fitz.open(pdf_path)

    # Iterate through each page and print its size
    for page_num in range(len(document)):
        page = document[page_num]
        rect = page.rect  # Get the rectangle representing the page size
        width = rect.width
        height = rect.height
        print(f"Page {page_num + 1}: Width = {width} points, Height = {height} points")

def process_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all PDF files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            print(f"Processing '{input_path}'...")
            resize_pdf(input_path, output_path)
            #pdf_size(output_path)

# Example usage
input_folder = "C:/Users/phili/Desktop/EasyHealth/Resizing PDFs/wrong/Elevance Notes Batch 2/"
output_folder = "C:/Users/phili/Desktop/EasyHealth/Resizing PDFs/correct/Elevance Notes Batch 2/"
process_folder(input_folder, output_folder)
