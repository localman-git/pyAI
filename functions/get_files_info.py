import os

def get_files_info(working_directory, directory="."):
    
    try:

        working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir, directory))

        if not os.path.commonpath([working_dir, target_dir]) == working_dir:
            return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_contents = ''
        for file in os.listdir(target_dir):
            file_path = os.path.normpath(os.path.join(target_dir, file))
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            dir_contents += f'- {file}: file_size={file_size} bytes, is_dir={is_dir}\n'

        return dir_contents
    
    except Exception as e:
        return f'Error: {e}'