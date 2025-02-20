import requests

response_main = requests.get("https://operational-missie-tufts-cs0150-04-spr25-76ae7ad6.koyeb.app/query")
print('Web Application Response:\n', response_main.text, '\n\n')


data = {"text":"tell me about tufts"}
response_llmproxy = requests.post("https://operational-missie-tufts-cs0150-04-spr25-76ae7ad6.koyeb.app/query", json=data)
print('LLMProxy Response:\n', response_llmproxy.text)