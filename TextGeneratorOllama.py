
import requests
import json

# Define the base URL for the Ollama API
BASE_URL = "http://localhost:11434/api"  # Replace with the correct port for your Ollama instance

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
    if prompt in {"math", "misinformationhealth"}:
        print(f"Starting {prompt}")
        for i in range(n):
            # Define the payload for the request
            payload = {
                "model": "Meollama run llama3.1:70b",
                "prompt": f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n{Prompts[prompt]}",
                "temperature": 0.5,
                "max_tokens": 1000
            }

            # Send a request to the Ollama API
            response = requests.post(f"{BASE_URL}/generate", json=payload)

            if response.status_code == 200:
                message = response.json()
                results.append(message.get("response", ""))
            else:
                print(f"Error at iteration {i}: {response.text}")

            # Logging for progress
            if i < 50 or i % 100 == 0:
                print(f"iter: {i}")

        # Save results to a file
        output_path = f"texts/llama3/{n}_{prompt}_Meta-Llama-3-70B-Q4_temp0-5.json"
        with open(output_path, 'w') as json_file:
            json.dump(results, json_file, indent=1)