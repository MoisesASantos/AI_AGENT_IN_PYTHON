import os
from dotenv import load_dotenv
from google import genai
import argparse


def main():
	parser = argparse.ArgumentParser(description="ChatBot")
	parser.add_argument("user_prompt", type=str, help="user prompt")
	arg = parser.parse_args()
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	if api_key is None:
		raise RunTimeError("Not found a API KEY for the model")
	client = genai.Client(api_key=api_key)
	response = client.models.generate_content(
		model="gemini-2.5-flash",
		contents=arg.user_prompt
	)
	if response.usage_metadata is None:
		raise RunTimeError("API request fail, try again") 
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
	print(response.text)


if __name__ == "__main__":
    main()
