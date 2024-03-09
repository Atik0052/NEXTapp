import openai

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

openai.api_key = "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"

with open("C:\\Users\\NishaBhakar\\Downloads\\json_corrected (1).jsonl", "rb") as file:
    response = openai.File.create(
        file=file,
        purpose='fine-tune'
    )

file_id = response['id']
print(f"file uploaded successfully with ID: {file_id}")


# "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" 