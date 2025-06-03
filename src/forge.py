from gpt4all import GPT4All

# Getting user's query
query = input("Query: ")
print("Generating response...")

# Query model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
with model.chat_session():
    print(model.generate(query, max_tokens=1024))