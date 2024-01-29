import pyperclip

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('thenlper/gte-small')

while True:
    querytext = input("Query to embed:\n")
    if querytext==exit:
        break
    embeddings = str(model.encode([querytext]).tolist())
    embeddings = embeddings[2:-2]
    pyperclip.copy(embeddings)
    print(embeddings)