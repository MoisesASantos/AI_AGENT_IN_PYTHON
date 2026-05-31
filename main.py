import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
	#ler o prompt apartir do command line
	parser = argparse.ArgumentParser(description="ChatBot")
	parser.add_argument("user_prompt", type=str, help="user prompt")
	args = parser.parse_args()
	#carregar as var de ambiente apartir do .env
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	if api_key is None:
		raise RunTimeError("Not found a API KEY for the model")
	#criar o cliente que vai conversar com o modelo de IA, nesse caso um objecto
	client = genai.Client(api_key=api_key)
	#conversa persistente com a IA, entendo histórico e contexto
	messages: list[types.Content] = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])] 
	response = client.models.generate_content(
		model="gemini-2.5-flash",
		contents=messages
	)
	if response.usage_metadata is None:
		raise RunTimeError("API request fail, try again") 
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
	print(response.text)


if __name__ == "__main__":
    main()
