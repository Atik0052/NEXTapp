from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
import torch

# 1. Load the data from the text file
with open("c:\\Users\\NishaBhakar\\Downloads\\cleaned_document.txt", "r") as file:
    lines = file.readlines()

# 2. Initialize the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
tokenizer.pad_token = tokenizer.eos_token


# 3. Tokenize the data
train_encodings = tokenizer(lines, truncation=True, padding=True, return_tensors="pt")

class GPT2Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = item['input_ids']
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])


train_dataset = GPT2Dataset(train_encodings)

# 5. Load the pre-trained GPT-2 model
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')

# 6. Define training arguments and initialize the trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=10,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# 7. Start training
trainer.train()

# 8. Save the fine-tuned model
model.save_pretrained("./fine_tuned_gpt2")
tokenizer.save_pretrained("./fine_tuned_gpt2")
