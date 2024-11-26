import re
import glob
import os
import pandas as pd

# Path to the subfolder containing the .H files
folder_path = 'generated_h_files'

# Get a list of all .H files in the subfolder
file_paths = glob.glob(os.path.join(folder_path, '*.H'))

# List to store the extracted data
tool_data = []

# Iterate over each .H file in the subfolder
for file_path in file_paths:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        # Check if the line contains "TOOL CALL"
        if 'TOOL CALL' in line:
            # Split the line at the semicolon to separate the comment
            parts = line.strip().split(';')
            # Extract the tool call part
            tool_call_part = parts[0]
            # Extract the comment part if it exists
            comment_part = parts[1].strip() if len(parts) > 1 else ''
            # Extract the tool number using regex
            tool_call_match = re.search(r'TOOL CALL\s+(\d+)', tool_call_part)
            if tool_call_match:
                tool_number = int(tool_call_match.group(1))
                # Extract the description and tool ID from the comment part
                # Assuming the format is "Description - Tool ID"
                description = ''
                tool_id = ''
                if comment_part:
                    # Split the comment part at ' - ' to separate description and tool ID
                    comment_parts = comment_part.split(' - ')
                    description = comment_parts[0].strip()
                    if len(comment_parts) > 1:
                        tool_id = comment_parts[1].strip()
                # Append the data to the list
                tool_data.append({
                    'Tool Number': tool_number,
                    'Description': description,
                    'Tool ID': tool_id
                })

# Create a DataFrame from the list
df = pd.DataFrame(tool_data)

# Save the DataFrame to an Excel file
output_file = 'tool_data.xlsx'
df.to_excel(output_file, index=False)

print(f"Data has been successfully extracted and saved to '{output_file}'.")
