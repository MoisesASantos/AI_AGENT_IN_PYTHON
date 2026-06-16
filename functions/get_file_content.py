import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        if not abs_file_path.startswith(abs_working_dir):
            return (
                f'Error: Cannot read "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if not os.path.isfile(abs_file_path):
            return (
                f'Error: File not found or is not a regular file: '
                f'"{file_path}"'
            )

        with open(abs_file_path, "r") as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated '
                    f'at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"
