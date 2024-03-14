import requests

url = "https://api.together.xyz/v1/chat/completions"

payload = {
    "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "max_tokens": 512,
    "stop": ["</s>", "[/INST]"],
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "repetition_penalty": 1,
    "n": 1,
    "messages": [
        {
            "role": "assistant",
            "content": "You will be given a text that consists of a speech-to-text translation of an audio. Your goal is to correct the mistakes in the translation. The text will have a CONTEXT and words that do not relate to that context should be replaced by more appropriate fonetically similar words. DO NOT change words that you are not sure about. If you are not sure about a word, leave it as it is. Take this gently, it is very importantly, you should take a step-by-step manner."
        },
        {
            "role": "context",
            "content": "Aula "
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer 14675e72fbbec99c3f7e7d5e0226de9321b41b9c1c9477b28ff1570b95c2b62a"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)