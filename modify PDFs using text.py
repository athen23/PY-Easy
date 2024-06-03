import fitz  # PyMuPDF
import os
import shutil

# Directory containing the PDFs
dir_path = "C:/Users/phili/Desktop/EasyHealth/PDFs/Other clients/wrong/"

# Coordinates of the area to replace text (left, bottom, right, top)
x_left = 238.55859375
y_bottom = 269.166748046875
x_right = 270.7375793457031
y_top = 280.5699157714844

# Adjustment factor for y-coordinate
y_adjustment = 5  # Adjust this value based on your needs

#Font for the new text
font_path = "C:/Users/phili/Desktop/EasyHealth/PDFs/times.ttf"
font_name='TimesNewRoman'

# Function to process each PDF
def process_pdf(pdf_path):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        print(f"Processing {pdf_path}")
        
        # Iterate through pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Search for the first term
            text_instances_term1 = page.search_for("Televisit")
            # Search for the second term
            text_instances_term2 = page.search_for("In Home")
            # Combine the results
            text_instances = text_instances_term1 + text_instances_term2
            #print(text_instances)
            #print(f"Found {len(text_instances)} instances of 'oldText' on page {page_num}")

            # Loop through found instances
            for inst in text_instances:
                #print(f"Found instance at {inst}")
                # Check if the instance is within the specified area
                if (inst[0] >= x_left and inst[1] >= y_bottom and inst[2] <= x_right and inst[3] <= y_top):
                    #print(f"Instance {inst} is within the specified area.")
                    # Create a redaction annotation
                    page.add_redact_annot(inst, fill=(1, 1, 1))  # white color to cover old text

            # Apply redactions
            page.apply_redactions()
            for inst in text_instances:
                if (inst[0] >= x_left and inst[1] >= y_bottom and inst[2] <= x_right and inst[3] <= y_top):
                    new_y_position = inst[1] + y_adjustment
                    #print(f"Inserting new text at {(inst[0], new_y_position)}")
                    # Insert new text with y-coordinate adjustment and line break
                    new_text ="Audio/Visual Modality: Telehealth Visit provided via real-time interactive"
                    # Insert the first line with normal fontsize and the second line with a smaller fontsize
                    page.insert_text((inst[0], new_y_position), new_text, fontsize=9, fontname=font_name, fontfile=font_path, color=(0, 0, 0))
                    # Reduce the font size for the second line to reduce spacing
                    page.insert_text((inst[0], new_y_position + 8), "audio and video session", fontsize=9, fontname=font_name, fontfile=font_path, color=(0, 0, 0))

        # Save the modified PDF to a new file
        new_pdf_path = pdf_path.replace(".pdf", "_modified.pdf")
        doc.save(new_pdf_path)
        doc.close()
        print(f"Processed {pdf_path} and saved as {new_pdf_path}")

        # Optionally, replace the original file with the modified one
        shutil.move(new_pdf_path, pdf_path)
        #print(f"Replaced original file with modified file: {pdf_path}")

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")


# Get list of PDF files in the directory
pdf_files = [f for f in os.listdir(dir_path) if f.endswith(".pdf")]

for pdf_file in pdf_files:
    pdf_path = os.path.join(dir_path, pdf_file)
    process_pdf(pdf_path)
