import os

def get_file_content(working_directory: str, file_path: str) -> str:

	result = get_file_info(file)
	if "Error" in result:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	if os.path.isfile(file_path):
		return f'Error: File not found or is not a regular file: "{file_path}"'
	
