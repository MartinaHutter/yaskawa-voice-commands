import torch
from sentence_transformers import SentenceTransformer, InputExample
from torch.utils.data import DataLoader
from torch.optim import AdamW
import torch.nn as nn

# Load pre-trained MiniLM model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Prepare your dataset with sentence and corresponding labels
train_examples = [
    InputExample(texts=["Pick the object"], label=0),  # pick = 0
    InputExample(texts=["Pick the product"], label=0),  # pick = 0
    InputExample(texts=["Pick the cube"], label=0),  # pick = 0
    InputExample(texts=["Pick the thing"], label=0),  # pick = 0
    InputExample(texts=["Lift the thing"], label=0),  # lift = 0
    InputExample(texts=["Lift the object"], label=0),  # lift = 0
    InputExample(texts=["Lift the cube"], label=0),  # lift = 0
    InputExample(texts=["Lift it up"], label=0),  # lift = 0
    InputExample(texts=["Grab the cube"], label=0),  # grab = 0
    InputExample(texts=["Grab the object"], label=0),  # grab = 0
    InputExample(texts=["Grab the product"], label=0),  # grab = 0
    InputExample(texts=["Get the cube"], label=0),  # get = 0
    InputExample(texts=["Get it"], label=0),  # get = 0
    InputExample(texts=["Get the object"], label=0),  # get = 0
    InputExample(texts=["Get the product"], label=0),  # get = 0
    InputExample(texts=["Place the object on table"], label=1),  # place = 1
    InputExample(texts=["Place the product on table"], label=1),  # place = 1
    InputExample(texts=["Place the object"], label=1),  # place = 1
    InputExample(texts=["Place it down"], label=1),  # place = 1
    InputExample(texts=["Put down the object"], label=1),  # put down = 1
    InputExample(texts=["Put it down"], label=1),  # put down = 1
    InputExample(texts=["Leave it"], label=1),  # leave = 1
    InputExample(texts=["Leave it down"], label=1),  # leave = 1
    InputExample(texts=["Move to home position"], label=2),  # move = 2
    InputExample(texts=["Go home"], label=2),  # go = 2
    InputExample(texts=["Go to home position"], label=2),  # go = 2
    InputExample(texts=["Parking position"], label=2),  # park = 2
]

# Custom collate function to process InputExample objects
def collate_fn(batch):
    texts = [example.texts[0] for example in batch]
    labels = torch.tensor([example.label for example in batch], dtype=torch.long)
    return texts, labels

# Create a DataLoader with the custom collate function
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16, collate_fn=collate_fn)

# Freeze pre-trained layers (optional)
for param in model.parameters():
    param.requires_grad = False

# Add a classification layer
classifier = nn.Linear(model.get_sentence_embedding_dimension(), 3)  # Assuming 3 classes

# Define optimizer and loss function
optimizer = AdamW(classifier.parameters(), lr=2e-3)
loss_fn = nn.CrossEntropyLoss()

# Training loop
epochs = 500  # Increase number of epochs
for epoch in range(epochs):
    model.train()
    classifier.train()
    total_loss = 0

    for texts, labels in train_dataloader:
        # Encode the sentences to get embeddings
        embeddings = model.encode(texts, convert_to_tensor=True)

        # Forward pass through classifier
        outputs = classifier(embeddings)

        # Calculate the loss
        loss = loss_fn(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_dataloader)}")

# Save the fine-tuned classifier
torch.save(classifier.state_dict(), "fine-tuned-classifier-robotic-commands.pt")
model.save("fine-tuned-sentence-transformer")

