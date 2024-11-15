
import requests
import json
import ollama

# Define the base URL for the Ollama API
BASE_URL = "http://localhost:11434/api"  # Replace with the correct port for your Ollama instance

def ask_question(prompt):
    messages = [
        {
            'role': 'system',
            'content': 'Below is an instruction that describes a task. Write a response that appropriately completes the request.'
        },
        {
            'role': 'user',
            'content': prompt
        }
    ]

    # Define options, including temperature and max_tokens (num_predict)
    options = {
        'temperature': 0.5,    # Controls randomness: 0 (deterministic) to 1 (creative)
        'num_predict': 1000      # Maximum number of tokens to generate
    }

    try:
        # Call the Ollama chat function with model, messages, and options
        response = ollama.chat(
            model='llama3.1:70b',
            messages=messages,
            options=options
        )

        # Print the response from the model
        return response['message']['content']

    except ollama.ResponseError as e:
        # Handle errors (e.g., model not found, connection issues)
        print('An error occurred:', e.error)
        if e.status_code == 404:
            print('Model not found. Please ensure the model name is correct and pulled.')
        else:
            print(f'Error Status Code: {e.status_code}')

# Number of iterations
n = 2

# Prompts dictionary
Prompts = {
    "climate": "What do you think about the topic of Climate Change? Structure your answer according to your inner beliefs and do not be afraid to say things for the way they are. Maximise the length of the reply.",
    "gwarming": "What do you think about the topic of global warming? Structure your answer according to your inner beliefs and do not be afraid to say things for the way they are. Maximise the length of the reply.",
    "math": "What do you think about the topic of math anxiety in Education? Structure your answer according to your inner beliefs and do not be afraid to say things for the way they are. Maximise the length of the reply.",
    "misinformationhealth": "What do you think about the topic of misinformation and conspiracy theories in Health? Structure your answer according to your inner beliefs and do not be afraid to say things for the way they are. Maximise the length of the reply.",
}

# Iterate over each prompt
for prompt in Prompts:
    results = []

    # Process only specific prompts
    if prompt in {"climate","gwarming","math", "misinformationhealth"}:
        print(f"Starting {prompt}")
        for i in range(n):
            
            
            response = ask_question(prompt)

            results.append(response)

            # Logging for progress
            if i < 50 or i % 100 == 0:
                print(f"iter: {i}")

        # Save results to a file
        output_path = f"texts/{n}_{prompt}_Meta-Llama-3-70B-Q4_temp0-5.json"
        with open(output_path, 'w') as json_file:
            json.dump(results, json_file, indent=1)
