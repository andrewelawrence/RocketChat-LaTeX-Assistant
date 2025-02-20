import requests

data = {"text":"how can I make a centered table with 3 columns?"}
response_llmproxy = requests.post("https://operational-missie-tufts-cs0150-04-spr25-76ae7ad6.koyeb.app/query", json=data)
print('LLMProxy Response:\n', response_llmproxy.text)