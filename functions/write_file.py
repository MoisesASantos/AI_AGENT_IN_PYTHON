import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file relative to the working directory, creating directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write to, relative to working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        if not abs_file_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot write to "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if os.path.isdir(abs_file_path):
            return (
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )

        os.makedirs(
            os.path.dirname(abs_file_path),
            exist_ok=True,
        )

        with open(abs_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
