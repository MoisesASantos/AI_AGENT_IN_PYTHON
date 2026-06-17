import os
import argparse
from google import genai
from dotenv import load_dotenv
from prompts import system_prompt
from google.genai import types
from call_function import available_functions


def main():
	print(system_prompt)

	# Ler o prompt a partir da linha de comando
	parser = argparse.ArgumentParser(description="ChatBot")
	parser.add_argument("user_prompt", type=str, help="user prompt")
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()

	# Carregar variáveis de ambiente
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	if api_key is None:
		raise RuntimeError("Not found a API KEY for the model")

	# Criar cliente Gemini
	client = genai.Client(api_key=api_key)

	# Histórico da conversa
	messages: list[types.Content] = [
		types.Content(
			role="user",
			parts=[types.Part(text=args.user_prompt)]
		)
	]
	
	response = client.models.generate_content(
		model="gemini-2.5-flash",
		contents=messages,
		config=types.GenerateContentConfig(
			tools=[available_functions],
			system_instruction=system_prompt,
		),
	)
	
	if response.usage_metadata is None:
		raise RuntimeError("API request failed, try again")

	# Se houver function calls, imprime-as
	if response.function_calls:
		for function_call in response.function_calls:
			print(
				f"Calling function: {function_call.name}({function_call.args})"
			)
	# Caso contrário, imprime o texto da resposta
	else:
		print(response.text)

	# Informações extras no modo verbose
	if args.verbose:
		print(
			f"\nUser prompt: {args.user_prompt}\n"
			f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
			f"Response tokens: {response.usage_metadata.candidates_token_count}"
		)

if __name__ == "__main__": 
	main()
