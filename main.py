import os
import argparse

from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    print(system_prompt)

    parser = argparse.ArgumentParser(description="ChatBot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Not found a API KEY for the model")

    client = genai.Client(api_key=api_key)

    messages: list[types.Content] = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
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

    function_responses = []

    if response.function_calls:
        for function_call in response.function_calls:
			
            function_call_result = call_function(function_call, args.verbose,)

            if not function_call_result.parts:
                raise Exception("Parts are None")

            if function_call_result.parts[0].function_response is None:
                raise Exception("Function response is None")

            if (
                function_call_result.parts[0]
                .function_response
                .response
                is None
            ):
                raise Exception("Response is None")

            function_responses.append(
                function_call_result.parts[0]
            )

            if args.verbose:
                print(
                    f"-> "
                    f"{function_call_result.parts[0].function_response.response}"
                )
    else:
        print(response.text)

    if args.verbose:
        print(
            f"\nUser prompt: {args.user_prompt}\n"
            f"Prompt tokens: "
            f"{response.usage_metadata.prompt_token_count}\n"
            f"Response tokens: "
            f"{response.usage_metadata.candidates_token_count}"
        )


if __name__ == "__main__":
    main()
