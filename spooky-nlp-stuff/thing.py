from transformers import BertTokenizer, BertForTokenClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=8)

# Example input text
text = "Albert Einstein was awarded the Nobel Prize in Physics."

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt")

# Get model predictions
with torch.no_grad():
    outputs = model(**inputs)

# Extract tokens and labels
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
labels = outputs.logits.argmax(dim=2)[0].tolist()

# Filter entities
entities = [tokens[i] for i, label in enumerate(labels) if label != 0]

print(entities)