import os

def rename_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    for filename in files:
        # Check if the file starts with "segment_" and has a number
        if filename.startswith("segment_") and any(char.isdigit() for char in filename):
            # Extract the numeric part of the filename
            prefix, number = filename.split("_")
            number, wav = number.split(".")
            # Format the number with leading zeros
            formatted_number = "{:02d}".format(int(number))
            
            # Construct the new filename
            new_filename = f"{prefix}_{formatted_number}.wav"
            
            # Rename the file
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            print(f"Renamed: {filename} -> {new_filename}")

# Specify the path to the folder containing the files
folder_path = "Audio/segments_5/"

# Call the function to rename files in the specified folder
rename_files(folder_path)

folder_path = "Audio/segments_10/"

# Call the function to rename files in the specified folder
rename_files(folder_path)