import os
from config import MAX_FILE_READ

def get_file_content(working_directory, file_path):
            
    try:

        working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir, file_path))

        if not os.path.commonpath([working_dir, target_file]) == working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file, 'r') as f:
            file_text = f.read(MAX_FILE_READ)
            file_truncated = f.read(1) is not None

        return file_text + f' [...File {file_path} truncated at {MAX_FILE_READ} characters]' if file_truncated else None
    
    except Exception as e:
        return f'Error: {e}'