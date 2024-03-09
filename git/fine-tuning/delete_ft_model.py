import openai

# Set up your OpenAI API key
openai.api_key = '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'

response =openai.Model.delete("ft:gpt-3.5-turbo-0613:u2opia-mobile::7yE3nRzz")

print(response)