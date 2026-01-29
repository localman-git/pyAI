import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file with the arguments provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="the arguments to pass into the specified python file",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            )
        },
    ),
)

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