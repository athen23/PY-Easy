import os
import pandas as pd

# Directory containing the PDFs
dir_path = "C:/Users/phili/Desktop/EasyHealth/Alignment/PDFs/wrong/"

# Get list of PDF files in the directory
pdf_files = [f for f in os.listdir(dir_path) if f.endswith(".pdf")]

# Create a DataFrame from the list of PDF files
df = pd.DataFrame(pdf_files, columns=["PDF Files"])

# Save the DataFrame to an Excel file
excel_path = "C:/Users/phili/Desktop/EasyHealth/Alignment/PDFs/pdf_list.xlsx"
df.to_excel(excel_path, index=False)

# print(f"List of PDF files has been saved to {excel_path}")
