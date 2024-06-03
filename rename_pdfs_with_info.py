import os
import pandas as pd
import csv

#Folder path for PDF files
folder_path = "C:/Users/phili/Desktop/EasyHealth/Alignment/PDFs/wrong/"

#EMPI to member ID file
patient_xlsx = "C:/Users/phili/Desktop/EasyHealth/PDFs/member_bod_lname.xlsx"

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter the list to only include PDF files
pdf_files = [f for f in files if f.lower().endswith(".pdf")]

# Get the Member_Ids, BOD and lname for all patients
df = pd.read_excel(patient_xlsx, header=0)
#print(df.head())

#Getting a list of all the existing member_id
member_id=[file[:-4] for file in pdf_files]
member_id=[int(x) for x in member_id]
#print(member_id)

#Lookup for each one of the member id and get the bod and lname
def lookup(lookup_value, lookup_column, return_column1, return_column2, df):
    try:
        # Exact match: Filter the dataframe where the lookup column matches the lookup value
        result = df[df[lookup_column] == lookup_value][[return_column1, return_column2]]

         # If the result is not empty, return the first match for both columns
        if not result.empty:
            return result.iloc[0][return_column1], result.iloc[0][return_column2]
        else:
            return None, None
    except KeyError:
        # If the column names are not found in the dataframe
        return None, None

def rename_pdfs(old_filename, last_name, bod, member_id):
    # Loop through the list of PDF files and rename them
        # Construct the new file name
        if len(str(bod)) < 8:
            if len(str(member_id)) == 6:
                new_name = f"Health Excel_{last_name}_0{bod}_00000{member_id}.pdf"
            else:
                new_name = f"Health Excel_{last_name}_0{bod}_000{member_id}.pdf"
        else:
            if len(str(member_id)) == 6:
                new_name = f"Health Excel_{last_name}_{bod}_00000{member_id}.pdf"
            else:
                new_name = f"Health Excel_{last_name}_{bod}_000{member_id}.pdf"
        # Create the full old and new file paths
        old_file_path = os.path.join(folder_path, old_filename)
        new_file_path = os.path.join(folder_path, new_name)

        #If the file already exists, don´t do anything
        if os.path.exists(new_file_path):
            print(f"File '{new_name}' already exists. Skipping...")
            return

        # Rename the file
        os.rename(old_file_path, new_file_path)

        #print(f"Renamed '{old_filename}' to '{new_name}'")

lookup_column = 'Member_ID'
return_column2 = 'BOD'
return_column1 = 'lname'

for old_filename, empi in zip(pdf_files, member_id):
    if empi:  # Ensure the EMPI is not empty
        result = lookup(empi, lookup_column, return_column1, return_column2, df)
        if result:
            new_name_template = result
            rename_pdfs(old_filename, new_name_template[0], new_name_template[1], empi)