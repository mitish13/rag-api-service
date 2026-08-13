from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

text = "This is a test text to check the embeddings created by sentence transformers"

embeddings = model.encode(text)
print(embeddings)

