import openai
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)


openai.api_key = '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'

file_id = "file-bbahAlXI1HOCHv8z7yzm1234"
# openai.FineTuningJob.retrieve(file_id)
model_name = "ft:gpt-3.5-turbo-0613:u2opia-mobile::82igfK9W"

response = openai.FineTuningJob.create(
    training_file = file_id,
    model = model_name
)

job_id = response['id']
print(f"Fine Tuning job created successfully with ID: {job_id}")

# file uploaded successfully with ID: file-bbahAlXI1HOCHv8z7yzm1234
# Fine Tuning job created successfully with ID: ftjob-AlvKUn0MdrccCjDT6mr3mPRc