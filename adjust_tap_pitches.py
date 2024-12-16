import os
import glob

# Input and output folders
input_folder = 'generated_h_files_big_daddy_a'
output_folder = 'generated_h_files_big_daddy'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Mapping of TAP M sizes to replacement lines
tap_mapping = {
    'TAP M1.6': '       Q239=+0.35 ;SPOED ~',
    'TAP M2 ': '        Q239=+0.4 ;SPOED ~',
    'TAP M2.5': '       Q239=+0.45 ;SPOED ~',
    'TAP M3 ': '        Q239=+0.5 ;SPOED ~',
}

# Get list of .H files in the input folder
file_paths = glob.glob(os.path.join(input_folder, '*.H'))

# Process each file
for file_path in file_paths:
    # Read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize index
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if the line contains any of the TAP M strings
        for tap_text, replacement_line in tap_mapping.items():
            if tap_text in line:
                # Found a TAP M line, now find the next line starting with Q239
                j = i + 1
                while j < len(lines):
                    if lines[j].strip().startswith('Q239'):
                        # Replace the line with the replacement line
                        lines[j] = replacement_line + '\n'
                        # Stop searching for Q239
                        break
                    j += 1
                # Since there might be multiple occurrences, we continue
                # After handling one TAP M occurrence, continue from next line
                break  # Break out of the for loop over tap_mapping
        i += 1  # Move to the next line

    # Write the modified lines to the output folder
    output_file_path = os.path.join(output_folder, os.path.basename(file_path))
    with open(output_file_path, 'w') as file:
        file.writelines(lines)

print(f"Processing complete. Modified files are saved in '{output_folder}'.")
