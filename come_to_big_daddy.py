import subprocess
import time
import os
import shutil

# Step 1: Run the 'tools_used.py' script
print("Running 'tools_from_original_to_big_daddy.py'...")
tools_used_process = subprocess.run(['python', 'tools_from_original_to_big_daddy.py'])

# Check if 'tools_used.py' ran successfully
if tools_used_process.returncode != 0:
    print("Error: 'tools_used.py' did not complete successfully.")
    exit(1)

# Step 2: Run the 'adjust_tap_pitches.py' script
print("Running 'adjust_tap_pitches.py'...")
adjust_tap_pitches_process = subprocess.run(['python', 'adjust_tap_pitches.py'])

# Check if 'adjust_tap_pitches.py' ran successfully
if adjust_tap_pitches_process.returncode != 0:
    print("Error: 'adjust_tap_pitches.py' did not complete successfully.")
    exit(1)

print("Both scripts have been executed successfully.")


# Step 3: Remove the folder 'generated_h_files_big_daddy_a' and all its files
folder_to_remove = 'generated_h_files_big_daddy_a'

# Check if the folder exists
if os.path.exists(folder_to_remove):
    print(f"Removing the folder '{folder_to_remove}' and all its contents...")
    try:
        shutil.rmtree(folder_to_remove)
        print(f"Folder '{folder_to_remove}' has been removed successfully.")
    except Exception as e:
        print(f"Error: Could not remove the folder '{folder_to_remove}'. {e}")
        exit(1)
else:
    print(f"Folder '{folder_to_remove}' does not exist. Skipping removal.")
