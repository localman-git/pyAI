import os
import subprocess

def run_python_file(working_directory, file_path, args=None):

    try:

        working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir, file_path))

        if not os.path.commonpath([working_dir, target_file]) == working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ['python', target_file]

        if args != None:
            command.extend(args)

        run = subprocess.run(command, cwd=working_dir, text=True, capture_output=True, timeout=30)

        result = ''
        
        if run.returncode != 0:
            result += f'Process exited with code {run.returncode}'
        if len(run.stdout) == 0 and len(run.stderr) == 0:
            result += f'No output produced'
        if len(run.stdout) > 0:
            result += f'STDOUT: {run.stdout}'
        if len(run.stderr) > 0:
            result += f'STDERR: {run.stderr}'
        
        return result

    except Exception as e:
        return f'Error: executing Python file: {e}'