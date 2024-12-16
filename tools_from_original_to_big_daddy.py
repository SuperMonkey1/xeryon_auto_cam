import re
import glob
import os
import pandas as pd

# Path to the subfolder containing the original .H files
input_folder = 'generated_h_files'

# Path to the folder where modified .H files will be saved
output_folder = 'generated_h_files_big_daddy_a'

# Ensure the output folder exists; create it if it doesn't
os.makedirs(output_folder, exist_ok=True)

# Path to the Excel file with the tool mappings
excel_file = 'tool_tables.xlsx'

# Load the Excel file into a DataFrame
df = pd.read_excel(excel_file)

# Build a mapping from original tool numbers to 'Tool Numbers Big Daddy'
# Assuming the columns are 'Tool Number' and 'Tool Numbers Big Daddy'
tool_number_mapping = dict(zip(df['Tool Number'], df['Tool Numbers Big Daddy']))

# Get a list of all .H files in the input folder
file_paths = glob.glob(os.path.join(input_folder, '*.H'))

# Iterate over each .H file in the input folder
for file_path in file_paths:
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Function to replace tool numbers in TOOL CALL statements
    def replace_tool_number(match):
        original_tool_number = int(match.group(1))
        if original_tool_number in tool_number_mapping:
            new_tool_number = tool_number_mapping[original_tool_number]
            return f'TOOL CALL {new_tool_number}'
        else:
            # If the tool number is not in the mapping, keep it unchanged
            return match.group(0)
    
    # Use regex to find and replace TOOL CALL statements
    content_modified = re.sub(r'TOOL CALL\s+(\d+)', replace_tool_number, content)
    
    # Write the modified content to a new file in the output folder
    # Preserve the original filename
    filename = os.path.basename(file_path)
    output_file_path = os.path.join(output_folder, filename)
    
    with open(output_file_path, 'w') as file:
        file.write(content_modified)

print(f"Tool numbers have been updated and modified files saved to '{output_folder}'.")
