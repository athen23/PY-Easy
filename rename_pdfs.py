import os
import pandas as pd
import csv

#Folder path for PDF files
folder_path = "C:/Users/phili/Desktop/EasyHealth/Elevance Aduit 5-28/PDFs/wrong"

#EMPI to member ID file
patient_xlsx = "C:/Users/phili/Desktop/EasyHealth/member_bod_lname.xlsx"

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter the list to only include PDF files
pdf_files = [f for f in files if f.lower().endswith(".pdf")]

# Get the Member_Ids, BOD and lname for all patients
df = pd.read_excel(patient_xlsx, header=0)
#print(df.head())

#Get the EMPI for each patient on the pdfs
def extract_EMPI(initial, final):
    results = []
    for x in pdf_files:
        start_index = x.find(initial)
        if start_index == -1:
            results.append("") 
            continue

        start_index += len(initial)
        end_index = x.find(final, start_index)
        if end_index == -1:
            results.append("")
            continue
        
        extracted = x[start_index:end_index]
        results.append(extracted)
    
    return results
    
initial = "care_plan_encounter_tab"
final = "e"
empis = extract_EMPI(initial, final)
empis = [int(x) for x in empis]
#print(empis)

#Lookup for each one of the member id and get the bod and lname
def lookup(lookup_value, lookup_column, return_column1, return_column2, return_column3, df):
    try:
        # Exact match: Filter the dataframe where the lookup column matches the lookup value
        result = df[df[lookup_column] == lookup_value][[return_column1, return_column2, return_column3]]

         # If the result is not empty, return the first match for both columns
        if not result.empty:
            return result.iloc[0][return_column1], result.iloc[0][return_column2], result.iloc[0][return_column3]
        else:
            return None, None
    except KeyError:
        # If the column names are not found in the dataframe
        return None, None

def rename_pdfs(old_filename, last_name, bod, member_id):
    # Loop through the list of PDF files and rename them
        
        #Striping last names due to having empty spaces
        last_name = last_name.strip()        
        # Construct the new file name
        if len(str(bod)) < 8:
            new_name = f"Elevance_{last_name}_0{bod}_{member_id}.pdf"
        else:
            new_name = f"Elevance_{last_name}_{bod}_{member_id}.pdf"

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

lookup_column = 'empi'
return_column3 = 'member_id'
return_column2 = 'birthdate'
return_column1 = 'lname'

for old_filename, emp in zip(pdf_files, empis):
    if empis:  # Ensure the EMPI is not empty
        result = lookup(emp, lookup_column, return_column1, return_column2, return_column3, df)
        #print(result)
        if result:
            new_name_template = result
            rename_pdfs(old_filename, new_name_template[0], new_name_template[1], new_name_template[2])